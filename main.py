import os
import requests
import telebot
import vk_api
import config as cfg
import keyboards as kb
from telebot import types

bot = telebot.TeleBot(cfg.BOT_TOKEN, parse_mode='HTML')
vk = vk_api.VkApi(token=cfg.VK_ACCESS_TOKEN, scope='offline').get_api()


@bot.message_handler(commands=['start'])
def start(message):
    # Приветствующее сообщение
    name = message.from_user.first_name
    bot.send_message(message.chat.id, "Привет, {0}!\nЯ бот, раскидывающий ваш пост по группам Вконтакте.\nНажмите <a href=''>/создать</a>, чтобы создать пост.".format(name), reply_markup = kb.markup)


# Обработчик команды '/создать'
@bot.message_handler(commands=['создать'])
def raskid(message):
    # Отправляем запрос на описание товара
    bot.send_message(message.chat.id, "Введите описание товара:")
    bot.register_next_step_handler(message, ask_for_description)


def ask_for_description(message):
    # Получаем описание товара
    description = message.text
    # Запрашиваем фотографию товара
    bot.send_message(message.chat.id, "Пришлите фотографию товара:")
    bot.register_next_step_handler(message, check_description_and_photo, description)


def check_description_and_photo(message, description):
    # Проверяем, есть ли фотография в сообщении пользователя
    if message.photo:
        photo_id = message.photo[-1].file_id
        # Запрашиваем подтверждение описания и фотографии
        keyboard = types.InlineKeyboardMarkup()
        keyboard.row(types.InlineKeyboardButton("Раскидать ✅", callback_data='confirm'),
                     types.InlineKeyboardButton("Редактировать ✏️", callback_data='retry'))
        bot.send_photo(message.chat.id, photo_id, caption=f"<u><b>Описание:</b></u>\n{description}\n\n<em>Верно ли описание и фотография?</em>",
                       reply_markup=keyboard)
    else:
        # Если фотография не была отправлена, просим ее отправить заново
        bot.send_message(message.chat.id, "Вы не прислали фотографию. Пожалуйста, пришлите фотографию товара:")
        bot.register_next_step_handler(message, check_description_and_photo, description)


def raskid_in_group(photo_id, description):
    group_id = [cfg.ID_GROUP_1, cfg.ID_GROUP_2, cfg.ID_GROUP_3, cfg.ID_GROUP_4, cfg.ID_GROUP_5, cfg.ID_GROUP_6, cfg.ID_GROUP_7, cfg.ID_GROUP_8]

    file_photo = bot.get_file(photo_id)
    file_name, file_extension = os.path.splitext(file_photo.file_path)
    downloaded_file_photo = bot.download_file(file_photo.file_path)
    src = 'photos/' + photo_id + file_extension
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file_photo)
    
    for id_barah in group_id:
        upload_url =  vk.photos.getWallUploadServer(owner_id=id_barah)['upload_url']
        request = requests.post(upload_url, files = {'file': open(src, 'rb')})
        save_wall_photo = vk.photos.saveWallPhoto(owner_id = id_barah, photo = request.json()['photo'], server = request.json()['server'], hash = request.json()['hash'])
        saved_photo = "photo" + str(save_wall_photo[0]['owner_id']) + "_" + str(save_wall_photo[0]['id'])
        clean_description = description.replace('Описание:', '').replace('\nВерно ли описание и фотография?', '').strip()
        vk.wall.post(owner_id = id_barah, attachments = saved_photo, message = clean_description)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'confirm':
        # Выполняем функцию 'raskid_in_group()' с передачей photo_id и description
        chat_id = call.message.chat.id
        message_text = call.message.caption
        raskid_in_group(call.message.photo[-1].file_id, message_text)
        bot.send_message(chat_id, "<b>Ваш товар был успешно отправлен!</b>")

    elif call.data == 'retry':
        bot.send_message(call.message.chat.id, "Повторите ввод описания и фотографии:")
        bot.register_next_step_handler(call.message, ask_for_description)


bot.infinity_polling()