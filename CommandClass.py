from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from RequestClass import Request

import random
from json import loads

"""++====-----------==--------=-------+--- ------------   ------- -- ---   -
| Это класс, по которому строятся все комманды.
|
|
|           Метод -> возвр. знач.             Краткое пояснение
|
\\=+-          process -> str                   Сама комманда.
/
\\=+-        sendMessage -> str              Отправляет сообщения.
/                                           Используется только для
|                                           промежуточных отправок.
|
\\=+-     checkForPermission -> func        Декоратор для функции
/                                                  process.
|                                           Проверяет человека на
|                                         право использовать комманду.
|
\\=+-         isAdmin -> bool                      isAdmin?
/
\\=+-     parseTargetFromFWDM -> str      Получает айди пользователя
/                                         по пересланному сообщению.
|
\\=+-        parseTarget -> int           Получает айди пользователя
/                                           из говна, что ему дали.
|
\\=+-      timeDifference -> int         Возвращает форматированую
/                                             разницу во времени
|
\\=+-        parseTime -> str           Возвращает секунды из времени,
/                                                что ему дали.
|
\\=+-        getRole -> tuple              Получает префикс и роль
/                                                  по айди.
|
\==---=-------------+------------- -------  ----   -   -"""

class Command:

    # Вызывающая команда
    key = ''
    # Уровень доступа
    permissions = 0

    # Эту функцию реализуют объекты класса.
    # Вызывается, если команда совпала с ключом
    # Возвращает текст-ответ
    def process(self) -> str:
        pass

    # Только для промежуточной отправки сообщений. Для готовых результатов
    # нужно возвращать их значение
    @classmethod
    def sendMessage(cls, message:str, chat_id:int,
                    keyboard:dict={}, attachment:str='') -> None:
        print(type(chat_id))
        Settings.vk.messages.send(
                                chat_id=chat_id,
                                message=message,
                                random_id=random.randint(1, 600000),
                                keyboard=keyboard,
                                attachment=attachment
                                )

    # Декоратор, которым оборачивается функция process
    # Проверяет права пользователя на использование команды
    @classmethod
    def checkForPermission(cls, target: int, chat_id: int):
        def wrap(function):
            def wrap_args(*args):
                role: str = Sql.execute(f"select role from Permissions where user={target}", chat_id)[0][0]

                try:
                    if not(Permission.levels[role] < cls.permissions) or cls.isAdmin(target, chat_id):
                        return function(*args)
                    return Samples.ERR_PERMS_DENIED
                except Exception as e:
                    return Samples.ERR_UNKNOWN

            return wrap_args
        return wrap

    # Проверка на админа беседы
    @classmethod
    def isAdmin(cls, target: int, chat_id: int) -> bool:
        admin: dict = loads(Sql.execute("select admins from Admin", chat_id)[0][0])
        if int(target) in admin['admins']:
            return True

        return False

    # Пытаемся получить цель по пересланному сообщению
    @classmethod
    def parseTargetFromFWDM(cls, request: Request) -> str:
        if request.event.object['fwd_messages']:
            return str(request.event.object['fwd_messages'][0]['from_id'])

    # Пытаемся определить цель из обращения/screen_name/другой поеботы
    @classmethod
    def parseTarget(cls, target: str) -> int:
        if 'id' in target:
            target: str = target[1:target.index('|')].replace('id', '')

            try:
                return int(target)
            except:
                return target

        target: str = target.replace('@', '')

        try:
            response: dict = Settings.vk.utils.resolveScreenName(screen_name=target)
            return int(response['object_id'])
        except:
            try:
                return int(target)
            except:
                return target

    # Разница во временеи
    @classmethod
    def timeDifference(cls, time1: int, time2: int) -> str:
        difference = abs(time2-time1)

        d = difference // 86400
        h = (difference % 86400) // 3600
        m = (difference % 86400 % 3600) // 60
        s = difference % 86400 % 3600 % 60

        if m<10:
            m='0'+str(m)
        else:
            m=str(m)
        if s<10:
            s='0'+str(s)
        else:
            s=str(s)
        return f'{d}д:{h}ч:{m}м:{s}с'

        
    # Перевод из формата d h m s в количество секунд
    @classmethod
    def parseTime(cls, time: str) -> int:
        time = time.lower().split()
        params = {'d': 86400, 'д': 86400,
                  'h': 3600, 'ч': 3600,
                  'm': 60, 'м': 60,
                  's': 1, 'с': 60}

        total = 0

        for arg in time:
            for param in params.keys():
                if param in arg:
                    need = arg.replace(param, '')
                    if not(need):
                        need = 0
                    total += params[param] * int(need)

        return total
        

    # Получаем роль и префикс цели.
    @classmethod
    def getRole(cls, target: int, chat_id: int) -> tuple:
        prefix, role = '', ''
        
        try:
            prefix = Sql.execute(f"select prefix from Permissions where user={target}", chat_id)[0][0]
            role = Sql.execute(f"select role from Permissions where user={target}", chat_id)[0][0]
        except:
            pass

        return role, prefix
