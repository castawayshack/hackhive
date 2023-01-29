import telebot
import os
from translate import Translator

API_KEY = os.environ['API_KEY']

# Define a function that will be run when the /start command is issued

bot = telebot.TeleBot(API_KEY)
translations = {
    "Information": {
        "en": "Information",
        "es": "Información",
        "fr": "Informations",
        "hi": "जानकारी"
    },
    "Register": {
        "en": "Register",
        "es": "Registro",
        "fr": "Inscription",
        "hi": "रजिस्टर करें"
    },
    "Resources": {
        "en": "Resources",
        "es": "Recursos",
        "fr": "Ressources",
        "hi": "संसाधन"
    }
    # add more options as needed
}


# Handle the '/start' command
@bot.message_handler(commands=['start'])
def handle_start(message):
    # Ask the user for their preferred language
    bot.send_message(message.chat.id, "Please select your preferred language:")
    bot.register_next_step_handler(message, handle_language)


def handle_language(message):
    source_language = message.text
    global lang
    lang = source_language
    # Translate the message to the user's language
    translator = Translator(to_lang=source_language)
    translated_text = translator.translate(
        "Welcome to the hackathon bot! Please select an option from the menu below:"
    )
    # Create a custom keyboard with menu options
    menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    menu_keyboard.row(translator.translate("Information"),
                      translator.translate("Register"))
    menu_keyboard.row(translator.translate("Resources"),
                      translator.translate("Contact"))
    # Send the message with the menu options
    bot.send_message(message.chat.id,
                     translated_text,
                     reply_markup=menu_keyboard)


def translate_text(text):
    #source_language = bot.user_preferred_language
    translator = Translator(to_lang=lang)
    return translator.translate(text)


# Handle the 'Information' option
@bot.message_handler(
    func=lambda message: message.text == translate_text("Information"))
def handle_information(message):
    source_language = message.from_user.language_code
    translator = Translator(to_lang=lang)
    translated_text1 = translator.translate(
        "This is the information about the hackathon event.Date, Venue, Prizes, Sponsors, etc."
    )
    bot.send_message(message.chat.id, translated_text1)


# Handle the 'Register' option
@bot.message_handler(func=lambda message: message.text == "Register" or message
                     .text == "S'inscrire" or message.text == "Inscription" or
                     message.text == "रजिस्टर करें")
def handle_register(message):
    source_language = message.from_user.language_code
    translator = Translator(to_lang=lang)
    translated_text = translator.translate(
        "Please click on the link to register for the event")
    bot.send_message(message.chat.id, translated_text)


# Handle the 'Resources' option
@bot.message_handler(
    func=lambda message: message.text == "Resources" or message.text ==
    "Recursos" or message.text == "Ressources" or message.text == "संसाधन")
def handle_resources(message):
    source_language = message.from_user.language_code
    translator = Translator(to_lang=lang)
    translated_text = translator.translate(
        "Here are some useful resources for the hackathon event")
    bot.send_message(message.chat.id, translated_text)


bot.polling()
