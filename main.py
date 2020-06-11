import vk_api
import random
import asyncio

from Settings import Settings
from Handler import Handler
from vk_api.bot_longpoll import VkBotEventType
from RequestClass import Request

"""++====-----------==--------=-------+--- ------------   ------- -- ---   -
| Это главный файл. Содержит класс Bot
|
|
|           Метод -> возвр. знач.            Краткое пояснение
|
\\=+-          start -> None                Запускает главный луп
/
\\=+-        handleEvent -> None           Предобработчик ивента.
/                                
\\=+-       eventListener -> None               Главный луп
/
|
\==---=-------------+------------- -------  ----   -   -"""



class Bot(Settings):
    def __init__(self):
        self.Handler = Handler()

    # Asyncio это хорошо
    def start(self) -> None:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.run())

    async def run(self):
        while True:
            await self.eventListener()

    # Эта функция отправляется в ensure_future и выполняется асинхронно.
    # Передает обработчику запрос, получает ответ и отправляет его в чат.
    async def handleEvent(self, event: VkBotEventType) -> None:
        # Передаем в обработчик реквест и получаем ответ
        result: str = self.Handler.handleRequest(Request(event.type, event, chat_id=event.chat_id))
        keyboard: dict = dict()
        attachment: str = ''
        message: str = ''

        if result:
            if type(result) == dict:    
                if 'keyboard' in result.keys():
                    keyboard = result['keyboard']
                if 'attachment' in result.keys():
                        attachment = result['attachment']
                if 'message' in result.keys():
                        message = result['message']
            else:
                message = result
                                
        if event.from_chat:
                self.vk.messages.send(
                                    chat_id=event.chat_id,
                                    message=message,
                                    random_id=random.randint(1, 600000),
                                    keyboard=keyboard,
                                    attachment=attachment
                                )

    # Слушаем Longpool. Это что-то вроде главного цикла
    async def eventListener(self) -> None:
        while True:
            try:
                for event in self.longpoll.check():
                    asyncio.ensure_future(self.handleEvent(event))

                await asyncio.sleep(0)
            except Exception as e:
                print(e)

if __name__ == '__main__':
    c = Bot()
    c.start()
