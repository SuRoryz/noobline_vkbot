import os
import importlib

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent
from Sql import Sql
from Settings import Settings
from AdminCommands.Admin import AdminCommands as AC
from Samples import Samples
from RequestClass import Request

"""++====-----------==--------=-------+--- ------------   ------- -- ---   -
| Это класс обработчика запросов.
|
|
|           Метод -> возвр. знач.            Краткое пояснение
|
\\=+-        isCommand -> bool                   isCommand?
/
\\=+-        curCommand -> str           Избавляет текст от префикса
/                                               или обращений
|
\\=+-       handleRequest -> str            Обрабатывает запрос
/                                        (принимает объект Request)
|
|
\==---=-------------+------------- -------  ----   -   -"""

class Handler(Settings):
    def __init__(self):

        modules: list = os.listdir('commands')
        self.commands: list = list()
        self._keys: dict = dict()

        # Подгрузка команд из папки commands. Костыль.
        for module in modules:
            module = module.replace('.py', '')
            
            if module == '__pycache__':
                continue
            
            exec(f"self.{module} = getattr(importlib.import_module(f'commands.{module}'), f'{module}')")
            self.commands.append(module)

            for command in self.commands:
                self._keys[eval(f'self.{command}.key')] = command
    
    # Проверка сообщения на команду
    def isCommand(self, content:str) -> bool:
        if content[:len(self.prefix)] == self.prefix:
            return True
        elif any(x in content.split()[0] for x in self.reference):
            return True
        
        return False

    # Избавляемся от обращений к боту и оставляем только запрос
    def cutCommand(self, content:str) -> str:
        if any(x in content.split()[0] for x in self.reference):
            content = content.split()
            del content[0]
            content = ' '.join(content)

        if content[:len(self.prefix)] == self.prefix:
            content = content.strip(self.prefix)

        return content

    def handleRequest(self, request: Request) -> str:
        if 'action' in request.event.object:

            # Выполняется на при добавлении в беседу - - - -
            
            if request.event.object['action']['type'] == 'chat_invite_user':
                if request.event.object['action']['member_id'] == -self.group_id:
                    AC.onBotJoin(request)
                    return 'После выдачи прав администратора боту, напишите !обновить'
                else:
                    return AC.onUserJoin(request)
                
            # - - - - - - - - - - - - - - - - - - - - - - - -


            # Выполняется при выходе||кике пользователя - - -
            
            elif request.event.object['action']['type'] == 'chat_kick_user':
                if request.event.object['action']['member_id'] == request.event.object['from_id']:
                    return AC.onLeave(request)

            # - - - - - - - - - - - - - - - - - - - - - - - -

        elif request.type == VkBotEventType.MESSAGE_NEW:

            # Пытаемся найти мат
            SUKABLYAT = AC.parseSUKABLYAT(request)
            if SUKABLYAT:
                return SUKABLYAT
            
            # Проверка на команду
            if self.isCommand(request.event.object['text']):
                Sql.setUpUser(request.event.object['from_id'], request.chat_id)

                message_content: str = self.cutCommand(request.event.object['text']).split()
                command: str = message_content.pop(0).lower()
                args: list = message_content
                
                try:
                    return eval("self.{}".format(self._keys[f'{command}'])).process(request, *args)
                except TypeError:
                    return Samples.ERR_COMMAND_INVALIDARGUMENT
                except KeyError as e:
                    return Samples.ERR_COMMAND_UNKNOWN
