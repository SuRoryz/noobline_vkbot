from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission

class GetRoles(Command):

    key = ('роли', 'roles')
    permissions = 0

    @classmethod
    def process(cls, request):
        from_id = request.event.object['from_id']

        @cls.checkForPermission(from_id, request.chat_id)
        def work():
                message = 'Роль | Уровень\n'
                for role in Permission.levels.keys():
                    message += f'\n[{role}] - {Permission.levels[role]}'

                return message
            
        return work()
