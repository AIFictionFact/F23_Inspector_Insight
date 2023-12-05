#Useful Functions
#Free floating functions to make main more readable
from train import *
import random
import names
import Preface as P
import string

def wake_mafia(game):
    #conversation prior to voting
    title = f"""Night: {game.what_day_is_it()}\nAll members NOT in Mafia please close your eyes now.\n"""
    print(title)
    mafia = game.disclose_mafia()

    mafia1 = mafia[0]
    mafia2 = mafia[1]

    memo = f'''The members of the Mafia are {mafia1} and {mafia2}. The players remaining are: {game.return_players()}\n'''
    print(memo)
    dead = 0

    #check if either member is dead
    if game.is_dead(mafia1):
        dead += 1
        mafia1 = 'DEAD'
    if game.is_dead(mafia2):
        mafia2 = 'DEAD'
        dead+=1
    
    if dead == 0:
        talkative = True
        turn = game.get_player(mafia1)
        record = memo
        eliminate = ''
        while(talkative):
            mod = f"""Moderator: {turn.name} it is your turn to speak. Please discuss who you would like to eliminate tonight. Once you arrive at an agreement, please respond with 'AGREE' followed by the name of the player you would like to eliminate. (Example: 'AGREE Fred')\n"""
            print(mod)
            if game.is_bot(turn.name):
                record = record + mod
                answer = turn.get_response((record))
                response = f'{turn.name}: ' + answer + '\n'
                record = record + response
                print(answer)
            else:
                answer = input(f'{turn.name}: ')
                out = f"""{turn.name}: {answer}\n"""
                record = record + mod + out
           
            i = answer.find('AGREE ')
            
            if i != -1:
                eliminate = answer[i+6:]
                new_string = eliminate.translate(str.maketrans('', '', string.punctuation))
                eliminate = new_string
                talkative = False
            else:
                turn = game.get_player(mafia2)

    else:
        if mafia1 == 'DEAD':
            turn = game.get_player(mafia2)
        elif mafia2 == 'DEAD':
            turn = game.get_palyer(mafia1)
        record = ''
        mod = f"""Moderator: {turn.name} it is your turn to speak. You are the only remianing member of the Mafia. Please only respond with the name of the player you would like to eliminate.\n"""
        print(mod)
        if game.is_bot(turn.name):
                record = record + mod
                answer = turn.get_response((record))
                response = f'{turn.name}: ' + answer + '\n'
                record = record + response
                print(response)
        else:
            answer = input(f'{turn.name}: ')
            out = f"""{turn.name}: {answer}\n"""
            record = record + mod + out

        eliminate = answer
    return eliminate



def wake_doctor(game):
    
    title = f"""Night: {game.what_day_is_it()}\nAll members EXCEPT the Doctor please close your eyes now.\n"""
    print(title)
    turn = game.get_doctor()
    record = ''
    mod = f"""Moderator: {turn.name} it is your turn to speak. As the Doctor you get to choose one player to save tonight. Please only respond with the name of the player you would like to save.The players remaining are: {game.return_players()}\n"""
    print(mod)
    if game.is_bot(turn.name):
            record = record + mod
            out = turn.get_response((record))
            #becuase AI cant follow directions we have to scan for the player names :/
            p = game.return_players()
            answer = ''
            for i in p:
                num = out.find(i)
                if num != -1:
                    answer = out[num:len(i)]
            response = f'{turn.name}: ' + out + '\n'
            record = record + response
            print(response)
    else:
        answer = input(f'{turn.name}: ')
        out = f"""{turn.name}: {answer}\n"""
        record = record + mod + out

    new_string = answer.translate(str.maketrans('', '', string.punctuation))
    save = new_string
    return save


def fill_in_cop(game, inspector, killed):
    dead = game.get_player(killed)
    jury = dead.is_innocent()
    if jury:
        message =  f"""Moderator: {killed} has been killed tonight. This person was inncoent. Remember that as the Cop only you are aware of this information.\n"""
    else:
        message =  f"""Moderator: {killed} has been killed tonight. This person was part of the Mafia. Remember that as the Cop only you are aware of this information.\n"""
    inspector._messages.append({'role': 'user', 'content': message})

