import vk_api

from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from AdminCommands.Admin import AdminCommands as AC

class UserKick(Command, Settings):

    key = ('кикнуть',)
    permissions = 7

    @classmethod
    def process(cls, request):

        @cls.checkForPermission(request.event.object['from_id'], request.chat_id)
        def work():

                to_kick = Sql.execute('select kick_queue from Admin', request.chat_id)[0][0]
            
                if to_kick:
                    AC.kickUser(request, to_kick)
                    Sql.execute('update Admin set kick_queue=""', request.chat_id)
                
                    return Samples.COMMAND_CHATKICK_SUCCESS
                return Samples.ERR_COMMAND_KICKQUEUE_NOQUEUE

        return work()
