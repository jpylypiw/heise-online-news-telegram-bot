import utility
from config import Config


def deploy():
    set_config_ini()
    set_news_ini()
    set_users_ini()


def set_config_ini():
    configpath = utility.get_abs_path_of_filepath(__file__) + "/config/config.ini"
    copy_config_content(configpath)
    config = Config(configpath + ".example")
    config.set_value("LOG", "level", "info")
    config.set_value("LOG", "to_files", "yes")
    config.set_value("LOG", "to_stdout", "yes")
    config.set_value("LOG", "filepath", "/var/log")
    config.set_value("LOG", "filename", "heise-online-bot")

    config.set_value("BOT", "token", "")


def set_news_ini():
    configpath = utility.get_abs_path_of_filepath(__file__) + "/config/news.ini"
    copy_config_content(configpath)
    config = Config(configpath + ".example")
    config.set_value("NEWS", "url", "https://www.heise.de/rss/heise-atom.xml")
    config.set_value("NEWS", "last_id", "")
    config.set_value("NEWS", "interval", "5")


def set_users_ini():
    configpath = utility.get_abs_path_of_filepath(__file__) + "/config/users.ini"
    copy_config_content(configpath)
    config = Config(configpath + ".example")
    config.set_value("USERS", "chat_ids", "")


def copy_config_content(configpath):
    configexamplepath = configpath + ".example"
    content = utility.file_get_contents(configpath)
    utility.create_file_if_not_exists(configexamplepath)
    utility.write_into_file(configexamplepath, content)


if __name__ == "__main__":
    deploy()
