from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from time import time
from json import loads, dumps

class GetBanlist(Command):

    key = ('банлист', 'списокбанов', 'banlist', 'баны', 'bans')
    permissions = 0

    @classmethod
    def process(cls, request):
        from_id = request.event.object['from_id']

        @cls.checkForPermission(from_id, request.chat_id)
        def work():
            extra = loads(Sql.execute("select extra from Admin", request.chat_id)[0][0])

            if 'bans' not in extra['utils']:
                return Samples.COMMAND_BANLIST_NOBANNED

            ban_dict = extra['utils']['bans']
            
            message = Samples.COMMAND_BANLIST_START

            for ban in ban_dict.keys():
                message += Samples.COMMAND_BANLISR_BANS.format(Samples.getReference(ban, request.chat_id),
                                             cls.timeDifference(round(time()), ban_dict[ban]))

            return message
            
        return work()
