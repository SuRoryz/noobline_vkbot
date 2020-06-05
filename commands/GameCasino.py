import vk_api

from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from AdminCommands.Admin import AdminCommands as AC

from json import loads, dumps
from random import choices

class GameCasino(Command, Settings):

    key = 'казино'
    permissions = 3

    @classmethod
    def process(cls, request, color='', money=''):

        from_id = request.event.object['from_id']

        if not(color):
            return Samples.GAME_CASINO_HELP

        try:
            color = color.lower()
        except:
            pass

        if color not in ['черное', 'чёрное', 'красное', 'зеленое', 'зелёное', 'голубое']:
            return Samples.GAME_CASINO_NOCOLOR

        try:
            money = abs(int(money))
        except:
            return Samples.GAME_ERR_INVALIDSUM

        @cls.checkForPermission(from_id, request.chat_id)
        def work(from_id):            

            if AC.getMoney(from_id, request.chat_id) < money:
                return Samples.GAME_ERR_NOMONEY
            
            result = choices(['к', 'ч', 'з', 'г'], [36, 36, 4, 1])[0]

            multi = {'к': 2,
                     'ч': 2,
                     'з': 10,
                     'г': 50}

            if result == 'ч':
                result = 'чёрное'
            elif result == 'к':
                result = 'красное'
            elif result == 'з':
                result = 'зелёное'
            elif result == 'г':
                result = 'голубое'

            if result[0].lower() == color[0].lower():
                AC.addMoney(from_id, money * multi[result[0].lower()], request.chat_id)
            else:
                AC.addMoney(from_id, -money, request.chat_id)

            return Samples.GAME_CASINO_SUCCESS.format(result, AC.getMoney(from_id, request.chat_id))

            
        return work(from_id)
