import os
import logging
import breed
import config
from time import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler)

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text("Это самый лучший определитель пород собак по фото. Скинь фоточку пёсика и я определю породу")

def error(update, context):
    logger.warning('update "%s" casused error "%s"', update, context.error)

def get_breed(breeds):
    map_characters =["Аффенпинчер", "Афганская борзая", "Африканская охотничья собака", "Эрдельтерьер", "Американский стаффордширский терьер", "Аппенцеллер зенненхунд", "Австралийский терьер", "Басенджи", "Бассет-хаунд", "Бигль", "Бедлингтон-терьер", "Бернский зенненхунд", "Чёрно-подпалый кунхаунд", "Бленхеймский спаниель", "Бладхаунд",
                     "Енотовая гончая", "Бордер-колли", "Бордер терьер", "Борзая", "Бостон-терьер", "Фландрский бувье", "Немецкий боксёр", "Пти-брабансон", "Бриар", "Британский спаниель", "Бульмастиф", "Керн-терьер", "Вельш-корги кардиган", "Чесапик-бей-ретривер", "Чихуахуа",  "Чау-чау", "Кламбер-спаниель", "Английский кокер-спаниель", "Колли", "Курчавошёрстный ретривер", "Денди-динмонт-терьер",
                     "Красный волк", "Динго", "Доберман", "Английский фоксхаунд", "Английский сеттер", "Английский спрингер", "Энтлебухер зенненхунд",  "Американский эскимосский шпиц", "Прямошёрстный ретривер", "Французский бульдог", "Немецкая овчарка",  "Курцхаар", "Ризеншнауцер", "Золотистый ретривер",  "Шотландский сеттер",
                     "Немецкий дог", "Пиренейская горная собака", "Большой швейцарский зенненхунд", "Грюнендаль", "Поденко ибиценко", "Ирландский красный сеттер", "Ирландский терьер", "Ирландский водяной спаниель", "Ирландский волкодав", "Левретка", "Японский хин", "Вольфшпиц", "Австралийский келпи", "Керри-блю-терьер", "Комондор", "Кувас", "Лабрадор ретривер", "Лейкленд-терьер",
                     "Леонбергер", "Лхаса апсо", "Маламут", "Бельгийская овчарка", "Мальтийская болонка", "Ксолоитцкуинтли", "Карликовый пинчер", "Карликовый пудель", "Цвергшнауцер", "Ньюфаундленд", "Норфолк-терьер", "Норвежский элкхаунд", "Норвич-терьер", "Бобтейл", "Оттерхаунд", "Континентальный той-спаниель", "Пекинес", "Вельш-корги пемброк", "Померанский шпиц", "Мопс",
                     "Редбон кунхаунд", "Родезийский риджбек", "Ротвейлер", "Сенбернар", "Салюки", "Самоедская собака", "Шипперке",  "Скотч-терьер","Дирхаунд", "Силихем-терьер", "Шелти", "Ши-тцу", "Сибирский хаски",  "Австралийский шелковистый терьер", "Ирландский мягкошёрстный пшеничный терьер", "Стаффордширский бультерьер", "Пудель", "Миттельшнауцер",
                     "Суссекс-спаниель", "Тибетский мастиф", 'Тибетский терьер', 'Той-пудель', 'Русский той', 'Венгерская выжла', 'Древесная енотовая гончая Уолкера', 'Веймаранер', 'Вельш-спрингер-спаниель', 'Вест-хайленд-уайт-терьер', 'Уиппет', 'Жесткошёрстный фокстерьер', 'Йоркширский терьер']
    result = ""
    for i in list(breeds.keys()):
        result = result+map_characters[i]+" ("+ str(breeds[i])+"%)\n"
    return result

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

    DogBreed = get_breed(breed.resolve(filepath))
    os.system('rm -rf '+filepath)

    keyboard = [
            [InlineKeyboardButton("Примеры пород", callback_data="/show"),]
            ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    result_message = update.message.reply_text(DogBreed, reply_markup=reply_markup)
    print(result_message['message_id'])

def cancel(update, context):
    return ConversationHandler.END

def show(update, context):
    print(update['callback_query']['message']['message_id'])

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
