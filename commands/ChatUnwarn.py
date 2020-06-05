import vk_api

from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from AdminCommands.Admin import AdminCommands as AC

class ChatUnwarn(Command, Settings):
    
    key = 'анварн'
    permissions = 7

    @classmethod
    def process(cls, request, target=''):
        target_ = cls.parseTargetFromFWDM(request)
        if target_:
            target = target_

        target = cls.parseTarget(target)
        from_id = request.event.object['from_id']

        @cls.checkForPermission(from_id, request.chat_id)
        def work(target):
            if target:
                try:
                    return AC.unwarnUser(request, target)
                except:
                    return Samples.ERR_COMMAND_CHATUNWARN_ERR

            return Samples.COMMAND_INVALIDUSER

        return work(target)
