from threading import Thread

from telegram.ext import CommandHandler, Updater

from config import Config
from log import Log
from users import Users


class Bot(object):

    def __init__(self, configpath, userspath):
        self.log = Log(configpath)
        self.config = Config(configpath)
        self.users = Users(userspath)
        self.updater = None
        self.dispatcher = None

    def init_updater(self):
        try:
            self.updater = Updater(token=self.config.get_value("BOT", "token"), use_context=True)
            self.dispatcher = self.updater.dispatcher
            return self.dispatcher
        except Exception as exc:
            self.log.LOGGING.error("Whoops. We failed to set up the updater. Error: {}".format(exc))

    def init_handler(self):
        start_handler = CommandHandler('start', self.start)
        subscribe_handler = CommandHandler('subscribe', self.subscribe)
        unsubscribe_handler = CommandHandler('unsubscribe', self.unsubscribe)
        # TODO: help command
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(subscribe_handler)
        self.dispatcher.add_handler(unsubscribe_handler)

    def start_bot(self):
        thread = Thread(target=self.updater.start_polling, args=())
        thread.start()

    def start(self, update, context):
        text = """
        Hi there! Welcome to the **Heise Online Telegram News Bot**.
Please note that the bot was **not** build by Heise Online itself.
You can view the source on GitHub: https://github.com/jpylypiw/heise-online-news-telegram-bot

**Commands the bot can execute:**
/subscribe - this starts the news subscription
/unsubscribe - this stops the automatic news sent to you

If you don't want to use the bot anymore, just delete the chat.
        """
        self.send_message(update.effective_chat.id, text, context.bot.send_message)

    def subscribe(self, update, context):
        succeeded = self.users.add_user(update.effective_chat.id)
        if succeeded:
            text = """
Thank you for subscribing to the news!
We will send you the next news when we got some.
            """
        else:
            text = """
You have already subscribed to the news.
            """
        self.send_message(update.effective_chat.id, text, context.bot.send_message)

    def unsubscribe(self, update, context):
        self.users.remove_user(update.effective_chat.id)
        text = """
You successfully unsubscribed from the list.
Thanks for using Heise Online News Bot!
You will no longer receive any messages.
        """
        self.send_message(update.effective_chat.id, text, context.bot.send_message)

    def send_message(self, chat_id, text, func, parse_mode="Markdown", disable_web_page_preview=True):
        try:
            func(chat_id=chat_id, text=text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
        except Exception as exc:
            self.log.LOGGING.error("Error sending message: {}".format(exc))
