from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission

# Меняет ник

class AddNickname(Command):

    key = 'ник'
    permissions = 3

    @classmethod
    def process(cls, request, nickname):
        from_id = request.event.object['from_id']

        @cls.checkForPermission(from_id, request.chat_id)
        def work():
                Sql.execute(f'update Permissions set nickname="{nickname}" where user={from_id}', request.chat_id)
                return Samples.COMMAND_ADDNICKNAME_SUCCESS.format(nickname)

        return work()
