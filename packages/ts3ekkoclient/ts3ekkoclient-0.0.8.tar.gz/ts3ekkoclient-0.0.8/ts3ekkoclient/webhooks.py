import bottle
import threading


class EkkoRemoteControl:
    def __init__(self, ekkobot, web_port=8080):
        self._ekko_app = ekkobot
        self._app = bottle.Bottle()
        self._routes()
        self.web_port = web_port

    def _routes(self):
        self._app.route('/hello/<name>', callback=self.index)
        self._app.route('/stm/<text>', callback=self.message)
        self._app.route('/ts3/whoami', callback=self.whoami)
        self._app.route('/ts3/sendtextmessage/<targetmode>/<target>/<message>')

    def index(self, name):
        return bottle.template('<b>Hello {{name}}</b>!', name=name)

    def message(self, text):
        self._ekko_app.create_connection().sendtextmessage(targetmode=2, target=1, msg=text + text)
        return "Hello World!"

    def whoami(self):
        whoami = self._ekko_app.create_connection().whoami()
        return bottle.template('{{whoami}}', whoami=whoami)

    def main(self):
        threading.Thread(target=self._app.run, kwargs=dict(host='0.0.0.0', port=int(self.web_port))).start()
