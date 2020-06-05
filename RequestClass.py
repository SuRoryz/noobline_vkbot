from vk_api.bot_longpoll import VkBotEventType

# Это класс запроса, именно его и принимает обработчик.
class Request:
    def __init__(self, _type, event: VkBotEventType, chat_id: int):
        self.type = _type
        self.event = event
        self.chat_id = chat_id
