import os
import telebot
import datetime
import time
#import schedule
from telebot import types
from telebot.types import ReplyKeyboardMarkup
from pymongo import MongoClient
import bcrypt
#from bcrypt import hashpw, gensalt, checkpw
import json
#import requests
from threading import Timer
import telegram
#import telegram.ext
#from telegram.ext import Updater,CommandHandler


MONGO_URL = os.environ.get("MONGO_URL")
if not MONGO_URL:
    raise ValueError("MONGO_URL environment variable is not set")
client = MongoClient(MONGO_URL)
db = client.mydatabase
user_collection = db["login"]
API_KEY = os.environ['API_KEY']

# Define a function that will be run when the /start command is issued

bot = telebot.TeleBot(API_KEY)


# Hash a password using bcrypt
def hash_password(plain_password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


# Verify a password against its hashed version
def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'),
                          hashed_password.encode('utf-8'))


# Variables to store registration deadline and requirements
registration_deadline = "29.01.2022"
registration_requirements = ["Requirement 1", "Requirement 2", "Requirement 3"]

# List to store registered students
registered_students = []
chat_id = ""


# Handle '/start' command
@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("/start", "/hackathon_info", "/registration_info",
               "/registration", "/resources", "/register",
               "/More_about_Hackathon", "/reminderset", "/help",
               "/Change_language")
    bot.send_message(
        chat_id,
        "Hi! There. I am Habot-your guide for solving all of your hackathon queries. I can accept your registration, answer your questions, and show you tutorials as well as resources to help you on your hackathon journey. \n\nPlease select a command from the menu.",
        reply_markup=markup)
    bot.send_animation(
        chat_id, "https://media.giphy.com/media/idFxmiV2dayJEqzXaW/giphy.gif")


