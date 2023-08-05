import logging
import requests
import ts3.response
from ts3ekkoutil.envconsts import EkkoPropertyNames as epn

try:
    from ts3ekkoclient.ts3ekko import TS3Ekko
    from ts3ekkoclient.cogs.media import MediaCog
    from ts3ekkoclient.cogs.text import TextCog
    from ts3ekkoclient.event_type import EventType
    from ts3ekkoclient.errors import EkkoUnsuitedCommand, EkkoParsingError, EkkoNonexistentPermissionDoc, \
        EkkoArgparserMessage
    from ts3ekkoclient.models import Invoker, startup
    from ts3ekkoclient.permission import PermissionManager, InvokerCtx
    from ts3ekkoclient.argparser import PermissionParser, UtilityParser
except ImportError:
    from .ts3ekko import TS3Ekko
    from .cogs.media import MediaCog
    from .cogs.text import TextCog
    from .event_type import EventType
    from .errors import EkkoUnsuitedCommand, EkkoParsingError, EkkoNonexistentPermissionDoc, EkkoArgparserMessage
    from .models import Invoker, startup
    from .permission import PermissionManager, InvokerCtx
    from .argparser import PermissionParser, UtilityParser

logger = logging.getLogger('ekkoclient-ekkobot')


class EkkoCorePermission:
    SPAWN = 'control.spawn'
    DESPAWN = 'control.despawn'
    JOIN = 'control.join'
    NAME = 'control.name'

    WHOAMI = 'other.whoami'

    PERMISSION_ADD = 'permission.add'
    PERMISSION_DELETE = 'permission.delete'
    PERMISSION_GET = 'permission.get'
    PERMISSION_INFO = 'permission.info'