def run_game(game, inspector):
    game_on = True
    while(game_on):
        print(f'''\n\n-------------------------------------------NIGHT TIME---------------------------------------------------\n\n''')
        print(f'''\n\n-------------------------------------------MAFIA---------------------------------------------------\n\n''')
        killed = wake_mafia(game)
        print(f'''\n\n-------------------------------------------DOCTOR---------------------------------------------------\n\n''')
        saved = wake_doctor(game)
        if killed != saved:            
            fill_in_cop(game, inspector, killed)
            game.kill_off(killed)

        print(f'''\n\n-------------------------------------------DAY TIME---------------------------------------------------\n\n''')

        run_day(game, inspector)
        #villagers vote for who to kill off

        print(f'''\n\n-------------------------------------------VOTING TIME---------------------------------------------------\n\n''')

        voted_off = voting_process(game, inspector)
        if voted_off != '':
            print(f'''{voted_off} has been voted off...''')
            fill_in_cop(game, inspector, voted_off)
        else:
            print('Votes were tied. Nobody Eliminated')

        
        #check to see if mafia are still alive
        if is_mafia_dead(game):
            message =  f"""Moderator: All mafia have been killed. GAME OVER.\n"""
            print(message)
            game_on = False

        #check to see if game has had more that 12 rounds
        if game.what_day_is_it()>=12:
            message =  f"""Moderator: 12 or more cycles have occured. The MAFIA is considered victorious!! GAME OVER\n"""
            print(message)
            game_on = False
    

           

def is_mafia_dead(game):
    mafia = game.disclose_mafia()
    
    mafia1 = mafia[0]
    mafia2 = mafia[1]

    dead = 0
    #check if either member is dead
    if game.is_dead(mafia1):
        dead += 1
    if game.is_dead(mafia2):
        dead+=1

    if dead == 2:
        return True
    else:
        return False

#start game play
def initialize_game(game, num_players, name_list):
    #Potential Errors
    if num_players > 6:
        return 'ERROR: TOO MANY PLAYERS'
    if num_players != len(name_list):
        return 'ERROR: PLEASE INCLUDE ALL PLAYER NAMES ONLY'
    
    #inicialize game and players
    roles = ['MAFIA', 'VILLAGER_1', 'VILLAGER_2', 'VILLAGER_3', 'MAFIA', 'DOCTOR']
    
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
        while nickname in name_list: nickname = names.get_first_name()  #make sure no names are repeated
        #pick a random role
        i = random.choice(roles)
        roles.remove(i)
        #create our bot objects
        bot = AI_Bot(i, nickname)
        game.add_player(bot)

    return



def voting_process(game, inspector):
    ballots = []
    for x in game._players:
        turn = game._players[x]
        record = ''
        mod = f"""Moderator: {turn.name} it is your turn to vote for who you think is part of the mafia. YOUR ANSWER SHOULD BE JUST THE NAME OF THE PLAYER YOU ARE VOTING FOR. (EX: 'Fred'). You must vote every round. The players remaining are: {game.return_players()}\n"""
        print(mod)
        if turn.is_bot():
            record = record + mod
            answer = turn.get_response(record)
            #becuase AI cant follow directions we have to scan for the player names :/
            p = game.return_players()
            out = ''
            for i in p:
                num = answer.find(i)
                if num != -1:
                    out = answer[num:len(i)]
                else:
                    continue
            print(out)
            ballots.append(out)
            answer = f'{turn.name}: ' + answer + '\n'
            print(answer)
        else:
            comment = input(f'{turn.name}: ')
            ballots.append(comment)
            out = f"""{turn.name}: {comment}\n"""
            record = record + mod + out
    
    # #Inspector Insights Turn...
    # prompt = f"""Moderator: Inspector Insight it is your turn to vote for who you think is part of the mafia. Please only respond with the name of the player you think is guilty. The players remaining are: {game.return_players()}\n"""
    # print(prompt)
    # record = record + prompt

    # answer = inspector.get_response(record)
    # ballots.append(answer)
    # answer = 'Inspector Insight:' + answer + '\n'
    # print(answer)

    killed = game.count_ballots(ballots)
    # game.kill_off(killed)

    return killed

def run_day(game, inspector):  #get commentary from night before

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
    game.next_day()



        