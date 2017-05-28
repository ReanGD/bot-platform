from telegram.ext import Filters, Updater, MessageHandler


class Bot(object):
    def __init__(self):
        self._updater = None
        self._root_id = None
        self._allow_ids = []
        self._callback = None

    def _handle_text(self, bot, update):
        if update.message.from_user.id in self._allow_ids:
            answer = self._callback(update.message.text)
        else:
            answer = 'Access is denied'
        update.message.reply_text(answer)

    def create(self, config, callback):
        self._updater = Updater(config['token'])
        self._root_id = config['root_id']
        self._allow_ids = config['allow_ids']
        self._callback = callback

        text_handler = MessageHandler(Filters.text, self._handle_text)
        self._updater.dispatcher.add_handler(text_handler)

    def run(self):
        self._updater.start_polling()
        self._updater.idle()
