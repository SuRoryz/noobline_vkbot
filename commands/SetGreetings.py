from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission

class SetGreetings(Command):

    key = ('приветствие', 'greeting')
    permissions = 9

    @classmethod
    def process(cls, request):
        
        from_id = request.event.object['from_id']

        @cls.checkForPermission(from_id, request.chat_id)
        def work():
                Sql.execute(f"update Admin set greeting='{request.event.object['fwd_messages'][0]['text']}'", request.chat_id)
    
                return Samples.COMMAND_SETGREETING_SUCCESS
            
        return work()