def information(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Hackathon Info", "Eligibility and Rules", "Exit")
    bot.send_message(chat_id, "Please select an option:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Hackathon Info")
def handle_hackathon_info(message):
    schedule = "Saturday, 9am-9pm: Hackathon\nSunday, 10am: Final presentations"
    location = "Online"
    rules = "1. Teams must have 1-5 members.\n2. All projects must be original and completed during the hackathon.\n3. No outside resources or assistance allowed."
    prizes = "1st Place: Winner Medal along with an E-certificate, for each member of the team\n2nd Place: 1st Runner-Up Medal along with an E-certificate, for each member of the team\n3rd Place: 2nd Runner-Up Medal along with an E-certificate, for each member of the team"

    bot.send_message(
        message.chat.id, "Schedule: \n" + schedule + "\n\nLocation: " +
        location + "\n\nRules: \n" + rules + "\n\nPrizes: \n" + prizes)


@bot.message_handler(
    func=lambda message: message.text == "Eligibility and Rules")
def handle_registration_info(message):
    deadline = "Registration deadline is on Friday, January 31st at 11:59 PM"
    requirements = "1. A completed registration form.\n2. A copy of your ID or passport.\n3. A CV or resume.\n4. A 500-word essay about your motivation to attend the event."

    bot.send_message(
        message.chat.id, "Registration deadline: " + deadline +
        "\n\nRequirements: \n" + requirements)


@bot.message_handler(func=lambda message: message.text == "Exit")
def handle_exit(message):
    bot.send_message(message.chat.id, "Returning to start menu.")


@bot.message_handler(commands=['Information'])
def handle_information(message):
    information(message)


'''
#to get info about registration
def hackathon_info(message):
    schedule = "Saturday, 9am-9pm: Hackathon\nSunday, 10am: Final presentations"
    location = "Online"
    rules = "1. Teams must have 1-5 members.\n2. All projects must be original and completed during the hackathon.\n3. No outside resources or assistance allowed."
    prizes = "1st Place: Winner Medal along with an E-certificate, for each member of the team\n2nd Place: 1st Runner-Up Medal along with an E-certificate, for each member of the team\n3rd Place: 2nd Runner-Up Medal along with an E-certificate, for each member of the team"

    bot.send_message(
        message.chat.id, "Schedule: \n" + schedule + "\n\nLocation: " +
        location + "\n\nRules: \n" + rules + "\n\nPrizes: \n" + prizes)


@bot.message_handler(commands=['hackathon_info'])
def handle_hackathon_info(message):
    hackathon_info(message)

'''


#deadline and Eligibility
def registration_info(message):
    deadline = "Registration deadline is on Friday, January 31st at 11:59 PM"
    requirements = "1. A completed registration form.\n2. A copy of your ID or passport.\n3. A CV or resume.\n4. A 500-word essay about your motivation to attend the event."

    bot.send_message(
        message.chat.id, "Registration deadline: " + deadline +
        "\n\nRequirements: \n" + requirements)


# to trigger the info fxn
@bot.message_handler(commands=['registration_info'])
def handle_registration_info(message):
    registration_info(message)


# Handle '/registration' command
@bot.message_handler(commands=['registration'])
def registration(message):
    bot.reply_to(
        message,
        f"The registration deadline is {registration_deadline}. Requirements: {', '.join(registration_requirements)}"
    )
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("/start", "/hackathon_info", "/registration_info",
               "/registration", "/resources", "/register", "/reminderset",
               "/help", "/change_language")
    bot.send_message(chat_id,
                     "Please select a command from the start menu.",
                     reply_markup=markup)


# Handle '/resources' command
#@bot.message_handler(commands=['resources'])
#def resources(message):
# bot.reply_to(
#    message,
#   f"Tutorials: {', '.join(tutorials)}. Sample projects: {', '.join(sample_projects)}"
#)
#chat_id = message.chat.id
#markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#markup.add("/start", "/registration", "/resources", "/register",
#          "/reminderset", "/help", "/Change_language")
#bot.send_message(chat_id,
#                "Please select a command from the start menu.",
#               reply_markup=markup)

# Variables to store resources
tutorials = [
    "Weather Telegram Bot using JavaScript: https://www.geeksforgeeks.org/how-to-design-a-weather-bot-in-telegram-using-javascript/",
    "Telegram Bot using Python: https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/ ",
    "Telegram Bot using Python with Payment and Database: https://medium.com/@tr_18329/build-a-telegram-bot-with-payments-and-a-database-from-a-z-8f54ee1e1ecf",
    "Build and Deploy in Solana: https://youtu.be/Mh_tvdkhJjA",
    "Using Replit Database for Node.js: https://youtu.be/vrEtQ3nEVAc"
]
sample_projects = [
    "Telegram Bot using Python: https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/ ",
    "Build and Deploy in Solana: https://youtu.be/Mh_tvdkhJjA",
    "Using Replit Database for Node.js: https://youtu.be/vrEtQ3nEVAc"
]


@bot.message_handler(commands=['resources'])
def resources(message):
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("All Tutorials", "Telegram Bot", "Solana", "Replit", "Exit")
    bot.send_message(chat_id, "Please select a topic:", reply_markup=markup)

    # Handle user's selection
    @bot.message_handler(func=lambda message: message.text in
                         ["All Tutorials", "Telegram Bot", "Solana", "Replit"])
    def handle_topic_selection(message):
        if message.text == "All Tutorials":
            bot.send_message(chat_id,
                             '\n'.join(["Available tutorials:"] + tutorials))
        elif message.text == "Telegram Bot":
            bot.send_message(
                chat_id,
                '\n'.join(["Available tutorials:"] + [sample_projects[0]]))
        elif message.text == "Solana":
            bot.send_message(
                chat_id,
                '\n'.join(["Available tutorials:"] + [sample_projects[1]]))
        elif message.text == "Replit":
            bot.send_message(
                chat_id,
                '\n'.join(["Available tutorials:"] + [sample_projects[2]]))

    @bot.message_handler(func=lambda message: message.text == "Exit")
    def exit_resources(message):
        start(message)


def share_links(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=
        "Here are some resources you might find helpful: \n1) Resources to make a conversational flow of bot: \n\ti) https://www.lucidchart.com/pages/ \n\tii) https://www.gliffy.com/ \n\tiii) https://www.smartdraw.com/ \n\t2) Resources to make a No-Code Job Board: \n\ti) https://youtu.be/7x-3DcPXrLU \n\tii) https://bubble.io/ \n\t3) Resources to make a No-Code Survey Bot: \n\ti) https://landbot.io/blog/how-to-collect-customer-feedback-with-chatbot-surveys \n\tii) https://landbot.io/ \n\t4) Resources to make a Low-Code Google Chrome Extension: \n\ti) https://youtu.be/NH52jzJg7SY \n\tii) https://flutterflow.io/ \n\t5) Resources to build a Telegram Bot with Python: \n\ti) https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/ \n\tii) https://www.geeksforgeeks.org/create-a-telegram-bot-using-python/ \n\t6) Resources to build a Telegram Bot with JavaScript: \n\ti) https://www.section.io/engineering-education/telegram-bot-in-nodejs/ \n\tii) https://www.geeksforgeeks.org/how-to-design-a-weather-bot-in-telegram-using-javascript/ \n"
    )


# Register
@bot.message_handler(commands=['register'])
def register(message):
    msg = bot.send_message(message.chat.id, [
        "Welcome to registration process! \nYou can type /cancel at any step to stop the process.\nEnter your username:"
    ])

    bot.register_next_step_handler(msg, register_username)


def register_username(message):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Registration cancelled.")
        return
    elif user_collection.find_one({"username": message.text}):
        msg = bot.send_message(
            message.chat.id,
            "Username already exists. Enter a different username:")
        bot.register_next_step_handler(msg, register_username)
    else:
        global username
        username = message.text
        msg = bot.send_message(message.chat.id, "Enter your email:")
        bot.register_next_step_handler(msg, register_email)


def register_email(message):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Registration cancelled.")
        return
    elif user_collection.find_one({"email": message.text}):
        msg = bot.send_message(
            message.chat.id, "Email already exists. Enter a different email:")
        bot.register_next_step_handler(msg, register_email)
    elif "@" not in message.text or ".com" not in message.text:
        msg = bot.send_message(message.chat.id,
                               "Invalid email. Enter a valid email:")
        bot.register_next_step_handler(msg, register_email)
    else:
        global email
        email = message.text
        msg = bot.send_message(message.chat.id, "Enter your password:")
        bot.register_next_step_handler(msg, register_password)


def register_password(message):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Registration cancelled.")
        return
    else:
        global password
        password = message.text
        hashed_password = bcrypt.hashpw(password.encode("utf-8"),
                                        bcrypt.gensalt())
        password = hashed_password
        msg = bot.send_message(message.chat.id,
                               "Enter your year of Graduation:")
        bot.register_next_step_handler(msg, register_grad_year)


def register_grad_year(message):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Registration cancelled.")
        return
    elif message.text not in ["2023", "2024", "2025", "2026"]:
        msg = bot.send_message(
            message.chat.id,
            "Invalid graduation year. Please enter a valid year:")
        bot.register_next_step_handler(msg, register_grad_year)
    else:
        global grad_year
        grad_year = message.text
        msg = bot.send_message(message.chat.id,
                               "Enter your branch of engineering:")
        bot.register_next_step_handler(msg, register_branch)


def register_branch(message):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Registration cancelled.")
        return
    else:
        global branch
        branch = message.text
        msg = bot.send_message(message.chat.id,
                               "Enter the name of your college:")
        bot.register_next_step_handler(msg, register_college)


def register_college(message):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "Registration cancelled.")
        return
    else:
        global college
        college = message.text
        user_collection.insert_one({
            "username": username,
            "email": email,
            "hashed_password": password,
            "grad_year": grad_year,
            "branch": branch,
            "college": college
        })
        bot.send_message(
            message.chat.id,
            "Registration successful! \nTime to gear up for the Hack!!")


