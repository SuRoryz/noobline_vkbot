from Sql import Sql
from Samples import Samples
from json import dumps, loads
from Settings import Settings
from RequestClass import Request
from time import time

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
\\=+-        unwarnUser -> str             Задает кол-во варнов 0
/                                             для пользователя
|
\\=+-          banUser  -> None              Банит пользователя
/
\\=+-         unbanUser -> None          Разбванивает пользователя
/ 
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
        Sql.setUpUser(Settings.group_id, request.chat_id)

    # Вызывается при подключении пользователя.
    # Присылает заданное приветствие, либо приветствие по дефолту
    @staticmethod
    def onUserJoin(request: Request) -> str:
        if AdminCommands.getSettings(request, 'antiraid'):
            AdminCommands.kickUser(request, request.event.object.action['member_id'])
            return 'Пользователь исключен, потому что включен режим антирейд'
        return Sql.execute("select greeting from Admin", request.chat_id)[0][0]

    # Вызывается при каждом сообщении.
    # Выполняет проверки на настйроки и т.д.
    @staticmethod
    def onEveryMessage(request: Request) -> str:

        if not(Sql.execute("select admins from Admin", request.chat_id)):
            return            
        
        extra = loads(Sql.execute("select extra from Admin", request.chat_id)[0][0])

        try:
            from_id = request.event.object['action']['member_id']
        except:
            from_id = request.event.object['from_id']

        if 'bans' in extra['utils'].keys():
            now_banned = extra['utils']['bans'].copy()
            for banned in extra['utils']['bans']:
                if extra['utils']['bans'][banned] <= round(time()):
                    now_banned.pop(banned)
                    AdminCommands.unbanUser(request, banned)
            extra['utils']['bans'] = now_banned

            if str(from_id) in extra['utils']['bans'].keys():
                print(1)
                AdminCommands.kickUser(request, from_id)
                return Samples.CHAT_BANNEDJOIN

        if AdminCommands.getSettings(request, 'stats'):
            AdminCommands.countStat(request)

    # Получаем настройки беседы
    @staticmethod
    def getSettings(request: Request, setting=None, full=False):

        extra = loads(Sql.execute("select extra from Admin", request.chat_id)[0][0])
        
        if not('settings' in extra['utils'].keys()):
            settings = Settings.default_values
        elif len(extra['utils']['settings']) == len(Settings.default_values):
            settings = extra['utils']['settings']
        else:
            for setting in Settings.default_values.keys():
                try:
                    extra['utils']['settings'][setting]
                except:
                    extra['utils']['settings'][setting] = Settings.default_values[setting]

            settings = extra['utils']['settings']

        if full:
            return settings

        try:
            return settings[setting]
        except:
            return Settings.default_values[setting]

    # Выставляем настройки беседы
    def setSettings(request: Request, setting: str, value: bool) -> None:
        extra = loads(Sql.execute("select extra from Admin", request.chat_id)[0][0])

        settings = AdminCommands.getSettings(request, full=True)

        settings[setting] = value

        extra['utils']['settings'] = settings

        extra = dumps(extra)
        Sql.execute(f"update Admin set extra='{extra}'", request.chat_id)

    # Парсер слов, за которые наказывают
    # извините, но это верх моего комедийного искусства.
    @staticmethod
    def parseSUKABLYAT(request: Request) -> str:
        
        if AdminCommands.getSettings(request, 'sukablyat') or request.event.object.from_id in AdminCommands.getSettings(request, 'protected'):
            return
        
        text: str = request.event.object.text.lower()
        text = text.split()

        if any(x in text for x in Settings.SUKABLYAT):
            return AdminCommands.warnUser(request, request.event.object.from_id, request.chat_id)

    # Выдает варн человеку. 3/3 = кик из беседы
    @staticmethod
    def warnUser(request: Request, target: int, chat_id: int) -> str:
        warn_dict: dict = loads(Sql.execute("select warns from Admin", chat_id)[0][0])
        target = str(target)
        warn_limit = int(AdminCommands.getSettings(request, 'warns'))

        if target in warn_dict['warns'].keys():
            warns_now = warn_dict['warns'][target]
            if warns_now == warn_limit-1:
                AdminCommands.kickUser(request, int(target))
                AdminCommands.unwarnUser(request, int(target))
                warn_dict['warns'][target] += 1
            else:
                warn_dict['warns'][target] += 1
        else:
            warn_dict['warns'][target] = 1

        warns_now = warn_dict['warns'][target]
        warn_dict = dumps(warn_dict)
        if warns_now != warn_limit:
            Sql.execute(f"update Admin set warns='{warn_dict}'", chat_id)
        return Samples.ADMIN_WARN.format(Samples.getReference(target, chat_id), warns_now, warn_limit, warn_limit)

    # Устанавливает количество варнов на 0
    @staticmethod
    def unwarnUser(request: Request, target: int) -> str:
        warn_dict: dict = loads(Sql.execute("select warns from Admin", request.chat_id)[0][0])
        target = str(target)
        warn_limit = int(AdminCommands.getSettings(request, 'warns'))

        warn_dict['warns'][target] = 0
        warn_dict = dumps(warn_dict)
        Sql.execute(f"update Admin set warns='{warn_dict}'", request.chat_id)
        return Samples.ADMIN_WARN_NULL.format(Samples.getReference(target, request.chat_id), warn_limit, warn_limit)

    # Кикает цель из беседы. Попутно снимает варны
    @staticmethod
    def kickUser(request: Request, target: int) -> None:
        Settings.vk.messages.removeChatUser(chat_id=request.event.chat_id,
                                        user_id=target,
                                        member_id=target)

        AdminCommands.unwarnUser(request, target)

    # Банит пользователя
    @staticmethod
    def banUser(request: Request, target: int, time: int) -> None:
        extra = loads(Sql.execute("select extra from Admin", request.chat_id)[0][0])
        if 'bans' not in extra['utils']:
            ban_dict = {}
        else:
            ban_dict = extra['utils']['bans']

        ban_dict[str(target)] = time

        extra['utils']['bans'] = ban_dict
        extra = dumps(extra)

        AdminCommands.kickUser(request, target)

        Sql.execute(f"update Admin set extra='{extra}'", request.chat_id)

    # Разбанивает пользователя
    @staticmethod
    def unbanUser(request: Request, target: int) -> None:
        extra = loads(Sql.execute("select extra from Admin", request.chat_id)[0][0])
        if 'bans' not in extra['utils']:
            return

        now_banned = extra['utils']['bans'].copy()

        try:
            now_banned.pop(str(target))
        except:
            pass
        extra['utils']['bans'] = now_banned

        extra = dumps(extra)
        Sql.execute(f"update Admin set extra='{extra}'", request.chat_id)

    # Записываем статистку сообщения в общую
    @staticmethod
    def countStat(request: Request) -> None:

        stats = {
                'overall': {},
                'users': {}
                }

        default_user_stats = {
                            'messages': 0,
                            'words': 0,
                            'sukablyat': 0,
                            'chars': 0
                            }
        
        extra = loads(Sql.execute("select extra from Admin", request.chat_id)[0][0])

        from_id = request.event.object.from_id
        text = request.event.object.text

        if 'stats' not in extra['utils'].keys():
            
            _stats = default_user_stats

            _stats['messages'] += 1
            _stats['words'] += len(text.split())
            _stats['chars'] += len(text)
            _stats['sukablyat'] += len(
                    [word for word in [word in Settings.SUKABLYAT for word in text
                                            .replace('?', '')
                                            .replace('!', '')
                                            .replace('.', '')
                                            .replace(',', '')
                                            .split()] if word]
                                        )

            stats['users'][str(from_id)] = _stats

        else:
            stats = extra['utils']['stats']
            if str(from_id) not in stats['users'].keys():
                _stats = default_user_stats

                _stats['messages'] += 1
                _stats['words'] += len(text.split())
                _stats['chars'] += len(text)
                _stats['sukablyat'] += len(
                        [word for word in [word in Settings.SUKABLYAT for word in text
                                                .replace('?', '')
                                                .replace('!', '')
                                                .replace('.', '')
                                                .replace(',', '')
                                                .split()] if word]
                                            )

                stats['users'][str(from_id)] = _stats

            else:
                _stats = stats['users'][str(from_id)]

                _stats['messages'] += 1
                _stats['words'] += len(text.split())
                _stats['chars'] += len(text)
                _stats['sukablyat'] += len(
                        [word for word in [word in Settings.SUKABLYAT for word in text
                                                .replace('?', '')
                                                .replace('!', '')
                                                .replace('.', '')
                                                .replace(',', '')
                                                .split()] if word]
                                            )
                
            
        extra['utils']['stats'] = stats

        extra = dumps(extra)
        Sql.execute(f"update Admin set extra='{extra}'", request.chat_id)
    
    # РАЗДЕЛ ЭКОНОМИКИ - - - - - - - - - - - - -

    # Начисляет сумму. Если сумма отрицательная, то забирает.
    @staticmethod
    def addMoney(target, money: int, chat_id: int) -> None:
        Sql.execute(f"update Economy set money={money}+money where user={target}", chat_id)

    # Получает баланс пользователя
    @staticmethod
    def getMoney(target: int, chat_id: int) -> int:
        return Sql.execute(f"select money from Economy where user={target}", chat_id)[0][0]
        
        
