import requests
import vk_api

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent

"""++====-----------==--------=-------+--- ------------   ------- -- ---   -
| Это класс настроек
|
|
\==---=-------------+------------- -------  ----   -   -"""


class Settings:

    # Айди группы
    group_id =

    # Логинимся в вк
    session = requests.Session()
    vk_session = vk_api.VkApi(token='ТУТ ТОКЕН ГРУППЫ')
    longpoll = VkBotLongPoll(vk_session, group_id)
    vk = vk_session.get_api()

    # Настройки
    prefix = '!'
    reference = (f'public{group_id}', f'club{group_id}')

    # Список слов, за которые нужно наказывать. Сейчас тут только мат
    SUKABLYAT = ['хуй', 'бля', 'ебанный', 'ебаный', 'блять', 'блядь',
                 'пизда', 'ебать', 'сука', 'пидарас', 'хуйло', 'хуйня',
                 'чмо', 'пиздабол', 'охуеть', 'пиздато', 'хуйхуй']