# Dictionary to store scheduled reminders

# Handle '/reminders' command
#@bot.message_handler(commands=['reminders'])
#def reminders(message):
#    if message.from_user.username in registered_students:
#        bot.reply_to(
#          message,
#            "Reminder: The hackathon is coming up soon. Don't forget #to prepare and submit your project on time."
#        )
#        bot.reply_to(
#          message,
#          "Do you wish to receive the reminders on a specific time?"
#      )
#    else:
#        bot.reply_to(
#            message,
#            "You are not registered for the hackathon. Type 3/register to register."
#        )

""

# Load existing reminders from file
try:
    with open("reminders.json", "r") as f:
        reminders = json.load(f)
except:
    reminders = {}


@bot.message_handler(commands=['reminderset'])
def reminderset(message):
    bot.send_message(message.chat.id, "Do you want to set a reminder?")
    bot.register_next_step_handler(message, process_response)


def process_response(message):
    if message.text.lower() == "yes":
        bot.send_message(message.chat.id,
                         "What time do you want to be reminded?")
        bot.register_next_step_handler(message, process_time)
    elif message.text.lower() == "no":
        bot.send_message(message.chat.id, "Okay, no reminder set.")
    else:
        bot.send_message(message.chat.id, "Please respond with 'yes' or 'no'.")
        bot.register_next_step_handler(message, process_response)


