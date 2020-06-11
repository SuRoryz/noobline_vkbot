from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission

class SetRules(Command):

    key = ('правила', 'rules')
    permissions = 9

    @classmethod
    def process(cls, request):
        
        from_id = request.event.object['from_id']

        if not(request.event.object['fwd_messages']):
                    return Sql.execute("select rules from Admin", request.chat_id)[0][0]

        @cls.checkForPermission(from_id, request.chat_id)
        def work():

                Sql.execute(f"update Admin set rules='{request.event.object['fwd_messages'][0]['text']}'", request.chat_id)
    
                return Samples.COMMAND_SETGREETING_SUCCESS
            
        return work()
