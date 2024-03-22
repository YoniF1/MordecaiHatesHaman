from email import message
import os
from dotenv import load_dotenv
import telebot
import volunteers
import VolunteerManager

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.from_user.id)
    new_user = volunteers.MyVolonteer(user_id)
    doesExist = VolunteerManager.Manager.get_by_id(new_user)
    if len(doesExist) == 0 :
        new_user.save()
        bot.reply_to(message, "Welcome! You've been added to the volunteers list.")
        bot.reply_to(message, "Hello, this is your first message, let's fight against antisemitism!")
        bot.reply_to(message, "Here's the instruction for all volunteers that registered in our program:Our program automatically detects anti-Semitic comments of different YouTube videos and sends here links to the comments. Your task is to reply on every comment and to leave a link to our web-page. We need to convince those people to be on our side and fight with antisemitism together")
    else:
        print("You're already there")  

bot.polling() 

