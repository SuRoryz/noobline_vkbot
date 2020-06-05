from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from AdminCommands.Admin import AdminCommands as AC

class MoneyBalance(Command):

    key = 'баланс'
    permissions = 0

    @classmethod
    def process(cls, request, target=''):
        from_id = request.event.object['from_id']

        target_ = cls.parseTargetFromFWDM(request)
        if target_:
            target = target_

        if target:
            target = cls.parseTarget(target)

            if type(target) != int:
                return Samples.COMMAND_INVALIDUSER

        else:
            target = from_id

        print(target, AC.getMoney(target, request.chat_id))

        Sql.setUpUser(target, request.chat_id)

        @cls.checkForPermission(from_id, request.chat_id)
        def work(target):

            return Samples.COMMAND_MONEYBALANCE_SUCC.format(Samples.getReference(target, request.chat_id),
                                                            AC.getMoney(target, request.chat_id))

        return work(target)