def process_time(message):
    # Do something with the time, like setting a reminder
    bot.send_message(message.chat.id, "Reminder set for " + message.text)


bot.polling()
#def start(update, context):
#    context.bot.send_message(chat_id=update.effective_chat.id, #text="I'm a reminder bot. Use /setreminder to set a reminder.")


def set_reminder(update, context):
    # Get the message text and split it into the reminder time and message
    message_text = update.message.text.split(" ", 2)
    reminder_time = message_text[1]
    reminder_message = message_text[2]

    # Parse the reminder time and convert it to a timestamp
    reminder_time = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
    reminder_timestamp = int(time.mktime(reminder_time.timetuple()))

    # Add the reminder to the dictionary and save it to file
    user_id = update.message.from_user.id
    if user_id not in reminders:
        reminders[user_id] = []
    reminders[user_id].append({
        "timestamp": reminder_timestamp,
        "message": reminder_message
    })
    with open("reminders.json", "w") as f:
        json.dump(reminders, f)

    # Start a timer that will send the reminder message when the time comes
    reminder_timer = Timer(reminder_timestamp - time.time(),
                           send_reminder,
                           args=[user_id, reminder_message])
    reminder_timer.start()

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Reminder set for {reminder_time}.")


def send_reminder(user_id, message):
    # Send the reminder message to the user
    bot = telebot.TeleBot(API_KEY)
    bot.send_message(chat_id=user_id, text=message)

    # Remove the reminder from the dictionary and save it to file
    for reminder in reminders[user_id]:
        if reminder["message"] == message:
            reminders[user_id].remove(reminder)
            break
    with open("reminders.json", "w") as f:
        json.dump(reminders, f)


# Add handlers for the commands
start_handler = CommandHandler('start', start)
updater = Updater(API_KEY)  #, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)
reminder_handler = CommandHandler('setreminder', set_reminder)
dispatcher.add_handler(reminder_handler)

#change language

#@bot.message_handler(commands=['Change_language'])
#def Change_language(message):
# bot.send_message(message.chat.id, "Do you wish to switch to a different language?")
#bot.register_next_step_handler(message, process_response)

#def different_language(text, target_language):
#api_key = "YOUR_API_KEY"
#    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={text}&key={API_KEY}"
#   r = requests.get(url)
#  return r.json()[0][0][0]

#def chatbot_response(text, language):
#   if language == "en":
#      response = "Hello, how can I help you?"
# elif language == "fr":
#    response = "Bonjour, comment puis-je vous aider?"
#elif language == "es":
#   response = "Hola, ¿cómo puedo ayudarte?"
#else:
#        response = different_language("Hello, how can I help you?", #language)
#    return response

#text = "Bonjour"
#language = "fr"
#print(chatbot_response(text, language))

# List of available online study resources
resources = {
    'Solana': 'https://solana.com/learn/',
    'Filecoin': 'https://filecoin.io/learn/',
    'Replit': 'https://repl.it/learn/',
    'Other': 'https://www.google.com/search?q=online+study+resources'
}


@bot.message_handler(commands=['Learning_Resources'])
def Gather_resources(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "Awesome! We're here to help you out with gathering the resources you wish yo for the hackathon! Just select the one you wish to get started with"
    )


