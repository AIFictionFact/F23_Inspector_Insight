
from train import AI_Bot
import Preface as P
from Functions import *



INSPECTOR = AI_Bot("Cop", "Inspector Insight")
    

def get_inputs():
    players = []
    num = input('How many People are Playing? ')
    for x in range(0, num):
        name = input(f''''Please enter name for Player {x}''')
        players.append(name)
    return num, players




if __name__ == "__main__" :
    #since our integration has not been merged properly we keep these inputs hardcoded

    player_list = ['Frank', "Carl", "Fiona", "Lip", "Liam", "Debbie"]
    number_players = 6
    #number_players, player_list = get_inputs()
    GAME = P.game()
    initialize_game(GAME, number_players, player_list)
    
    run_game(GAME, INSPECTOR)
    
    exit(0)

















