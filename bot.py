import os
import logging
import breed
import config
from time import time
import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler, Filters)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text("Это самый лучший определитель пород собак по фото. Скинь фоточку пёсика и я определю породу")

def error(update, context):
    logger.warning('update "%s" casused error "%s"', update, context.error)

def photo(update, context):
    user = update.message.from_user
    id = user.id
    print(user)
    name = str(time())+ ".jpg"
    if not (str(id) in os.listdir(path="./user_data/")):
        os.system("mkdir ./user_data/"+str(id))
    filepath = "./user_data/" + str(id) + "/" + name

    print("получение")
    largest_photo = update.message.photo[-1].get_file()
    print("скачивание")
    largest_photo.download(filepath)
    print("завершено")

    DogBreed = breed.resolve(filepath)
    os.system('rm -rf '+filepath)
    update.message.reply_text(DogBreed)

def cancel(update, context):
    return ConversationHandler.END

def main():
    updater = Updater(config.TOKEN, use_context=True)
    dp = updater.dispatcher

    photo_handler = MessageHandler(Filters.photo, photo)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(photo_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
