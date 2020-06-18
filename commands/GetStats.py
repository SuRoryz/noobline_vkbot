from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings

import requests
from time import time
from json import loads, dumps

class GetStats(Command):

    key = ('статистика', 'стата')
    permissions = 0

    @classmethod
    def process(cls, request):
        from_id = request.event.object['from_id']

        @cls.checkForPermission(from_id, request.chat_id)
        def work(from_id):
            extra = loads(Sql.execute("select extra from Admin", request.chat_id)[0][0])

            if 'stats' not in extra['utils'].keys():
                return Samples.ERR_GETSTATS_DISABLED
            else:
                messages = 0
                words = 0
                chars = 0
                sukablyat = 0

                stats = extra['utils']['stats']['users']

                print(stats)

                for user in stats:
                    messages += stats[user]['messages']
                    words += stats[user]['words']
                    chars += stats[user]['chars']
                    sukablyat += stats[user]['sukablyat']
                    
            return Samples.COMMAND_GETSTATS_STATS.format(stats[str(from_id)]["messages"], messages,
                                                        stats[str(from_id)]["words"], words,
                                                        stats[str(from_id)]["chars"], chars,
                                                        stats[str(from_id)]["sukablyat"], sukablyat)

        return work(from_id)

