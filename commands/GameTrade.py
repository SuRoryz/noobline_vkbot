import vk_api

from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from AdminCommands.Admin import AdminCommands as AC

from json import loads, dumps
from random import randint

class GameTrade(Command, Settings):

    key = 'трейд'
    permissions = 3

    @classmethod
    def process(cls, request, money=''):

        from_id = request.event.object['from_id']

        if not(money):
            return Samples.GAME_TRADE_INFO

        try:
            money = abs(int(money))
        except:
            return Samples.GAME_ERR_INVALIDSUM

        @cls.checkForPermission(from_id, request.chat_id)
        def work(from_id):            

            if AC.getMoney(from_id, request.chat_id) < money:
                return Samples.ERR_NOMONEY
            
            trade_rate = Sql.execute("select trade_rate from Admin", request.chat_id)[0][0]
            new_rate = trade_rate * randint(105, 1995) / 1000
            q = round((1 - trade_rate / new_rate), 3)
            to_add = round(money * (q + 1) - money)
            AC.addMoney(from_id, to_add, request.chat_id)

            return Samples.GAME_TRADE_SUCCESS.format(q * 100, to_add)

        return work(from_id)
