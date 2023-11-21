
from train import AI_Bot
import Preface as P
import random
import names



INSPECTOR = AI_Bot("Inspector Insight", "COP")

#run game play
def run_game(game, num_players, name_list):
    #Potential Errors
    if num_players > 6:
        return 'ERROR: TOO MANY PLAYERS'
    if num_players != len(name_list):
        return 'ERROR: PLEASE INCLUDE ALL PLAYER NAMES ONLY'
    
    #inicialize game and players
    roles = ['MAFIA_1', 'VILLAGER_1', 'VILLAGER_2', 'VILLAGER_3', 'MAFIA_2', 'DOCTOR']
    
    for x in range(0, num_players):
        #pick random roles for each player
        i  = random.choice(roles)
        p = P.Player(i, name_list[x])
        roles.remove(i)

        #add players to game
        game.add_player(p)
    
    while len(roles)!=0:
        #generate a random name for our bots
        nickname = names.get_first_name()
        #pick a random role
        i = random.choice(roles)
        roles.remove(i)
        #create our bot objects
        bot = AI_Bot(i, nickname)
        game.add_player(bot)

    return
        
    

def start_conversation(game, inspector):  #get commentary from night before

    #conversation prior to voting
    title = f"""Day: {game.what_day_is_it()}\nThere are currently {len(game._players)} players alive. {len(game._dead)} have been killed.\n"""

    last_killed = game.last_killed()
    if last_killed != "NOBODY DIED":
        title = title + f"""{last_killed} was last to be killed.\n"""

    print(title)
    record = title
    for x in game._players:
        turn = game._players[x]
        mod = f"""Moderator: {turn.name} it is your turn to speak. What comments do you have about last night?\n"""
        print(mod)
        if turn.is_bot():
            record = record + mod
            answer = turn.get_response(record)
            answer = f'{turn.name}: ' + answer + '\n'
            print(answer)
        else:
            comment = input(f'{turn.name}: ')
            out = f"""{turn.name}: {comment}\n"""
            record = record + mod + out
    
    #Inspector Insights Turn...
    prompt = f'''Moderator: Inspector Insight it is your turn to speak. What comments do you have about last night?\n'''
    print(prompt)
    record = record + prompt

    answer = inspector.get_response(record)
    answer = 'Inspector Insight:' + answer + '\n'
    print(answer)

if __name__ == "__main__" :
    player_list = []
    number_players = 0
    GAME = P.game()
    run_game(GAME, number_players, player_list)
    # GAME.kill_off("Debbie")
    start_conversation(GAME, INSPECTOR)
    
    
    exit(0)

















