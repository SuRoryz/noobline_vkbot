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
    vk_session = vk_api.VkApi(token='токен')
    longpoll = VkBotLongPoll(vk_session, group_id)
    print(longpoll.ts)
    vk = vk_session.get_api()

    # Настройки
    prefix = '!'
    reference = (f'public{group_id}', f'club{group_id}')

    # Список слов, за которые нужно наказывать. Сейчас тут только мат
    SUKABLYAT = ['хуй', 'бля', 'ебанный', 'ебаный', 'блять', 'блядь',
                 'пизда', 'ебать', 'сука', 'пидарас', 'хуйло', 'хуйня',
                 'чмо', 'пиздабол', 'охуеть', 'пиздато', 'хуйхуй']

    default_values = {'sukablyat': False,
                      'games': True,
                      'protected': [],
                      'antiraid': False,
                      'warns': 3,
                      'stats': True
                      }

    settings_dict = {'sukablyat': 'Мат', 'мат': 'sukablyat',
                    'games': 'Игры', 'игры': 'games',
                     'antiraid': 'Антирейд', 'антирейд': 'antiraid',
                     'warns': 'Варны', 'варны': 'warns',
                     'stats': 'Статистика', 'статистика': 'stats'}

    values_dict = {True: 'Вкл', 'вкл': True,
                           False: 'Выкл', 'выкл': False}

    black_list = ['protected']

    

    
