
import random


global g__

class game():
    def __init__(self):
        self._players = {}
        self._dead = {}
        #game begins at night
        self._night = True
        self._day_num = 1

    def add_player(self, ID):
        if ID.name in self._players or ID.name in self._dead:
            return 'ERROR: PLAYER ALREADY ADDED'
        else:
            self._players[ID.name] = ID

    def kill_off(self, name): #kill a player and remove them from active list
        if name in self._dead:
            return 'ERROR: PLAYER ALREADY DEAD'
        else:
            dead = self._players.pop(name)
            #kill the player and append them to the dead player list
            dead.died()
            self._dead[name] = dead

    def disclose_mafia(self):
        # disclose to both mafia people that eachother exsist returns, a list of mafia player objects
        mafia = []
        for x in self._players.keys():
            if not(self._players[x].is_innocent()):
                mafia.append(self._players[x].name)
        return mafia
    
    def last_killed(self):
        if len(self._dead) == 0:
            return "NOBODY DIED"
        else:
            name, ID = self._dead.popitem()
            self._dead[name] = ID
            return name


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
    def __init__(self, role, name, bot=False):
        self._role = role
        self.name = name
        self._alive = True
        self._doctor = False
        self._mafioso = False
        self._bot = bot
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
    
    def is_bot(self):
        return self._bot












    
    
    

        
    














    




    







    

     


    

    




    
