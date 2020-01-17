"""this is the inofficial heise online telegram news bot"""
from bot import Bot
from news import News
from log import Log
from utility import get_abs_path_of_filepath


def run_bot():
    """run_bot is the main function of the program"""
    configpath = get_abs_path_of_filepath(__file__) + "/config/config.ini"
    userspath = get_abs_path_of_filepath(__file__) + "/config/users.ini"
    newspath = get_abs_path_of_filepath(__file__) + "/config/news.ini"
    bot = Bot(configpath, userspath)
    try:
        dispatcher = bot.init_updater()
        news = News(configpath, newspath, userspath, dispatcher)
        bot.init_handler()
        bot.start_bot()
        news.start_thread()
    except KeyboardInterrupt:
        news.stopflag = True
    except Exception as exc:
        Log.LOGGING.error("Unhandled Exception: {}".format(exc))


if __name__ == "__main__":
    run_bot()
