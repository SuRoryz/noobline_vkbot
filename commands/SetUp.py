from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission

class SetUp(Command):

    key = ('обновить',)
    permissions = 0

    @classmethod
    def process(cls, request):

        from_id = request.event.object['from_id']

        @cls.checkForPermission(from_id, request.chat_id)
        def work():
                
                Sql.setAdmin(request) 

                return Samples.COMMAND_SETUP_SUCCESS

        return work()
