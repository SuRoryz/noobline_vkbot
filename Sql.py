from Settings import Settings
from json import loads, dumps
import sqlite3

"""++====-----------==--------=-------+--- ------------   ------- -- ---   -
| Это класс для работы с базой данных.
|
|
|           Метод -> возвр. знач.              Краткое пояснение
|
\\=+-         execute -> tuple               Выполянет SQL-query и
/                                              возвращает ответ
|
\\=+-         setAdmin -> None              Обновляет список админов
/
\\=+-         setUpUser -> None           Добавляет человека в таблицы,
/                                               если его там нет
|
\\=+-         setUp -> None               Создает таблицы из table_dict
/
|
\==---=-------------+------------- -------  ----   -   -"""


class Sql(Settings):

    """++====-----------==--------=-------+--- ------------   ------- -- ---   -
    | Немного проясним ситуацию
    |
    | table_dict - словарь таблиц формата:
    |        {Таблица: {колонка: (тип данных, значение по дефолту)}}
    |
    | *Значение по дефолту можно оставить пустым
    |
    | $user_id и подобные означает, что по дефолту нужно использовать
    | переменную, которой в момент определения словаря пока нет
    |
    | *Значения по дефолту в таблице Admin вручную заполняются ниже, а не тут.
    \==---=-------------+------------- -------  ----   -   -"""

    table_dict: dict = {'Economy': {'user': ('int', '$user_id'),
                              'money': ('int', 100)},
                  'Permissions': {'user': ('int', '$user_id'),
                                  'role': ('nvarchar(50)', '"Нуб"'),
                                  'prefix': ('nvarchar(50)', '"None"'),
                                  'nickname': ('nvarchar(50)', '"None"')},
                  'Admin': {'admins': ('ntext', '$admin_dict'),
                            'kick_queue': ('int', '0'),
                            'greeting': ('ntext', ''),
                            'rules': ('ntext', ''),
                            'warns': ('ntext', ''),
                            'trade_rate': ('float', '')},
                    'Games': {'coin_flip': ('ntext', '$game_cf_setup')}
                  }

    # Выполняем SQL-Query
    # Возвращает кортеж, полученный у fetchall()
    @staticmethod
    def execute(query: str, chat_id: int) -> tuple:
        result: tuple = None
        connection: 'Подключение' = sqlite3.connect(f'db/{chat_id}.db')
        cur: 'Курсор' = connection.cursor()
    
        try:
            cur.execute(query)
            result = cur.fetchall()

            connection.commit()
            connection.close()
        except OperationalError as e:
            return 'ERROR'
        except Exception as e:
            print( f'Some error: {type(e)}, {query}' )
        finally:
            if result:
                return result
            return None

    # Обновляет список админов беседы
    @classmethod
    def setAdmin(cls, request) -> None:
        res: dict = Settings.vk.messages.getConversationMembers(peer_id=request.event.obj.peer_id,fields='items')['items']
        admin_dict: dict = {"admins": []}
        
        for element in res:
                if not('is_admin' in element.keys()):
                    continue
                if element['is_admin']:
                    admin = element['member_id']
                    admin_dict['admins'].append(admin)
                    
        admin_dict = dumps(admin_dict)
        cls.execute(f"update Admin set admins='{admin_dict}'", request.chat_id)

    # Добавляет пользователя в таблицы
    # ВНИМАНИЕ! КОСТЫЛЬ!
    # тут мы единожды добавляем строку в Admin, потому что я не придумал
    # другой вариант. Тут натуральный костыль, который нужно провить.
    @classmethod
    def setUpUser(cls, user_id: int, chat_id: int):
        # Используется как дефолтное значение в таблицах
        # Потом сделаю нормально, щас пусть так будет
        admin_dict: dict = dumps({'admins': []})
        greetings: str = ('Привет!\nПохоже, приветсвие еще не задано.\n'
                    'Чтобы задать его, используйте команду !приветсвие с '
                    'прикрепленным сообщением, текст которого будет '
                    'задан как приветсвие.')
        rules: str = ('Привет!\nПохоже, правила еще не заданы.\n'
                      'Чтобы задать их, используйте команду !правила с '
                      'прикрепленным сообщением, текст которого будет '
                      'задан как правила.')
        warn_dict: dict = dumps({'warns': {}})

        # тут переменные для гамесов
        game_cf_setup = dumps({'in_search': None, 'games_now': []})

        # Проверка пользователя на предмет нахождения в таблице
        # *Проверяется по наличию в таблице Economy
        #  из-за чего при добавлении новых строк/таблиц придется удалять
        #  всю дб и система со словарем таблиц становится бесполезной.
        #  Цель: исправить, но потом
        def isExist(user_id: int) -> bool:
            if cls.execute(f''' SELECT count(user) FROM Economy WHERE user={user_id} ''', chat_id)[0][0]:
                return True
            return False

        if not(isExist(user_id)):
            for table in cls.table_dict.keys():
                
                # Тут большой Bruh  - - - - - - - - - - -
                
                if table == 'Admin':
                    if Sql.execute("select * from Admin", chat_id):
                        continue
                    Sql.execute(f"insert into Admin (admins, kick_queue, greeting, rules, warns, trade_rate) values ('{admin_dict}', 0, '{greetings}', '{rules}', '{warn_dict}', 1.0)", chat_id)
                    continue

                elif table == 'Games':
                    if Sql.execute("select * from Games", chat_id):
                        continue
                    Sql.execute(f"insert into Games (coin_flip) values ('{game_cf_setup}')", chat_id)
                    continue
                
                # - - - - - - - - - - - - - - - - - - - -
                
                columns: dict = cls.table_dict[table]
                columns_list: list = list()
                values_list: list = list()
                
                for column in columns.keys():
                    columns_list.append(column)

                    value = columns[column][1]
                    if Sql.isVar(value):
                        value = eval(value.replace('$', ''))
                    values_list.append(str(value))

                values = ', '.join(values_list)
                columns = ', '.join(columns_list)

                cls.execute(f''' INSERT INTO {table} ({columns}) VALUES ({values})''', chat_id)
            
    # Устновка бота. Создает таблицы и прочее.
    # При добавлении новых таблиц в tables_dict будет добавлять их при повторном вызове
    # не трогая остальные. Хорошая система, но ебучий isExist у setUpUser всё портит
    @classmethod
    def setUp(cls, chat_id: int) -> None:
        # Проверка на существование таблицы.
        def isExists(table: str) -> bool:
            if cls.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table}' ''', chat_id)[0][0]:
                return True
            return False

        for table in cls.table_dict.keys():
            if not(isExists(table)):
                
                columns = cls.table_dict[table]
                columns_list = list()
                
                for column in columns.keys():
                    columns_list.append(f'{column} {columns[column][0]}')
                columns = ', '.join(columns_list)
                    
                cls.execute(f''' CREATE TABLE {table} ({columns})''', chat_id)

    # Проверяет, переменная ли значение, которое по дефолту должно быть в таблице
    @staticmethod
    def isVar(value: str) -> bool:
        try:
            if '$' in str(value):
                return True
            return False
        except:
            return False
