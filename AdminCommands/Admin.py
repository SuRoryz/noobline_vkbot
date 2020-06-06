from Sql import Sql
from Samples import Samples
from json import dumps, loads
from Settings import Settings
from RequestClass import Request

"""++====-----------==--------=-------+--- ------------   ------- -- ---   -
| Это класс команд, которые вызываются в процессе работы бота
|
|
|           Метод -> возвр. знач.            Краткое пояснение
|
\\=+-         onLeave -> tuple           Вызывает при выходе юзера
/
\\=+-         onBotJoin -> None         Вызывает при добавлении бота
/
\\=+-         onUserJoin -> str          Вызывает при заходе юзера
/
\\=+-        parseSUKABLYAT -> str           Пытается найти мат
/
\\=+-          warnUser -> str            Выдает пользователю варн
/
\\=+-         unwarnUser -> str            Задает кол-во варнов 0
/                                             для пользователя
|
\\=+-          kickUser -> None            Кикает пользователя из
/                                          беседы и снимает варны
|
\\=+-          addMoney -> None            Начисляет сумму денег.
/
\\=+-          getMoney -> int            Возвращает баланс юзера
/  
|
\==---=-------------+------------- -------  ----   -   -"""


class AdminCommands:

    # Вызывается при выходе пользователя.
    # Предлагает кикнуть вышедшего.
    # В ответе дает кортеж с сообщением и словарем клавиатуры
    @staticmethod
    def onLeave(request: Request) -> tuple:
        target: int = request.event.object['action']['member_id']
        message: str = Samples.EVENT_ON_LEAVE.format(Samples.getReference(target, request.chat_id))
        keyboard: dict = dumps({'one_time': False,
                          'inline': True,
                          'buttons': [[{
                                      'action': {
                                            "type": "text",
                                            "label": "Кикнуть"},
                                      'color': 'secondary',
                                    }]]
                          })
        
        try:
            Sql.execute(f'update Admin set kick_queue={target}', request.chat_id)
        except:
            pass
        return {'message': message, 'keyboard': keyboard}

    # Вызывает при подключении бота к беседе
    @staticmethod
    def onBotJoin(request: Request) -> None:
        Sql.setUp(request.chat_id)

    # Вызывается при подключении пользователя.
    # Присылает заданное приветствие, либо приветствие по дефолту
    @staticmethod
    def onUserJoin(request: Request) -> str:
        return Sql.execute("select greeting from Admin", request.chat_id)[0][0]

    # Парсер слов, за которые наказывают
    # извините, но это верх моего комедийного искусства.
    @staticmethod
    def parseSUKABLYAT(request: Request) -> str:
        text: str = request.event.object.text.lower()
        text = text.split()

        if any(x in text for x in Settings.SUKABLYAT):
            return AdminCommands.warnUser(request, request.event.object.from_id, request.chat_id)

    # Выдает варн человеку. 3/3 = кик из беседы
    @staticmethod
    def warnUser(request: Request, target: int, chat_id: int) -> str:
        warn_dict: dict = loads(Sql.execute("select warns from Admin", chat_id)[0][0])
        target = str(target)

        if target in warn_dict['warns'].keys():
            warns_now = warn_dict['warns'][target]
            if warns_now == 2:
                AdminCommands.kickUser(request, int(target))
                AdminCommands.unwarnUser(request, int(target))
                warn_dict['warns'][target] += 1
            else:
                warn_dict['warns'][target] += 1
        else:
            warn_dict['warns'][target] = 1

        warns_now = warn_dict['warns'][target]
        warn_dict = dumps(warn_dict)
        if warns_now != 3:
            Sql.execute(f"update Admin set warns='{warn_dict}'", chat_id)
        return Samples.ADMIN_WARN.format(Samples.getReference(target, chat_id), warns_now)

    # Устанавливает количество варнов на 0
    @staticmethod
    def unwarnUser(request: Request, target: int) -> str:
        warn_dict: dict = loads(Sql.execute("select warns from Admin", request.chat_id)[0][0])
        target = str(target)

        warn_dict['warns'][target] = 0
        warn_dict = dumps(warn_dict)
        Sql.execute(f"update Admin set warns='{warn_dict}'", request.chat_id)
        return Samples.ADMIN_WARN_NULL.format(Samples.getReference(target, request.chat_id))

    # Кикает цель из беседы. Попутно снимает варны
    @staticmethod
    def kickUser(request: Request, target: int) -> None:
        Settings.vk.messages.removeChatUser(chat_id=request.event.chat_id,
                                        user_id=target,
                                        member_id=target)

        AdminCommands.unwarnUser(request, target)

    # РАЗДЕЛ ЭКОНОМИКИ - - - - - - - - - - - - -

    # Начисляет сумму. Если сумма отрицательная, то забирает.
    @staticmethod
    def addMoney(target, money: int, chat_id: int) -> None:
        Sql.execute(f"update Economy set money={money}+money where user={target}", chat_id)

    # Получает баланс пользователя
    @staticmethod
    def getMoney(target: int, chat_id: int) -> int:
        return Sql.execute(f"select money from Economy where user={target}", chat_id)[0][0]
        
        
