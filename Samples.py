

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

    HELP_BASE = ('🐝 Это страница помощи.\n\n🐔В <> указаны обязательные аргументы. '
                    '\nВ [] указаны необязательные аргументы\n'
                    '\n🐤 Указать на пользователя (аргумент <кому>) '
                    'можно через @обращение или прикрепив '
                    'его сообщение\n\n'
                    '🐧 Разделы:\n🐳 !Помощь экономика\n🐋 !Помощь чат\n🐬 !Помощь игры')

    HELP_ECONOMY = 'Команды экономики:\n💰 !Баланс\n💸 !Перевести <кому> <сумма>'

    HELP_GAMES = ('Игры:\n📢 !кф (орёл и орешка против других участников беседы)'
                            '\n📈 !трейд\n💰 !казино')

    HELP_CHAT = ('Команды чата:\n🔱 !Приветствие <прикрепленное сообщение>'
                            '\n🦊 !Правила [прикрепленное сообщение]'
                            '\n🆘 !Варн <кому>\n♻ !анварн <кому>'
                            '\n🚫 !Кик <кому>'
                            '\n !Бан <кому> [время (d, h, m, s)]'
                            '\n🐱 !Онлайн'
                            '\n👤 !Ник <ник>'
                            '\n👥 !Префикс <префикс>'
                            '\n !Настройки [имя] [значение]'
                            '\n !Варнлист'
                            '\n !Банлист')

    SETTINGS_CURRENT = 'Текущие настройки для беседы:\n' # NEW

    SETTINGS_NOPARAM = 'Данного параметра не существует' # NEW

    SETTINGS_SUCCESS = 'Для параметра {} успешно установлено значение: {}' # NEW

    SETTINGS_SET = 'Для параметра {} сейчас установлено значение: {}' # NEW

    CHAT_BANNEDJOIN = 'Забаненный пользователь попытался зайти и был кикнут.' # NEW

    ERR_UNKNOWN = '❌ Произошла ошибка на сервере'
    
    ERR_PERMS_DENIED = '❌ У вас недостаточно прав'

    ERR_CHAT_GAMESOFF = 'В данной беседе игры отключены' # NEW

    ERR_COMMAND_INVALIDARGUMENT = '❌ Введены неверные аргументы'

    ERR_COMMAND_UNKNOWN = '❌ Неизвестая команда'

    ERR_COMMAND_WARN_DENIED = '❌ Вы не можете выдать варн данному пользователю'

    ERR_COMMAND_WARN_ERR =  '❌ Не удалось выдать варн данному пользователю'

    ERR_COMMAND_KICK_DENIED = '❌ Вы не можете кикнуть данного пользователя'

    ERR_COMMAND_KICK_ERR = '❌ Не удалось кикнуть данного пользователя'

    ERR_COMMAND_BAN_DENIED = '❌ Вы не можете кикнуть данного пользователя'

    ERR_COMMAND_BAN_ERR = '❌ Не удалось кикнуть данного пользователя'

    ERR_COMMAND_CHATUNWARN_ERR = '❌ Не удалось снять варн данному пользователю'

    ERR_COMMAND_CHATUNBAN_ERR = '❌ Не разбанить данного пользователя'

    ERR_COMMAND_KICKQUEUE_NOQUEUE = '❌ Пока никто не выходил'

    ERR_GETSTATS_DISABLED = 'В данной беседе выключен сбор статистики. Включить его можно командой "!настройки статистика вкл"'

    ADMIN_WARN = '💋 У {} сейчас {}/{} варнов. За {} варна(-ов) бот кикает из беседы.'

    ADMIN_WARN_NULL = '💋 У {} сейчас 0/{} варнов. За {} варн(-ов) бот кикает из беседы.'

    EVENT_ON_LEAVE = '💔 {} вышел из беседы. Хотите кикнуть?'

    COMMAND_GETSTATS_STATS = ('Ваша статистика/общая:'
                            '\n Сообщений: {}/{}'
                            '\n Слов: {}/{}'
                            '\n Символов: {}/{}'
                            '\n Мата: {}/{}'
                    		) 

    COMMAND_GETTOP_PRESTART = 'Начинаю считать топ. Это может занять время.'

    COMMAND_GETTOP_TOP = '\n{}. {}: {}$ | {}'

    COMMAND_GETTOP_START = 'Топ по деньгам среди бесед:'

    COMMAND_BANLIST_NOBANNED = 'Забаненных пользователей нет.' # NEW

    COMMAND_BANLIST_START = 'Баны:' # NEW

    COMMAND_BANLIST_BANS = '\n{}: До разбана {}' # NEW

    COMMAND_WARNLIST_NOWARNED = 'Варнов пока нет.' # NEW

    COMMAND_WARNLIST_START = 'Варны:' # NEW

    COMMAND_WARNLIST_WARNS = '\n{}: {} варн(-ов)' # NEW

    COMMAND_ONLINE_MOBILE = '📱'

    COMMAND_ONLINE_PC = '🖥'

    COMMAND_ONLINE_USER = '\n🕶 {} {}'

    COMMAND_ONLINE_TOTAL = '👥 Пользователей онлайн {}:\n'

    COMMAND_INVALIDUSER = '❌ Не удалось найти пользователя'

    COMMAND_CHATKICK_SUCCESS = '✅ Пользователь кикнут из беседы'

    COMMAND_CHATBAN_SUCCESS = '✅ Пользователь кикнут из беседы'

    COMMAND_CHATUNBAN_SUCCESS = 'Пользователь разбанен' # NEW

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

    COMMAND_MONEYTRANSFER_ERR_NOMONEY = '❌ Недостаточно средств. Текущий баланс: {} 💲'

    COMMAND_MONEYTRANSFER_SUCCESS = '✅ Перевод проведен. Ваш баланс: {} 💸'

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

    GAME_CF_ERR_NOSUMENEMY = '❌ У Вашего соперника нет столько денег'

    GAME_CF_ERR_NOSUMME = '❌ У Вас нет столько денег'

    GAME_CF_ERR_NOTINGAME = ('❌ Вы не в игре. Напишите !кф поиск, '
                             'чтобы начать поиск соперника из этой беседы')

    GAME_CF_WIN_O = '💰 Выпал орёл! Победитель {}'

    GAME_CF_WIN_R = '💰 Выпала решка! Победитель {}'

    GAME_TRADE_INFO = '📈 !трейд <сумма> - быстрый способ заработать💸'

    GAME_TRADE_SUCCESS = ('Трейд завершен.\nЦена изменилась на {}%.'
                        '\n💰 Ваша прибыль: {} 💲')

    GAME_CASINO_NOCOLOR = ('Доступно 4 ставки:\n⚫ Чёрное - x2'
                           '\n🔴 Красное - x2\n🟢 Зелёное - x10\n🔵 Голубое - 50x')

    GAME_CASINO_SUCCESS = '💰 Выпало {}! Ваш баланс: {} 💲'

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
        
