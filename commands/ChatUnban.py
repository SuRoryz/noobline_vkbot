import vk_api

from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from AdminCommands.Admin import AdminCommands as AC

class ChatUnban(Command, Settings):
    
    key = ('анбан', 'разбан', 'unban')
    permissions = 7

    @classmethod
    def process(cls, request, target=''):
        target_ = cls.parseTargetFromFWDM(request)
        if target_:
            target = target_

        target = cls.parseTarget(target)
        from_id = request.event.object['from_id']

        print(target)

        @cls.checkForPermission(from_id, request.chat_id)
        def work(target):
            if target:
                try:
                    AC.unbanUser(request, target)
                    return Samples.CHAT_UNBAN_SUCCESS
                except:
                    return Samples.ERR_COMMAND_CHATUNBAN_ERR

            return Samples.COMMAND_INVALIDUSER

        return work(target)
