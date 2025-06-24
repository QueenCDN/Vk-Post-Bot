import vk_api

BOT_TOKEN = "YOUR TG-TOKEN" #токен для телеграм бота
VK_LOGIN = "PHONE NUMBER" #логин от страницы Вконтакте
VK_PASSWORD = "PASSWORD" #пароль от страницы Вконтакте
VK_ACCESS_TOKEN = "VK ACCESS TOKEN" #access токен от страницы Вконтакте
vk = vk_api.VkApi(token=VK_ACCESS_TOKEN, scope='offline').get_api()

#ID групп вконтакте (тут может быть несколько переменных)
ID_GROUP_TEST = "-" + str(vk.groups.getById(group_id = 'VK_GROUP_ID')[0]['id'])
ID_GROUP_TEST_1 = "-" + str(vk.groups.getById(group_id = 'VK_GROUP_ID_1')[0]['id'])