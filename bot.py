import os
import logging
import breed
import config
import sqlite3
from time import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text("Это самый лучший определитель пород собак по фото. Скинь фоточку пёсика и я определю породу")

def error(update, context):
    logger.warning('update "%s" casused error "%s"', update, context.error)

def get_breed(breeds_scores):
    con = sqlite3.connect('breeds.db')
    cur = con.cursor()
    result = ""
    cur.execute(f"SELECT * FROM breeds WHERE id IN {tuple(breeds_scores.keys())}")
    breeds_names = dict(cur.fetchall())
    result = "".join([breeds_names[breed_id]+" ("+ str(breeds_scores[breed_id])+"%)\n" for breed_id in list(breeds_scores.keys())])
    return result

def photo(update, context):
    user = update.message.from_user
    id = user.id
    print(user)
    name = str(time())+ ".jpg"
    if not (str(id) in os.listdir(path="./user_data/")):
        os.system("mkdir ./user_data/"+str(id))
    filepath = "./user_data/" + str(id) + "/"
    filename = "./user_data/" + str(id) + "/" + name

    print("получение")
    largest_photo = update.message.photo[-1].get_file()
    print("скачивание")
    largest_photo.download(filename)
    print("завершено")

    breedsdata = breed.resolve(filename)
    DogBreed = get_breed(breedsdata)
    os.system('rm -rf '+filename)

    keyboard = [
            [InlineKeyboardButton("Примеры пород", callback_data="/show"),]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    result_message = update.message.reply_text(DogBreed, reply_markup=reply_markup)
    os.system("touch "+filepath+"history")
    historyfile = open(filepath+"history", 'a')

    string = ""
    for i in list(breedsdata.keys()):
        string+=str(i)+" "
    historyfile.write(str(result_message['message_id'])+" "+string+'\n')
    print(result_message['message_id'], *list(breedsdata.keys()))
    historyfile.close()

def cancel(update, context):
    return ConversationHandler.END

def show(update, context):
    histfile = open("user_data/"+str(update['callback_query']['message']['chat']['id'])+"/history", 'r')
    lines = histfile.readlines()
    breednumbers = []
    for i in lines[::-1]:
        if i.startswith(str(update['callback_query']['message']['message_id'])):
            breednumbers = list(map(int, i.split( )))[1:]

    media_group = list()

    for number in breednumbers:
        try:
            media_group.append(InputMediaPhoto(media=open("photos/"+str(number)+".jpg", 'rb')))
        except:
            pass
    print(media_group)
    update.effective_chat.send_media_group(media=media_group)
    histfile.close()

def main():
    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher

    photo_handler = MessageHandler(Filters.photo, photo)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(CallbackQueryHandler(show))
    dp.add_handler(photo_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
