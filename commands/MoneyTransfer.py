from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from AdminCommands.Admin import AdminCommands as AC

class MoneyTransfer(Command):

    key = 'перевести'
    permissions = 0

    @classmethod
    def process(cls, request, target, money=0):
        from_id = request.event.object['from_id']
        
        target_ = cls.parseTargetFromFWDM(request)
        if target_:
            money = target
            target = target_

        target = cls.parseTarget(target)

        if type(target) != int:
            return Samples.COMMAND_INVALIDUSER

        try:
            money = abs(int(money))
        except:
            return Samples.COMMAND_MONEYTRANSFER_ERR_INVALIDMONEY

        Sql.setUpUser(target, request.chat_id)

        @cls.checkForPermission(from_id, request.chat_id)
        def work(target, from_id):
            his_money = AC.getMoney(from_id, request.chat_id)
            if his_money < money:
                return Samples.COMMAND_MONEYTRANSFER_ERR_NOMONEY.format(his_money)
            AC.addMoney(from_id, money*-1, request.chat_id)
            AC.addMoney(target, money, request.chat_id)
            return Samples.COMMAND_MONEYTRANSFER_SUCCESS.format(his_money-money)

        return work(target, from_id)
