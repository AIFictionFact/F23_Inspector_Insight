
from train import AI_Bot
import Preface
import os



inspector = AI_Bot()

#run game play
def run_game(num_players, name_list):
    #Potential Errors
    if num_players > 6:
        return 'ERROR: TOO MANY PLAYERS'
    if num_players != len(name_list):
        return 'ERROR: PLEASE INCLUDE ALL PLAYER NAMES ONLY'
    
    #inicialize game and players
    g__ = game()
    roles = ['MAFIA_1', 'VILLAGER_1', 'VILLAGER_2', 'VILLAGER_3', 'MAFIA_2', 'DOCTOR']
    
    for x in range(0, num_players):
        #pick random roles for each player
        i  = random.choice(roles)
        p = Player(i, name_list[x])
        roles.remove(i)

        #add players to game
        g__.add_player(p)



def start_conversation(game, inspector):  #get commentary from night before

    #conversation prior to voting
    last_killed = game._dead[-1]
    title = f"""Starting Day: {game.what_day_is_it()}\n
            Moderator: There are currently {len(game._players)} alive. {len(game._dead)} have been killed.\n
            Moderator: {last_killed.name} was last to be killed.\n"""
    print(title)
    record = title
    for x in game._players:
        turn = game._players[x]
        mod = f"""Moderator: {turn.name} it is your turn to speak. What comments do you have about last night?\n"""
        print(mod)
        comment = input('>>>>   ')
        out = f"""{turn.name}: {comment}\n"""
        print(out)
        record = record + mod + out
    
    #Inspector Insights Turn...
    prompt = f'''Moderator: Inspector Insight it is your turn to speak. What comments do you have about last night?\n'''
    print(prompt)
    record = record + prompt

    answer = inspector.get_response(record)
    answer = 'Inspector Insight:' + answer + '\n'
    print(answer)

if __name__ == "__main__" :
    player_list = ["Debbie", "Fiona", "Lip", "Carl", "Ian", "Liam"]
    number_players = 6
    run_game(number_players, player_list)

    exit(0)

















