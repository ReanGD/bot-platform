import os
import json
from telegram.ext import Filters, Updater, MessageHandler


class Bot(object):
    def __init__(self):
        cred_dir = os.path.join(os.path.expanduser('~'), '.config', 'credentials')
        if not os.path.exists(cred_dir):
            os.makedirs(cred_dir)
        self._config_file = os.path.join(cred_dir, 'telergam.json')
        self._updater = None
        self._root_id = None
        self._allow_ids = []
        self._callback = None

    def _handle_text(self, bot, update):
        if update.message.from_user.id in self._allow_ids:
            answer = self._callback(update.message.text)
        else:
            answer = 'Skip'
        update.message.reply_text(answer)

    def create(self, callback):
        config = json.load(open(self._config_file, 'r'))
        self._updater = Updater(config['token'])
        self._root_id = config['root_id']
        self._allow_ids = config['allow_ids']
        self._callback = callback

        text_handler = MessageHandler(Filters.text, self._handle_text)
        self._updater.dispatcher.add_handler(text_handler)

    def run(self):
        self._updater.start_polling()
        self._updater.idle()
