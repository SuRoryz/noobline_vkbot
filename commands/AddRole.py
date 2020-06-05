from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission

class AddRole(Command):

    key = 'роль'
    permissions = 9

    @classmethod
    def process(cls, request, target='', role=''):
        from_id = request.event.object['from_id']
        
        if target in Permission.levels.keys():
            role = target

        target_ = cls.parseTargetFromFWDM(request)
        if target_:
            target = target_
        

        if not(target):
            role, prefix = cls.getRole(from_id, request.chat_id)

            if prefix and prefix != 'None':
                return Samples.COMMAND_ADDROLE_GETROLE_PREFIX.format(prefix, role, Samples.getReference(from_id, request.chat_id))
            return Samples.COMMAND_ADDROLE_GETROLE.format(role, Samples.getReference(from_id, request.chat_id))
        
        target = cls.parseTarget(target)

        if type(target) != int:
            return Samples.COMMAND_INVALIDUSER

        Sql.setUpUser(target, request.chat_id)

        if not(role):
            role, prefix = cls.getRole(target, request.chat_id)

            if prefix:
                return Samples.COMMAND_ADDROLE_GETROLE_PREFIX.format(prefix, role, Samples.getReference(target, request.chat_id))
            return Samples.COMMAND_ADDROLE_GETROLE.format(role, Samples.getReference(target, request.chat_id))

        @cls.checkForPermission(from_id, request.chat_id)
        def work(target):

                if role in Permission.levels.keys():
                    Sql.execute(f'update Permissions set role="{role}" where user="{target}"', request.chat_id)
                    return Samples.COMMAND_ADDROLE_SUCCESS.format(role, Samples.getReference(target, request.chat_id))

                return Samples.COMMAND_ADDROLE_INVALIDROLE

        return work(target)