class EkkoBot(TS3Ekko):
    def __init__(self, args):
        self.args = args
        super().__init__(apikey=args[epn.TS3_CLIENT_APIKEY], server=args[epn.TS3_CLIENTQUERY_HOST],
                         port=args[epn.TS3_CLIENTQUERY_PORT], bot_username=args[epn.TS3_USERNAME])
        self.register_hooks()

        self.dbsession = startup(self.args[epn.DB_USERNAME], self.args[epn.DB_PASSWORD], self.args[epn.DB_HOST],
                                 self.args[epn.DB_DBNAME])

        self.permission_manager = PermissionManager(self)

        self.add_cog(MediaCog(self, self.args, self.dbsession))
        self.add_cog(TextCog(self, self.args, self.dbsession))

    def can(self, permission, event, quiet=False, deny_msg='Sorry, can\'t do that. You might not have the required '
                                                           'permission for that.', quiet_permission_name=False):
        invoker_ctx = self.parse_invoker_context(event[0])
        if not self.permission_manager.can(permission, invoker_ctx):
            if not quiet and quiet_permission_name:
                self.reply(deny_msg, event)
            elif not quiet and not quiet_permission_name:
                self.reply(f'{deny_msg} (permission name: {permission})', event)
            return False
        else:
            return True

    def parse(self, parse_func, event: ts3.response.TS3Event, *args, **kwargs):
        """
        Calls a parsing function with the given arguments. Replies with usage and error in teamspeak to the event,
        should the parsing be not successful.

        :param parse_func: a argparser function (see in `~ts3ekkoclient.parser`)
        :param event: a ts3 event to which can be replied
        :param args: args for the parser function
        :param kwargs: kwargs for the parser function
        :returns: from the parse_func
        :raises EkkoParsingError: if parse_func is not successful
        """
        try:
            return parse_func(*args, **kwargs)
        except EkkoParsingError as e:
            # Something was missing (required args e.g.)
            self.reply(e.__str__(), event)
            raise
        except EkkoArgparserMessage as e:
            # These are messages like help or usage
            self.reply(e.__str__(), event)
            # This exception should be excepted further up the handling chain and be quietly discarded,
            # while also aborting the handling (because it was handled succesfully).
            raise

    def can_invoker(self, permission: str, invoker_ctx: InvokerCtx) -> bool:
        """
        Can/Permission-Check relay to permission manager.
        :param permission: name of the requested permission
        :param invoker_ctx:
        :return: bool, if the invoker is allowed to perform the action or not
        """
        return self.permission_manager.can(permission, invoker_ctx)

    def register_hooks(self):
        """
        Enables command hooks for events like spawning and despawning.
        FIXME: would really like this to be decorators, guess I could do that sometimes in the future
        """
        self.add_command(EventType.TEXTMESSAGE, self.relay_spawn, help_cmd_str='!spawn')
        self.add_command(EventType.TEXTMESSAGE, self.relay_despawn, help_cmd_str='!despawn')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_join, help_cmd_str='!join')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_help)
        self.add_command(EventType.TEXTMESSAGE, self.cmd_name, help_cmd_str='!name')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_whoami, help_cmd_str='!whoami')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_permission, priority=75, help_cmd_str='!permission')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_permission_add, help_cmd_str='!permission')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_permission_get, help_cmd_str='!permission')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_permission_info, help_cmd_str='!permission')
        self.add_command(EventType.TEXTMESSAGE, self.cmd_permission_delete, help_cmd_str='!permission')

    def relay_spawn(self, event):
        if self.check_cmd_suitability('^!spawn', event[0]['msg']):
            if self.can(EkkoCorePermission.SPAWN, event):
                invoker_clid = event[0]['invokerid']
                invoker_cid = self.ts3conn.cid_from_clid(invoker_clid)
                requests.get(f'http://{self.args[epn.EKKO_MANAGE_SERVER]}:{self.args[epn.EKKO_MANAGE_PORT]}'
                             f'/cmd/spawn/{invoker_cid}')

    def relay_despawn(self, event):
        if self.check_cmd_suitability('^!despawn', event[0]['msg']):
            if self.can(EkkoCorePermission.DESPAWN, event):
                self.reply('Exiting now! o/', event)
                requests.get(f'http://{self.args[epn.EKKO_MANAGE_SERVER]}:{self.args[epn.EKKO_MANAGE_PORT]}'
                             f'/cmd/despawn/{self.args[epn.EKKO_NODE_ID]}')
                exit(0)

    def cmd_join(self, event):
        if self.check_cmd_suitability('^!join', event[0]['msg']):
            if self.can(EkkoCorePermission.JOIN, event):
                invoker_clid = event[0]['invokerid']
                invoker_cid = self.ts3conn.cid_from_clid(invoker_clid)
                bot_clid = self.ts3conn.whoami()[0]['clid']
                self.ts3conn.clientmove(clid=bot_clid, cid=invoker_cid)

    def cmd_name(self, event):
        cmd_prefix = '!name'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.NAME, event):
                name = self.parse(UtilityParser.parse_name, event, '!name', event[0]['msg'])
                self.ts3conn.clientupdate(client_nickname=name)

    def cmd_whoami(self, event):
        if self.check_cmd_suitability('^!whoami', event[0]['msg']):
            if self.can(EkkoCorePermission.WHOAMI, event):
                ictx = self.parse_invoker_context(event[0])
                self.reply(f'username: {ictx.username} | server groups: {ictx.server_groups} | '
                           f'channel group: {ictx.channel_group} | unique id: {ictx.unique_id}', event)

    def cmd_help(self, event):
        if self.check_cmd_suitability('^!help', event[0]['msg']):
            help_cmd_strs = set(sorted(
                [str(cmd.help_cmd_str) for cmd in self.commands if cmd.help_cmd_str is not None]
            ))
            help_reply = f'List of all available command sets: \n    ' + '\n    '.join(
                help_cmd_strs) + '\n To receive more help about a specific command, use the `-h` or `--help` flag when calling a command (e.g. !skip --help)'
            self.reply(help_reply, event)

    def cmd_permission(self, event):
        """
        Command: !permission

        Fallback command in case none of the other !permission commands catches on, replies with usage information.

        :param event: TS3Event
        """
        cmd_prefix = '!permission'
        cmd_usage = 'usage: !permission [ add | get | info | delete ]'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            self.reply(cmd_usage, event)

    def cmd_permission_add(self, event):
        cmd_prefix = '!permission add'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.PERMISSION_ADD, event):
                permission, uid, cg, sg = self.parse(PermissionParser.parse_add, event, cmd_prefix, event[0]['msg'])
                ictx = InvokerCtx(sg, cg, uid)
                logger.debug(ictx)
                self.permission_manager.add_grant(permission, ictx)

    def cmd_permission_get(self, event):
        cmd_prefix = '!permission get'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.PERMISSION_GET, event):
                permission = self.parse(PermissionParser.parse_get, event, cmd_prefix, event[0]['msg'])
                p_grants = self.permission_manager.get_grant(permission)
                # FIXME: doesnt work
                sgid_data = self.resolve_servergroups()
                logger.debug(f'sgid_data: {sgid_data}')
                grants, denies = '', ''
                logger.debug(p_grants)
                for index, grant in enumerate(p_grants):
                    if not grant.deny:
                        grants += f'\n{grant.pretty_noname_repr(sgid_data)}'
                    else:
                        denies += f'\n{grant.pretty_noname_repr(sgid_data)}'
                logger.debug(grants)
                logger.debug(denies)
                if grants or denies:
                    self.reply(f'Allowed entities: {grants or "none"}\n '
                               f'Forbidden entities: {denies or "none"}', event)
                else:
                    self.reply('no grants for this permission found.', event)

    def cmd_permission_info(self, event):
        cmd_prefix = '!permission info'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.PERMISSION_INFO, event):
                permisson = self.parse(PermissionParser.parse_info, event, cmd_prefix, event[0]['msg'])
                try:
                    perm_doc = self.permission_manager.get_grant_info(permisson)
                    self.reply(perm_doc.formatted_long, event)
                except EkkoNonexistentPermissionDoc as e:
                    self.reply(e, event)

    def cmd_permission_delete(self, event):
        cmd_prefix = '!permission delete'
        if self.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.can(EkkoCorePermission.PERMISSION_DELETE, event):
                permisson = self.parse(PermissionParser.parse_delete, event, cmd_prefix, event[0]['msg'])
                try:
                    deleted_perm = self.permission_manager.delete_grant(permisson)
                except EkkoNonexistentPermissionDoc as e:
                    self.reply(e, event)
                else:
                    self.reply(f'permission deleted! ({deleted_perm.__repr__()})', event)

    @staticmethod
    def color_message(text, color='#1433b1'):
        """
        Puts BB-Code formatting around the provided text.

        :param text: text which should be colored.
        :param color: the color which should be put on the text.
        :return: color BB-code formatted string.
        """
        return f'[color={color}]{text}[/color]'

    def determine_invoker(self, event):
        """
        Searches database for existing, matching invoker object.
        Returns found invoker or creates new object if not found.

        :param event: ts3event
        :return: Invoker object
        """
        inv = Invoker(event['invokeruid'], event['invokername'])
        inv_query = self.dbsession.query(Invoker).filter_by(unique_id=inv.unique_id, username=inv.username).first()
        if inv_query is not None:
            return inv_query
        else:
            return inv

    def resolve_servergroups(self) -> dict:
        """
        Create dataset of servergroup-ids (sgids) and their respective string name.

        FIXME: doesnt work, pls fix (ts3conn.servergrouplist() returns nothing ??)
        :return: dict => keys are the sgids, the data is the string name
        """
        resolved_sgids = {}
        try:
            sgid_dataset = self.ts3conn.servergrouplist()
            logger.debug(sgid_dataset.__dict__)
            for sgid_data in sgid_dataset:
                resolved_sgids[str(sgid_data['sgid'])] = sgid_data['name']
        except IndexError:
            pass
        logger.debug(resolved_sgids)
        return resolved_sgids

    def parse_invoker_context(self, event) -> InvokerCtx:
        """
        Creates InvokerCtx (Invoker Context) based on the data available in the provided event. This includes
        data like server & channel groups of the invoker, as well as their unique id.

        :param event: TS3Event
        :return: InvokerCtx()
        """
        client_id = event['invokerid']

        client_variables = self.ts3conn.clientvariable(client_id, "client_channel_group_id", "client_servergroups")[0]
        logger.debug(client_variables)
        return InvokerCtx(client_variables['client_servergroups'].split(','),
                          client_variables['client_channel_group_id'], event['invokeruid'], event['invokername'])

    @staticmethod
    def split_message(remaining_message, part_length=1024, split_chars=('\n', ' '), text_mod=None):
        """
        Splits a message into parts to match a certain maximum length restriction.

        :param remaining_message: string/message which should be split
        :param part_length: maximum length of each part
        :param split_chars: characters used to split the message into parts, FIFO processing
        :param text_mod: function which transforms text (like color coding, needed to match part_length)
        :return: list of parts from the message
        """

        def dummy_text_mod(s):
            return s

        if text_mod is None:
            text_mod = dummy_text_mod

        continue_pad = '\n'
        parts = []
        # process split_chars until all parts match part_length
        for split_char in split_chars:
            while True:
                if len(remaining_message) <= 0:
                    return parts

                # split message and prepare for re-assemble
                split_result = remaining_message.split(split_char)
                stitched_message = ''
                for splitter in split_result:
                    # create imaginary part based on the current splitter and transform it in the text_mod function
                    future_part = text_mod(f'{continue_pad}{stitched_message}{splitter}{split_char}')
                    # check if this imaginary part would meet the requirement
                    if len(future_part) <= part_length:
                        stitched_message += splitter + split_char
                    else:
                        break

                if not parts and stitched_message != '':
                    # the first part should not have the continue_pad
                    # remove last appended split char again
                    parts.append(text_mod(stitched_message[:-len(split_char)]))
                elif stitched_message != '':
                    # remove last appended split char again
                    parts.append(text_mod(continue_pad + stitched_message[:-len(split_char)]))
                else:
                    break

                # remove processed string from remaining message
                remaining_message = remaining_message[len(stitched_message):]

    def reply(self, message, event):
        """
        Reply to the text message described by the event parameter.

        :param message: the bots message towards the other client.
        :param event: the source event to which should be replied to.
        :raises NotImplementedError: if the source event is not a text message.
        """
        if EventType.get_type(event) == EventType.TEXTMESSAGE:
            logger.debug(message)
            logger.debug(event[0])
            for message in self.split_message(message, part_length=1000, text_mod=lambda s: self.color_message(s)):
                self.ts3conn.sendtextmessage(targetmode=event[0]['targetmode'],
                                             target=event[0]['invokerid'],
                                             msg=message)
        else:
            raise NotImplementedError()
