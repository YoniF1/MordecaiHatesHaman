import os
from dotenv import load_dotenv
import telebot
from telebot import types
from volunteers import MyVolunteer
from VolunteerManager import Manager
from youtube import Comments

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

class Bot:
    def __init__(self, video_id):
        self.user_comment_index = {}
        self.video_id = video_id

    def send_welcome(self, message):
        user_id = str(message.from_user.id)
        new_user = MyVolunteer(user_id)
        does_exist = Manager.get_by_id(new_user.chat_id)
        if not does_exist:
            new_user.save()
            bot.reply_to(message, "Welcome! You've been added to the volunteers list.")
            bot.reply_to(message, "Hello, this is your first message, let's fight against antisemitism!")
            bot.reply_to(message, "Here are the instructions for all volunteers that registered for our program:Our program automatically detects anti-Semitic comments of different YouTube videos and sends links to the comments. Your task is to reply to every comment and to leave a link to our web-page. We need to convince those people to be on our side and fight against antisemitism together")
            bot.reply_to(message, "Type or select /get_to_work to receive your first antisemitic comment")
        else:
            print("You're already there, type /get_to_work to fight antisemitism")

    def get_to_work(self, message):
        user_id = message.from_user.id
        user = MyVolunteer(user_id)
        does_exist = Manager.get_by_id(user.chat_id)
        if does_exist:
                if user_id not in self.user_comment_index:
                    self.user_comment_index[user_id] = 0 
                self.send_bad_comment(user.chat_id, self.user_comment_index[user_id])
                self.user_comment_index[user_id] += 1
        else:
            print("You need to be registered first, type /start")

    def create_button(self, chat_id, command):
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Get another comment", callback_data='button1')
        markup.add(button1)
        bot.send_message(chat_id=chat_id, text=command, reply_markup=markup)

    def when_user_clicks(self, callback):
        user_id = callback.from_user.id
        if callback.data == 'button1':
            if user_id not in self.user_comment_index:
                self.user_comment_index[user_id] = 0 
        self.send_bad_comment(user_id, self.user_comment_index[user_id])
        self.user_comment_index[user_id] += 1
        bot.send_message(callback.message.chat.id, 'Let\'s do another comment!')

    def send_bad_comment(self, chat_id, comment_index):
        comments = Comments(self.video_id)
        bad_comments = comments.find_bad_comments()

        if bad_comments and comment_index < len(bad_comments):
            comment = bad_comments[comment_index]
            message = f"A bad comment was found:\n\n {comment[1]}.\n\n Click the link to respond: {self.build_url(comment[3], comment[4])}"
            bot.send_message(chat_id=chat_id, text=message)
            self.create_button(chat_id, 'Do you want to continue?')
        else:
            bot.send_message(chat_id=chat_id, text="No more bad comments to respond to for now.")

    def build_url(self, video_id, comment_id):
        return f'https://www.youtube.com/watch?v={video_id}&lc={comment_id}'

bot_instance = Bot('8klRQ-zCVm4')

@bot.message_handler(commands=['start'])
def start(message):
    bot_instance.send_welcome(message)

@bot.message_handler(commands=['get_to_work', 'skip'])
def get_to_work(message):
    bot_instance.get_to_work(message)

@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback):
    bot_instance.when_user_clicks(callback)

bot.polling()
