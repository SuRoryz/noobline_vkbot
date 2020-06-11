from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings

class GetOnline(Command):

    key = ('онлайн', 'online')
    permissions = 0

    @classmethod
    def process(cls, request):
        from_id = request.event.object['from_id']

        def makeReference(target, first_name, last_name):
            return f'[id{target}|{first_name} {last_name}]'

        @cls.checkForPermission(from_id, request.chat_id)
        def work():
                try:
                    res: dict = Settings.vk.messages.getConversationMembers(peer_id=request.event.obj.peer_id)
    
                    message = ''
                    counter = 0

                    for profile in res['profiles']:
                        if profile['online']:
                            counter += 1
                            message += Samples.COMMAND_ONLINE_USER.format(profile['first_name'], profile['last_name'],
                                Samples.COMMAND_ONLINE_MOBILE if 'is_mobile' in profile['online_info'].keys() else Samples.COMMAND_ONLINE_PC)

                    message = Samples.COMMAND_ONLINE_TOTAL.format(counter) + message
                except Exception as e:
                    message = e
                return message
            
        return work()
