import vk_api

from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from AdminCommands.Admin import AdminCommands as AC

from time import time
from json import loads, dumps

class ChatBan(Command, Settings):

    key = ('бан', 'ban', 'банвремя', 'tempban')
    permissions = 8

    @classmethod
    def process(cls, request, target='', *args):

        target_ = cls.parseTargetFromFWDM(request)
        if target_:
            target = target_
            
        target = cls.parseTarget(target)

        if not(target):
            return Samples.COMMAND_INVALIDUSER
        if not(args):
            time_ = 9999999999999
        else:
            time_ = round(time()) + cls.parseTime(' '.join(args))
        
        from_id = request.event.object['from_id']

        @cls.checkForPermission(from_id, request.chat_id)
        def work(target):               
            try:
                if Permission.levels[cls.getRole(target, request.chat_id)[0]] >= Permission.levels[cls.getRole(from_id, request.chat_id)[0]]:
                    return Samples.ERR_COMMAND_BAN_DENIED
            except:
                pass
            try:
                AC.banUser(request, target, time_)
            except:
                return Samples.ERR_COMMAND_BAN_ERR

            return Samples.COMMAND_CHATBAN_SUCCESS

        return work(target)
