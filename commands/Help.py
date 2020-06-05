from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission

class Help(Command):

    key = 'помощь'
    permissions = 0

    @classmethod
    def process(cls, request, subcommand=''):
        from_id = request.event.object['from_id']

        if not(subcommand) or subcommand not in ['экономика', 'чат', 'игры']:
            return Samples.HELP_BASE

        @cls.checkForPermission(from_id, request.chat_id)
        def work():

                if subcommand == 'экономика':
                    return Samples.HELP_ECONOMY
                elif subcommand == 'чат':
                    return Samples.HELP_CHAT
                elif subcommand == 'игры':
                    return Samples.HELP_GAMES
                    
            
        return work()
