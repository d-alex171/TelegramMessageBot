# The code was created on 28/01/2018 by Alexey Dudarev

import telebot
from constants import *
from methods import *
import random
import os

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_command(message):
    answer = "Hello there"
    bot.send_message(message.chat.id, answer)

    log(message, answer)


@bot.message_handler(commands=['help'])
def help_command(message):
    answer = "here are all commands :)"
    bot.send_message(message.chat.id, answer)
    bot.send_message(message.chat.id, commands)

    log(message, answer)


@bot.message_handler(commands=["chat_start"])
def chat_start_system(message):
    if message.chat.id in searchers_for_chat_ids or message.chat.id in in_chat_user_ids:
        answer = "you are already in the chat"
        bot.send_message(message.chat.id, answer)
        log(message, answer)
    else:
        user1 = User(message.chat.id, message.chat.first_name, '00000')
        searchers_for_chat.append(user1)
        searchers_for_chat_ids.append(user1.chat_id)
        answer = "searching for chats..."
        bot.send_message(message.chat.id, answer)
        log(message, answer)

        if len(searchers_for_chat) == 2 and searchers_for_chat[0].chat_id != searchers_for_chat[1].chat_id:
            answer2 = "You are in the chat!"
            bot.send_message(searchers_for_chat[0].chat_id, answer2)
            bot.send_message(searchers_for_chat[1].chat_id, answer2)

            chat_token = random.choice(chat_token_parts) + random.choice(
                chat_token_parts) + random.choice(chat_token_parts) + random.choice(
                chat_token_parts) + random.choice(chat_token_parts)

            searchers_for_chat[0].chat_number = chat_token
            searchers_for_chat[1].chat_number = chat_token

            in_chat_users.insert(0, searchers_for_chat[0])
            in_chat_users.insert(0, searchers_for_chat[1])
            in_chat_user_ids.insert(0, searchers_for_chat[0].chat_id)
            in_chat_user_ids.insert(0, searchers_for_chat[1].chat_id)

            searchers_for_chat.remove(searchers_for_chat[0])
            searchers_for_chat.remove(searchers_for_chat[0])
            searchers_for_chat_ids.clear()

            log(message, answer2)


@bot.message_handler(commands=["chat_stop"])
def chat_stop_system(message):
    if message.chat.id in in_chat_user_ids or message.chat.id in searchers_for_chat_ids:
        i = 0
        if message.chat.id in in_chat_user_ids:
            while i != len(in_chat_users):
                if message.chat.id == in_chat_users[i].chat_id and type(i/2) == int:
                    bot.send_message(in_chat_users[i].chat_id, "you are not in the chat anymore")
                    bot.send_message(in_chat_users[i + 1].chat_id, "you are not in the chat anymore - your partner quit")
                    in_chat_users.remove(in_chat_users[i])
                    in_chat_users.remove(in_chat_users[i + 1])
                    break
                elif message.chat.id == in_chat_users[i].chat_id and type(i/2) == float:
                    bot.send_message(in_chat_users[i].chat_id, "you are not in the chat anymore")
                    bot.send_message(in_chat_users[i - 1].chat_id, "you are not in the chat anymore - your partner quit")
                    in_chat_users.remove(in_chat_users[i])
                    in_chat_users.remove(in_chat_users[i - 1])
                    break
                else:
                    i += 1
        elif message.chat.id in searchers_for_chat_ids:
                if message.chat.id == searchers_for_chat_ids[0]:
                    searchers_for_chat_ids.remove(searchers_for_chat_ids[0])
                    answer = "you don't search for chats anymore"
                    bot.send_message(message.chat.id, answer)
                    log(message, answer)
    else:
        answer = "you are not in the chat right now"
        bot.send_message(message.chat.id, answer)
        log(message, answer)


@bot.message_handler(content_types=['text'])
def text_reactor(message):
    if message.chat.id in in_chat_user_ids:
        i = 0
        n = 0
        while n != len(in_chat_users):
            if message.chat.id == in_chat_users[n].chat_id:
                break
            else:
                n += 1
        while i != len(in_chat_users):
            if in_chat_users[n].chat_id != in_chat_users[i].chat_id and in_chat_users[n].chat_number == in_chat_users[i].chat_number:
                bot.send_message(in_chat_users[i].chat_id, message.text)
                log(message, None)
                break
            else:
                i += 1
    else:
        answer = random.choice(default_text_reactions)
        bot.send_message(message.chat.id, answer)
        log(message, answer)

bot.polling(True, interval=0)
