from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission

# Ставит префикс

class AddPrefix(Command):

    key = 'префикс'
    permissions = 5

    @classmethod
    def process(cls, request, prefix):
        from_id = request.event.object['from_id']

        @cls.checkForPermission(from_id, request.chat_id)
        def work():

                Sql.execute(f'update Permissions set prefix="{prefix}" where user={from_id}', request.chat_id)
                return Samples.COMMAND_ADDPREFIX_SUCCESS.format(prefix)

        return work()
