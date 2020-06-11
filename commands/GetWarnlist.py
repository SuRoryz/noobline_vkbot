from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from time import time
from json import loads, dumps

class GetWarnlist(Command):

    key = ('варнлист', 'списокпредов', 'варны', 'warns', 'warnlist')
    permissions = 0

    @classmethod
    def process(cls, request):
        from_id = request.event.object['from_id']

        @cls.checkForPermission(from_id, request.chat_id)
        def work():
            warns = loads(Sql.execute("select warns from Admin", request.chat_id)[0][0])

            warns_dict = warns['warns']

            if not(warns_dict):
                return Samples.COMMAND_WARNLIST_NOWARNED

            message = Samples.COMMAND_WARNLIST_START

            for warn in warns_dict.keys():
                if warns_dict[warn] == 0:
                    continue
                message += Samples.COMMAND_WARNLIST_WARNS.format(Samples.getReference(warn, request.chat_id),
                                                 warns_dict[warn])

            return message
            
        return work()
