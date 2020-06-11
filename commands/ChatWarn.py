import vk_api

from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from AdminCommands.Admin import AdminCommands as AC

class ChatWarn(Command, Settings):

    key = ('варн', 'пред', 'warn')
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
                    if Permission.levels[cls.getRole(target, request.chat_id)[0]] >= Permission.levels[cls.getRole(from_id, request.chat_id)[0]]:
                        return Samples.ERR_COMMAND_WARN_DENIED
                except KeyError:
                    pass
                try:
                    return AC.warnUser(request, target, request.chat_id)
                except:
                    return Samples.ERR_COMMAND_WARN_ERR

            return Samples.COMMAND_INVALIDUSER


        return work(target)
