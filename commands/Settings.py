import vk_api

from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from AdminCommands.Admin import AdminCommands as AC

from json import loads, dumps
from random import randint

class Settings(Command, Settings):

    key = ('настройки',)
    permissions = 9

    @classmethod
    def process(cls, request, setting=None, value=None):

        from_id = request.event.object['from_id']

        def parseSetting(setting, value=None):
            settings_dict = {'sukablyat': 'Мат', 'мат': 'sukablyat',
                              'games': 'Игры', 'игры': 'games',
                             }

            values_dict = {True: 'Вкл', 'вкл': True,
                           False: 'Выкл', 'выкл': False}

            black_list = ['protected']

            if setting in black_list:
                return '', ''
            
            try:
                setting = settings_dict[setting]
            except:
                pass

            try:
                value = values_dict[value]
            except:
                pass

            print(setting, value)

            return setting, value

        @cls.checkForPermission(from_id, request.chat_id)
        def work(setting, value):
            settings = AC.getSettings(request, full=True)

            if not(setting):
                message = Samples.SETTINGS_CURRENT

                for setting in settings:
                    setting_line = '\n{}: {}'.format(*parseSetting(setting, settings[setting]))
                    if setting_line != '\n: ':
                        message += setting_line

                return message

            if parseSetting(setting.lower())[0] not in settings.keys():
                return Samples.SETTINGS_NOPARAM

            if not(value):
                return Samples.SETTING_SET.format(*parseSetting(setting.lower(), settings[setting]))

            try:
                value = value.lower()
            except:
                pass
    
            AC.setSettings(request, *parseSetting(setting.lower(), value))
            return Samples.SETTINGS_SUCCESS.format(*parseSetting(setting.lower(), settings[setting]))

        return work(setting, value)
