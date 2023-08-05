import re
import datetime
import logging

try:
    from ts3ekkoclient.event_type import EventType
    from ts3ekkoclient.errors import EkkoUnsuitedCommand, EkkoNonexistentAlias
    from ts3ekkoclient.argparser import TextAliasParser
    from ts3ekkoclient.models import TextAlias, Invoker, startup, desc
except ImportError:
    from ..event_type import EventType
    from ..errors import EkkoUnsuitedCommand, EkkoNonexistentAlias
    from ..argparser import TextAliasParser
    from ..models import TextAlias, Invoker, startup, desc

logger = logging.getLogger('ekkocog-textalias')


class TextCogPermission:
    SET_TEMPORARY = 'textalias.temporary.set'
    GET_TEMPORARY = 'textalias.temporary.get'
    DELETE_TEMPORARY = 'textalias.temporary.delete'
    LIST_TEMPORARY = 'textalias.temporary.list'

    SET_PERMANENT = 'textalias.permanent.set'
    GET_PERMANENT = 'textalias.permanent.get'
    DELETE_PERMANENT = 'textalias.permanent.delete'
    LIST_PERMANENT = 'textalias.permanent.list'


class TextCog:
    def __init__(self, ekkobot, args, dbsession):
        self.ekko_bot = ekkobot

        # same config as bot
        self.args = args
        self.dbsession = dbsession

        # list of temporary aliase, not saved in database
        self.temporary_aliase = []

    @property
    def commands(self):
        """
        Returns data for command hooks creation for events like textalias set/get, etc.
        :return list of tuple in format: (EventType-int, callback-func, priority-int, name-str, help_cmd_str-str)
        """
        return [
            (EventType.TEXTMESSAGE, self.cmd_textalias, 75, None, '!textalias'),
            (EventType.TEXTMESSAGE, self.cmd_textalias_set, 100, None, '!textalias'),
            (EventType.TEXTMESSAGE, self.cmd_textalias_get, 100, None, '!textalias'),
            (EventType.TEXTMESSAGE, self.cmd_textalias_delete, 100, None, '!textalias'),
            (EventType.TEXTMESSAGE, self.cmd_textalias_list_temporary, 100, None, '!textalias'),
            (EventType.TEXTMESSAGE, self.cmd_textalias_list_permanent, 100, None, '!textalias'),
            (EventType.TEXTMESSAGE, self.cmd_textalias_set_shortform, 100, None, '!textalias'),
            (EventType.TEXTMESSAGE, self.cmd_textalias_get_shortform, 100, None, '!textalias'),
        ]

    def _add_alias(self, aliasname, aliasvalue, invoker, permanent=False):
        """
        Creates a new alias based on the parameters and either saves it in memory (temporary)
        or in the database (permanent).
        :param aliasname: Keyword of the alias
        :param aliasvalue: Replacement text of the alias
        :param invoker: Invoker object
        :param permanent: Flag indicating if the alias is stored in memory or in the database
        :return: the created TextAlias object
        """
        new_alias = TextAlias()
        new_alias.alias = aliasname
        new_alias.value = aliasvalue
        new_alias.invoker = invoker
        new_alias.timestamp = datetime.datetime.now()
        logger.debug(new_alias)
        if permanent:
            self.dbsession.add(new_alias)
            self.dbsession.commit()
        else:
            for alias in self.temporary_aliase:
                if alias.alias == aliasname:
                    self.temporary_aliase.remove(alias)
            self.temporary_aliase.append(new_alias)
        return new_alias

    def _find_permanent_alias(self, aliasname):
        ordered_query = self.dbsession.query(TextAlias).filter_by(alias=aliasname).order_by(TextAlias.id.desc())
        if ordered_query.all() and not ordered_query.first().is_deleted:
            return ordered_query.first()
        else:
            raise EkkoNonexistentAlias(aliasname, True)

    def _find_temporary_alias(self, aliasname):
        for alias in self.temporary_aliase:
            if alias.alias == aliasname:
                return alias
        raise EkkoNonexistentAlias(aliasname, False)

    def _delete_temporary_alias(self, aliasname):
        for t_alias in self.temporary_aliase:
            if t_alias.alias == aliasname:
                self.temporary_aliase.remove(t_alias)

    def _delete_permanent_alias(self, aliasname, invoker):
        try:
            self._find_permanent_alias(aliasname)
        except EkkoNonexistentAlias:
            pass
        else:
            self._add_alias(aliasname, None, invoker, True)

    def _list_temporary_alias(self):
        reply_msg = 'temporary available alias:'
        if self.temporary_aliase:
            for alias in self.temporary_aliase:
                reply_msg += f'\n{alias.alias}'
        else:
            reply_msg += '\nno temporary alias available!'

        return reply_msg

    def _list_permanent_alias(self):
        reply_msg = 'permanent available alias:'
        ta_q = self.dbsession.query(TextAlias).order_by(TextAlias.id.desc()).all()

        # filter out the unique names of alias
        unique_ta_names = []
        unique_ta = []
        for alias in ta_q:
            logger.debug(alias)
            if alias.alias not in unique_ta_names and not alias.is_deleted:
                unique_ta.append(alias)
            unique_ta_names.append(alias.alias)

        # creating the actual listing (output)
        if unique_ta:
            for alias in unique_ta:
                logger.debug(f'added following TA to list-permanent query; {alias}')
                reply_msg += f'\nKeyword: {alias.alias}, set by {alias.invoker.username},' \
                             f' set on {alias.timestamp}'
        else:
            reply_msg += '\nno permanent alias available!'

        return reply_msg

    def delete_alias(self, aliasname, invoker, permanent):
        if permanent:
            return self._delete_permanent_alias(aliasname, invoker)
        else:
            return self._delete_temporary_alias(aliasname)

    def find_alias(self, aliasname, permanent=None):
        if permanent is None or permanent:
            try:
                return self._find_permanent_alias(aliasname)
            except EkkoNonexistentAlias:
                if permanent:
                    raise
                else:
                    return self._find_temporary_alias(aliasname)
        elif not permanent:
            return self._find_temporary_alias(aliasname)

        raise EkkoNonexistentAlias(aliasname, permanent)

    def cmd_textalias(self, event):
        """
        Command: !textalias

        Fallback command in case none of the other !textalias commands catches on, replies with usage information.

        :param event: TS3Event
        """
        cmd_prefix = '!textalias'
        cmd_usage = 'usage: !textalias [set|get|delete|list-temporary|list-permanent]'
        if self.ekko_bot.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            self.ekko_bot.reply(cmd_usage, event)

    def cmd_textalias_set(self, event):
        """
        Command: !textalias set

        Creates a new textalias based on the parameters, should the invoker be allowed to create one.
        Can create temporary and permanent alias.

        See `TextAliasParser.parse_set` for parameters.

        :param event: TS3Event
        """
        cmd_prefix = '!textalias set'
        if self.ekko_bot.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            permanent, aliasname, aliasvalue = self.ekko_bot.parse(TextAliasParser.parse_set, event, cmd_prefix, event[0]['msg'])
            invoker = self.ekko_bot.determine_invoker(event[0])
            if permanent and self.ekko_bot.can(TextCogPermission.SET_PERMANENT, event):
                self._add_alias(aliasname, aliasvalue, invoker, permanent)
            elif not permanent and self.ekko_bot.can(TextCogPermission.SET_TEMPORARY, event):
                self._add_alias(aliasname, aliasvalue, invoker, permanent)

    def cmd_textalias_get(self, event):
        cmd_prefix = '!textalias get'
        if self.ekko_bot.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            permanent, aliasname = self.ekko_bot.parse(TextAliasParser.parse_get, event, cmd_prefix, event[0]['msg'])
            try:
                if permanent and self.ekko_bot.can(TextCogPermission.GET_PERMANENT, event):
                    alias = self.find_alias(aliasname, permanent)
                    self.ekko_bot.reply(alias.value, event)
                elif not permanent and self.ekko_bot.can(TextCogPermission.GET_TEMPORARY, event):
                    alias = self.find_alias(aliasname, permanent)
                    self.ekko_bot.reply(alias.value, event)
            except EkkoNonexistentAlias:
                self.ekko_bot.reply('no such alias available.', event)

    def cmd_textalias_delete(self, event):
        cmd_prefix = '!textalias delete'
        if self.ekko_bot.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            permanent, aliasname = self.ekko_bot.parse(TextAliasParser.parse_delete, event, cmd_prefix, event[0]['msg'])
            invoker = self.ekko_bot.determine_invoker(event[0])
            try:
                if permanent and self.ekko_bot.can(TextCogPermission.DELETE_PERMANENT, event):
                    self.delete_alias(aliasname, invoker, permanent)
                elif not permanent and self.ekko_bot.can(TextCogPermission.DELETE_TEMPORARY, event):
                    self.delete_alias(aliasname, invoker, permanent)
            except EkkoNonexistentAlias:
                self.ekko_bot.reply('no such alias available for deletion.', event)

    def cmd_textalias_list_temporary(self, event):
        cmd_prefix = '!textalias list-temporary'
        if self.ekko_bot.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.ekko_bot.can(TextCogPermission.LIST_TEMPORARY, event):
                reply_msg = self._list_temporary_alias()
                self.ekko_bot.reply(reply_msg, event)

    def cmd_textalias_list_permanent(self, event):
        cmd_prefix = '!textalias list-permanent'
        if self.ekko_bot.check_cmd_suitability(f'^{cmd_prefix}', event[0]['msg']):
            if self.ekko_bot.can(TextCogPermission.LIST_TEMPORARY, event):
                reply_msg = self._list_permanent_alias()
                self.ekko_bot.reply(reply_msg, event)

    def cmd_textalias_set_shortform(self, event):
        cmd_regex = '^!~(?P<aliasname>\w+) (?P<value>.+)$'

        def parse(cmd_str):
            result = re.search(cmd_regex, cmd_str)
            return result.group('aliasname'), result.group('value')

        if self.ekko_bot.check_cmd_suitability(cmd_regex, event[0]['msg']):
            if self.ekko_bot.can(TextCogPermission.SET_TEMPORARY, event):
                aliasname, aliasvalue = parse(event[0]['msg'])
                invoker = self.ekko_bot.determine_invoker(event[0])
                self._add_alias(aliasname, aliasvalue, invoker)

    def cmd_textalias_get_shortform(self, event):
        cmd_regex = '^!~(?P<aliasname>\w+)$'

        def parse(cmd_str):
            result = re.search(cmd_regex, cmd_str)
            return result.group('aliasname')

        if self.ekko_bot.check_cmd_suitability(cmd_regex, event[0]['msg']):
            aliasname = parse(event[0]['msg'])
            try:
                if self.ekko_bot.can(TextCogPermission.GET_TEMPORARY, event, quiet=True) \
                        and self.ekko_bot.can(TextCogPermission.GET_PERMANENT, event, quiet=True):
                    alias = self.find_alias(aliasname)
                    self.ekko_bot.reply(alias.value, event)
                elif self.ekko_bot.can(TextCogPermission.GET_TEMPORARY, event):
                    alias = self.find_alias(aliasname, permanent=False)
                    self.ekko_bot.reply(alias.value, event)
            except EkkoNonexistentAlias:
                self.ekko_bot.reply('no such alias available.', event)
