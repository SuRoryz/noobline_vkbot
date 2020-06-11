import vk_api

from CommandClass import Command
from Sql import Sql
from Samples import Samples
from permissions import Permission
from Settings import Settings
from AdminCommands.Admin import AdminCommands as AC

from json import loads, dumps
from random import randint

class GameCoinFlip(Command, Settings):

    key = ('кф', 'коинфлип', 'cf', 'coinflip')
    permissions = 3

    @classmethod
    def process(cls, request, subcommand='', *args):

        from_id = request.event.object['from_id']

        try:
            subcommand = subcommand.lower()
        except:
            pass

        if not(subcommand) or not(subcommand in ['орел', 'орёл', 'решка', 'выйти', 'поиск']):
            return Samples.GAME_CF_NOSUBCOMMAND
        
        def cfUpload(cf):
            cf = dumps(cf)
            Sql.execute(f"update Games set coin_flip='{cf}'", request.chat_id)

        def getGame(target, cf):
            for game in cf['games_now']:
                    if target in game:
                        return game
            return False

        @cls.checkForPermission(from_id, request.chat_id)
        def work(from_id):            
            if subcommand == 'поиск':
                cf = loads(Sql.execute("select coin_flip from Games", request.chat_id)[0][0])
                
                if getGame(from_id, cf) or cf['in_search'] == from_id:
                    return Samples.GAME_CF_ALREADYIN

                if cf['in_search']:
                    player_2 = cf['in_search']
                    cf['in_search'] = None
                    cf['games_now'].append([player_2, from_id])

                    cfUpload(cf)

                    message = Samples.GAME_CF_STARTGAME.format(Samples.getReference(from_id, request.chat_id), Samples.getReference(player_2, request.chat_id))
                else:
                    cf['in_search'] = from_id
                    
                    cfUpload(cf)
                    
                    message = Samples.GAME_CF_SEARCHSTARTED

                return message

            if subcommand == 'выйти':

                cf = loads(Sql.execute("select coin_flip from Games", request.chat_id)[0][0])
                current_game = getGame(from_id, cf)

                if current_game or cf['in_search'] == from_id:
                    try:
                        cf['games_now'].remove(current_game)
                    except:
                        cf['in_search'] = None
                    cfUpload(cf)
                    return Samples.GAME_CF_EXIT
                return Samples.GAME_CF_ERR_NOTINGAME

            if subcommand in ['орел', 'решка', 'орёл']:
                
                cf = loads(Sql.execute("select coin_flip from Games", request.chat_id)[0][0])
                current_game = getGame(from_id, cf)

                if current_game:

                    player_2, player_1 = current_game

                    if player_2 == from_id:
                        player_2 = player_1
                        player_1 = from_id
                    
                    try:
                        _sum = abs(int(args[0]))
                    except:
                        return Samples.GAME_CF_ERR_NOSUM
                    
                    if AC.getMoney(player_2, request.chat_id) < _sum:
                        return Samples.GAME_CF_ERR_NOSUMENEMY

                    if AC.getMoney(player_1, request.chat_id) < _sum:
                        return Samples.GAME_CF_ERR_NOSUMME
                    
                    result = randint(0, 1)

                    print(result)
                    
                    if subcommand in ['орёл', 'орел']:
                        if result == 0:
                            
                            cf['games_now'].remove(current_game)
                            cfUpload(cf)
                            AC.addMoney(player_1, _sum, request.chat_id)
                            AC.addMoney(player_2, -_sum, request.chat_id)
                            return Samples.GAME_CF_WIN_O.format(Samples.getReference(player_1, request.chat_id))

                        cf['games_now'].remove(current_game)
                        cfUpload(cf)
                        AC.addMoney(player_2, _sum, request.chat_id)
                        AC.addMoney(player_1, -_sum, request.chat_id)
                        return Samples.GAME_CF_WIN_R.format(Samples.getReference(player_2, request.chat_id))
                    else:
                        if result == 0:
                            cf['games_now'].remove(current_game)
                            cfUpload(cf)
                            AC.addMoney(player_1, _sum, request.chat_id)
                            AC.addMoney(player_2, -_sum, request.chat_id)
                            return Samples.GAME_CF_WIN_R.format(Samples.getReference(player_1, request.chat_id))

                        cf['games_now'].remove(current_game)
                        cfUpload(cf)
                        AC.addMoney(player_2, _sum, request.chat_id)
                        AC.addMoney(player_1, -_sum, request.chat_id)
                        return Samples.GAME_CF_WIN_O.format(Samples.getReference(player_2, request.chat_id))


                return Samples.GAME_CF_ERR_NOTINGAME

        return work(from_id)
