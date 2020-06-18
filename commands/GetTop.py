from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings

import requests
from time import time
from json import loads, dumps
from os import listdir

class GetTop(Command):

    key = ('топ', 'top', 'рейтинг')
    permissions = 0

    @classmethod
    def process(cls, request, offset=0):
        from_id = request.event.object['from_id']
        offset = int(offset)

        @cls.checkForPermission(from_id, request.chat_id)
        def work(offset):
            cls.sendMessage(Samples.COMMAND_GETTOP_PRESTART, request.chat_id)
            chats = listdir('db')
            chat_ids = list()
            users = dict()

            for db in chats:
                chat_ids.append(int(db[:-3]))

            for chat_id in chat_ids:
                chat_users = Sql.execute("select user, money from Economy", chat_id)
                chat_name = Settings.vk.messages.getConversationsById(peer_ids=2000000000+chat_id)['items'][0]['chat_settings']['title']

                for user in chat_users:
                    if str(user[0]) in users.keys():
                        print(1)
                        if users[str(user[0])][0] < user[1]:
                            print(2)
                            users[str(user[0])] = (user[1], chat_name, chat_id)
                            print(3)
                    else:
                        users[str(user[0])] = (user[1], chat_name, chat_id)

            top = sorted(users.items(), key=lambda user: user[1][0], reverse=True)[offset:10]

            print(top)

            message = Samples.COMMAND_GETTOP_START

            for user in top:
                message += Samples.COMMAND_GETTOP_TOP.format(top.index(user)+1,
                                                     Samples.getReference(int(user[0]), user[1][2]),
                                                     user[1][0],
                                                     user[1][1])

            return message

        return work(offset)
