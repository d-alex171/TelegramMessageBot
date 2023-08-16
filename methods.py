import datetime

searchers_for_chat = []
in_chat_users = []
in_chat_user_ids = []
searchers_for_chat_ids = []


def log(user_message, bot_answer):
    print("------")
    print(datetime.datetime.now())
    print("message from ", user_message.from_user.first_name, user_message.chat.id)
    print(user_message.text)
    print("bot's answer:")
    print(bot_answer)


class User:

    def __init__(self, chat_id, first_name, chat_number):
        self.chat_id = chat_id
        self.first_name = first_name
        self.chat_number = chat_number
