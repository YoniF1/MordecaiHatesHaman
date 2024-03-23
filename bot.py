import os
from dotenv import load_dotenv
import telebot
from volunteers import MyVolunteer
from VolunteerManager import Manager
from youtube import Comments

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

user_comment_index = {} 

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    new_user = MyVolunteer(user_id)
    does_exist = Manager.get_by_id(new_user.chat_id)
    if not does_exist:
        new_user.save()
        bot.reply_to(message, "Welcome! You've been added to the volunteers list.")
        bot.reply_to(message, "Hello, this is your first message, let's fight against antisemitism!")
        bot.reply_to(message, "Here are the instructions for all volunteers that registered for our program:Our program automatically detects anti-Semitic comments of different YouTube videos and sends links to the comments. Your task is to reply to every comment and to leave a link to our web-page. We need to convince those people to be on our side and fight against antisemitism together")
        bot.reply_to(message, "Type /get_to_work to receive your first antisemitic comment")
    else:
        print("You're already there, type /get_to_work to fight antisemitism")

@bot.message_handler(commands=['get_to_work'])
def get_to_work(message):
   user_id = message.from_user.id
   user = MyVolunteer(user_id)
   does_exist = Manager.get_by_id(user.chat_id)
   if does_exist:
        if user_id not in user_comment_index:
            user_comment_index[user_id] = 0 
        send_bad_comment(user, user_comment_index[user_id])
        user_comment_index[user_id] += 1
   else:
       print("You need to be registered first, type /start")


def send_bad_comment(user, comment_index):
    comments = Comments('lJYn09tuPw4')
    bad_comments = comments.find_bad_comments()

    if bad_comments and comment_index < len(bad_comments):
        comment = bad_comments[comment_index]
        message = f"A bad comment was found:\n\n {comment[1]}.\n Click the link to respond: {build_url(comment[3], comment[4])}"
        bot.send_message(chat_id=user.chat_id, text=message)
    else:
        bot.send_message(chat_id=user.chat_id, text="No more bad comments to respond to for now.")

def build_url(video_id, comment_id):
    return f'https://www.youtube.com/watch?v={video_id}&lc={comment_id}'

bot.polling()
