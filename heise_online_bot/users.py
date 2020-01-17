from config import Config


class Users(object):

    def __init__(self, userspath):
        self.usersconfig = Config(userspath)

    def add_user(self, chat_id):
        curr_ids = str(self.usersconfig.get_value("USERS", "chat_ids"))
        chat_id = str(chat_id)
        prefix = ";"
        if curr_ids == "":
            prefix = ""
        if not chat_id in curr_ids:
            self.usersconfig.set_value("USERS", "chat_ids", curr_ids + "{}{}".format(prefix, chat_id))
            return True
        return False

    def remove_user(self, chat_id):
        curr_ids = self.get_user_list()
        curr_ids.remove(str(chat_id))
        self.usersconfig.set_value("USERS", "chat_ids", ';'.join(curr_ids))

    def get_user_list(self):
        curr_ids = str(self.usersconfig.get_value("USERS", "chat_ids"))
        return curr_ids.split(';')
