
import random
from train import AI_Bot

global g__

class game():
    def __init__(self):
        self._players = []
        self._dead = []
        #game begins at night
        self._night = True
        self._day_num = 1

    def add_player(self, ID):
        if ID in self._players or ID in self._dead:
            return 'ERROR: PLAYER ALREADY ADDED'
        else:
            self._players.append(ID)

    def kill_off(self, ID): #kill a player and remove them from active list
        if ID in self._dead:
            return 'ERROR: PLAYER ALREADY DEAD'
        else:
            self._players.remove(ID)
            #kill the player and append them to the dead player list
            ID.died()
            self._dead.append(ID)

    def disclose_mafia(self):
        # disclose to both mafia people that eachother exsist returns, a list of mafia player objects
        mafia = []
        for x in range(0, len(self.__players)):
            if not(self._players[x].is_innocent()):
                mafia.append(self._players[x])
        return mafia


    #takes in votes from all of the players and counts the ballots to see who is voted off
    def count_ballots(self, ballot):
        votes = {}
        for x in range(0, 7):
            if ballot[x] not in votes:
                votes[ballot[x]]=1
            else:
                votes[ballot[x]]+=1
        for x in votes:
            if votes[x] == max(votes.values()):
                killed = x

                
        return killed

    def is_night(self):
        return self._night
    
    def what_day_is_it(self):
        return self._day_num


#------------------------------------------------------------------------------------------------


class Player():
    def __init__(self, role, name):
        self._role = role
        self.name = name
        self._alive = True
        self._doctor = False
        self._mafioso = False
        if role == 'MAFIA':
            self._mafioso = True
        if role == 'DOCTOR':
            self._doctor = True
        
    def status(self):   #return an outline of player status
        return self._name, self._role, self._alive
    
    def is_innocent(self):   #check to see what team the player is on
        return not(self._mafioso)
    
    def died(self):         #kill off the player and change the flag
        self._alive = False
    
    def is_doctor(self):    #check to see if the player has the power to revive a person
        return self._doctor












    
    
    

        
    














    




    







    

     


    

    




    
