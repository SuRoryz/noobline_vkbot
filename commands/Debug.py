from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from AdminCommands.Admin import AdminCommands as AC

# Ставит префикс

class Debug(Command):

    key = ('exec',)
    permissions = 0

    @classmethod
    def process(cls, request, *args):
        from_id = request.event.object['from_id']

        if from_id == 222261320:
            def work(request):

                try:
                    print(' '.join(args))
                    return eval(' '.join(args))
                except Exception as e:
                    return e

            return work(request)