def study(update, context):
    topic = ' '.join(context.args)
    if topic in resources:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            f'Here\'s the link for learning about {topic}: {resources[topic]}')
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            f'Sorry, I don\'t have any resources for {topic}. Check out some general online study resources here: {resources["Other"]}'
        )


def Learning_Resources():
    updater = Updater(API_KEY)  #,use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    study_handler = CommandHandler('study', study)
    dispatcher.add_handler(study_handler)

    updater.start_polling()


'''
@bot.message_handler(commands=['resources'])
def share_links(message):
    bot.send_message(chat_id=message.chat.id, text='Here are some resources you might find helpful: \n1. https://example.com/resource1 \n2. https://example.com/resource2')

z
'''


# Handle '/help' command
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(
        message,
        "Commands:/start, /hackathon_info,/registration_info, /registration, /resources, /register, /More_about_Hackathon,/reminderset,/Change_language"
    )


rules = {'rules', 'Rules'}
coc = {'Code of Conduct', 'code of conduct', 'coc', 'COC'}
eli = {'eligibility criteria, Eligibility Criteria'}


#adwita working please cooperate
@bot.message_handler(commands=['More_about_Hackathon'])
def Rules_and_Coc_ig(context, update, user_msg):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        "Would you like to know about the hackathon? Well, we love your enthusiasm! What would you like to know about?"
    )
    chat_id = message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("Rules", "Code of Conduct", "Eligibility Criteria", "Exit")
    bot.send_message(chat_id, "Please select a topic:", reply_markup=markup)
    user_response = user_msg
    if (user_response != 'Exit'):
        if (user_response in rules):
            bot_resp = "Rules: \n\t1. The hackathon is open to all college students.\n\t2. Each team can have a maximum of 4 members \n\t3. The hackathon will be held on a designated date and time, and all participants must be present for the duration of the event.\n\t4. Each team must submit a working prototype or proof of concept of their hack by the end of the hackathon.\n\t5. The judges' decision is final and binding.\n\t6. Prizes will be awarded to the top teams as determined by the judges.\n\t7. The organizers reserve the right to modify the rules or code of conduct at any time without notice.\n\t8. All participants must respect the intellectual property rights of others.\n\t9. Each team has to submit their final code on Git or any other platform before the end of the hackathon.\n\t10. Plagiarism is not allowed and any team found guilty of plagiarism will be disqualified."
            return bot_resp
        elif (user_response in coc):
            bot_resp = "Code of Conduct:\n\t1. All participants must abide by the rules and regulations of the hackathon.\n\t2. All participants must respect the rights and dignity of others, including but not limited to, participants, staff, and judges.\n\t3. Discrimination, harassment, or any form of misconduct will not be tolerated. This includes but is not limited to, discrimination based on race, gender, sexual orientation, religion, national origin, age, or disability.\n\t4. All participants must refrain from cheating or any form of dishonesty.\n\t5. The use of drugs or alcohol during the hackathon is strictly prohibited.\n\t6. Participating in the hackathon grants the organizers the right to use their names and images for promotional purposes.\nThe above code of conduct must be followed at all costs. Any discrepancies would lead to being debarred from the hackathon."
            return bot_resp
        elif (user_response in eli):
            bot_resp = "The Eligibility criteria are as follows- Participants must be currently enrolled as full-time students in an accredited college or university and must have a valid ID or passport to verify their identity and age. Participants must also be present for the entire duration of the hackathon and must agree to abide by the hackathon's code of conduct and rules. It is also imperative that the participants have the necessary permissions from their respective college/university to participate in the event."
            return bot_resp
        else:
            user_response = user_response.lower()
            bot_resp = response(user_response)
            sent_tokens.remove(
                user_response
            )  # remove user question from sent_token that we added in sent_token in response() to find the Tf-Idf and cosine_similarity
            return "Could you repeat? I'm terribly confused"
    else:
        flag = False
        bot_resp = random.choice(bye)
        return bot_resp


        reply = make_reply(message)
        tbot.send_message(reply,from_)

# Start the bot
bot.polling()
start(bot.get_me())
