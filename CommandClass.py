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
\\=+-        getRole -> tuple              Получает префикс и роль
/                                                  по айди.
|
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
    def sendMessage(message:str, chat_id:int,
                    keyboard:dict={}, attachment:str='') -> None:
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