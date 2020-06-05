from Sql import Sql

"""++====-----------==--------=-------+--- ------------   ------- -- ---   -
| Это класс сэмплов с текстом и не только. В общем, отвечает за работу с текстом
|
|
|           Метод -> возвр. знач.            Краткое пояснение
|
\\=+-        getReference -> str            Получает упоминание
/                                              пользователя.
|
\\=+-        getPrefix -> str                  Gets prefix
/
|
\==---=-------------+------------- -------  ----   -   -"""


class Samples:

    HELP_BASE = ('Это страница помощи\n\nВ <> указаны обязательные аргументы '
                    'В [] указаны необязательные аргументы\n'
                    '\nУказать на пользователя (аргумент <кому>) '
                    'можно через @обращение или прикрепив '
                    'его сообщение\n\n'
                    'Разделы:\n!помощь экономика\n!помощь чат\n!помощь игры')

    HELP_ECONOMY = 'Команды экономики:\n!баланс\n!перевести <кому> <сумма>'

    HELP_GAMES = ('Игры:\n!кф (орёл и орешка против других участников беседы'
                            '\n📈 !трейд\n💰 !казино')

    HELP_CHAT = ('Команды чата:\n!приветствие <прикрепленное сообщение>'
                            '\n!правила [прикрепленное сообщение]'
                            '\n!варн <кому>\n!анварн <кому>'
                            '\n!кик <кому>'
                            '\n!онлайн'
                            '\n!ник <ник>'
                            '\n!префикс <префикс>')

    ERR_UNKNOWN = '❌ Произошла ошибка на сервере'
    
    ERR_PERMS_DENIED = '❌ У вас недостаточно прав'

    ERR_COMMAND_INVALIDARGUMENT = '❌ Введены неверные аргументы'

    ERR_COMMAND_UNKNOWN = '❌ Неизвестая команда'

    ERR_COMMAND_KICK_DENIED = '❌ Вы не можете кикнуть данного пользователя'

    ERR_COMMAND_WARN_DENIED = '❌ Вы не можете выдать варн данному пользователю'

    ERR_COMMAND_WARN_ERR =  '❌ Не удалось выдать варн данному пользователю'

    ERR_COMMAND_KICK_ERR = '❌ Не удалось кикнуть данного пользователя'

    ERR_COMMAND_CHATUNWARN_ERR = '❌ Не удалось снять варн данному пользователю'

    ERR_COMMAND_KICKQUEUE_NOQUEUE = '❌ Пока никто не выходил'

    ADMIN_WARN = 'У {} сейчас {}/3 варнов. За 3 варна бот кикает из беседы.'

    ADMIN_WARN_NULL = 'У {} сейчас 0/3 варнов. За 3 варна бот кикает из беседы.'

    EVENT_ON_LEAVE = '{} вышел из беседы. Хотите кикнуть?'

    COMMAND_ONLINE_MOBILE = '📱'

    COMMAND_ONLINE_PC = ''

    COMMAND_ONLINE_USER = '\n{} {}'

    COMMAND_ONLINE_TOTAL = '👥 Пользователей онлайн {}:\n'

    COMMAND_CHATKICK_SUCCESS = '✅ Пользователь кикнут из беседы'

    COMMAND_INVALIDUSER = '❌ Не удалось найти пользователя'

    COMMAND_ADDROLE_SUCCESS = '✅ Успешно установлена роль {} для {}'

    COMMAND_ADDROLE_INVALIDROLE = ('❌ Неверная роль. Чтобы узнать список доступных ролей,'
                                   ' используйте команду !роли')

    COMMAND_ADDROLE_GETROLE_PREFIX = '[{}] ({}) | {}'

    COMMAND_ADDROLE_GETROLE = '[{}] | {}'

    COMMAND_ADDNICKNAME_SUCCESS = '✅ Успешно установлен ник {}'

    COMMAND_ADDPREFIX_SUCCESS = '✅ Успешно установлен префикс {}'

    COMMAND_SETGREETING_SUCCESS = '✅ Приветствие установлено!'

    COMMAND_SETUP_SUCCESS = '✅ Список админов обновлён'

    COMMAND_MONEYBALANCE_SUCC = '💰 Баланс {}: {}  💲'

    COMMAND_MONEYTRANSFER_ERR_INVALIDMONEY = '❌ Сумма перевода должна быть целым числом'

    COMMAND_MONEYTRANSFER_ERR_NOMONEY = '❌ Недостаточно средств. Текущий баланс: [} 💲'

    COMMAND_MONEYTRANSFER_SUCCESS = '✅ Перевод проведен. Ваш баланс: {} 💲'

    GAME_ERR_NOMONEY = '❌ У вас недостаточно средств'

    GAME_ERR_INVALIDSUM = '❌ Сумма должна быть целым числом'

    GAME_CF_NOSUBCOMMAND = ('Доступные команды:'
                            '\n\n🔍 !кф поиск\n🆚 !кф орёл/решка '
                            '(после нахождения противника)')

    GAME_CF_ALREADYIN = '❗ Вы уже в игре'

    GAME_CF_STARTGAME = ('📢 Начинается игра в CoinFlip между {} и {}. '
                         'Первый, кто напишет !кф орёл/решка <сумма>, '
                         'начнёт игру.')

    GAME_CF_SEARCHSTARTED = '🔍 Ждём соперника'

    GAME_CF_EXIT = '❗ Вы вышли из игры'

    GAME_CF_ERR_NOSUM = ('Введите сумму, на которую будете играть. '
                        'Она спишется у проигравшего и добавится победителю')

    GAME_CF_ERR_NOSUMENEMY = '❌ У вашего соперника нет столько'

    GAME_CF_ERR_NOSUMME = '❌ У вас нет столько'

    GAME_CF_ERR_NOTINGAME = ('❌ Вы не в игре. Напишите !кф поиск, '
                             'чтобы начать поиск соперника из этой беседы')

    GAME_CF_WIN_O = '💰 Выпал орёл! Победитель {}'

    GAME_CF_WIN_R = '💰 Выпала решка! Победитель {}'

    GAME_TRADE_INFO = '📈 !трейд <сумма> - быстрый способ заработать'

    GAME_TRADE_SUCCESS = ('Трейд завершен.\nЦена изменилась на {}%.'
                        '\n💰 Ваша прибыль: {} 💲')

    GAME_CASINO_NOCOLOR = ('Доступно 4 ставки:\nЧёрное - x2'
                           '\nКрасное - x2\nЗелёное - x10\nГолубое - 50x')

    GAME_CASINO_SUCCESS = '💰 Выпало {}! Ваш баланс: {} 💲'

    GAME_CASINO_HELP = ('💰 !казино <ставка> <сумма>\n\nСтавки:\nКрасное - x2\n'
                        'Чёрное - x2\nЗелёное - x10\nГолубое - x50')

    # Получает упоминание пользователя используя его ник
    # *в дальнейшем будет еще и префикс, сейчас мне лень
    @staticmethod
    def getReference(target: int, chat_id: int) -> str:
        try:
            nickname = Sql.execute(f"select nickname from Permissions where user={target}", chat_id)[0][0]
        except:
            nickname = 'None'
        if nickname != 'None':
            return f'[id{target}|{nickname}]'
        else:
            return f'[id{target}|Пользователь]'

    # А вот и префиксы. Да, мне лень вызвать эту функцию в методе выше.
    @staticmethod
    def getPrefix(target: int, chat_id: int) -> str:
        try:
            prefix = Sql.execute(f"select prefix from Permissions where user={target}", chat_id)[0][0]
        except:
            return ''
        if prefix != 'None':
            return prefix
        return ''
        
