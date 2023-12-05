
#handles everything to do with our AI inspector
from Preface import Player
import openai

file = open('password.txt', 'r')
password = file.readline()


OPENAI_API_KEY = password


openai.api_key = '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'

#Holds previous AI knowledge and interations
#create a child class of player for bots
class AI_Bot(Player):
    def __init__(self, role, name):
        Player.__init__(self, role, name, True)
        self.context = f'''Your name is {name}. You are a {role} in a game called Mafia.
                    Your job is to ask questions and interact with the users and figure out who is the part of the mafia. Statements from each player will begin with their name, including the moderator, named Moderator. 
                    These are the rules of the game: Lying and bluffing are not only allowed, but are necessary for play! 
                    That being said, lying as town can lead to you being executed.
                    A player who has been killed is no longer part of the game, and may not participate.
                    The roles of players who have been killed are public. All other roles are hidden.
                    Mafia must not reveal themselves or their partner to the town.
                    The goal of the mafia is to bring the town to 4 members including 2 mafia, or 2 members including 1 mafia.
                    Mafia tries to eliminate the majority of town by killing at night or having innocents executed by vote.
                    The goal of the villager is to prevent other villagers from being killed, and to correctly vote both members of the mafia at day meetings.
                    The "classic" mafia setup is: 2 mafia, 3 villagers, 1 cop, 1 doctor. Roles are assigned randomly prior to the game, you have been assigned role of {role}.
                    The game begins in the night phase.
                    There are two phases: night and day. At night, certain players secretly perform special actions.
                    The mafia can share notes, and agree on which player they would like to *kill* (remove from the game.) 
                    The doctor can guess who might be killed, and block a kill attempt, if one is made. 
                    The villager is a character who receives zero information during this period. 
                    The cop can do an "investigation" (select another player and learn whether they are sided with the mafia or innocents.
                    During day, players try to figure out who mafia is, and vote to "lynch", or eliminate, one player. Players may vote to execute other players,
                    and when the players finish voting, the person with 50% or more of the town votes is lynched.
                    The roles of cop and doctor are known only by themselves, and they can choose to declare their role if they think it can help town execute the correct player.
                    The mafia team frequently lies and claims that they are the cop, presenting a false report on another players innocence/guilt,
                    in order to have the town execute the cop, which aids the mafia. In situations where town decides to execute a player, 
                    the mafia team faces the challenge of having a town player executed.
                    While the goal of the doctor is to keep the cop or other villagers alive, and the cops goal is to find one or both mafia and 
                    convince the town to execute them, 
                    and the goal of the mafia is to have the cop, doctor, or other town executed,
                    the villager has the harder challenge of deciding what the optimal execution is without any information received outside of the day phases.
                    The conversations that happen during the day are Turn based, so you will only answer when you are notified of your turn. 
                    The moderator will disclose whos turn it is. The moderator will also let you know when it is your turn to vote.
                    When it is time to vote, just respond with the name of the player you would like to vote off.
                    These phases alternate with each other until all mafiosio have been eliminated or until the mafia outnumbers the innocents.
                    There is a moderator that will distribute information needed to play the game.
                    '''
        self._messages = [{"role": "system", "content": self.context}]

        

    def get_response(self, message):
        #check our current token size and summerize if needed
        self.check_tokens()

        self._messages.append({'role': 'user', 'content': message})
        response =  openai.ChatCompletion.create(model='gpt-3.5-turbo', messages = self._messages, temperature = 1, max_tokens = 250)
        #Update Message List with each Dialoge so that our Bot can gain insight and the conversation flows

        self._messages.append({'role':'assistant', 'content': response.choices[0].message.content})

        return response.choices[0].message.content
    
    def get_vote(self, message):
        
        #check our current token size and summerize if needed
        self.check_tokens()

        self._messages.append({'role': 'user', 'content': message})
        response =  openai.ChatCompletion.create(model='gpt-3.5-turbo', messages = self._messages, temperature = 1, max_tokens = 32)
        return response.choices[0].message.content
    
    def check_tokens(self):
        token_size = 0
        #some prep in case we need to shorten
        tmp_messages = [{"role": "system", "content": "You are an assistant, used to summarize text so that they remain under the max token size for a gpt model which is 4000 tokens. Summarize given text while maintaining clearity and understanding. Try to make it as short as possible, without risking ruining the context."}]
        big_chunk = 'Summerize the following Message: '

        for i in range(1, len(self._messages)):
            token_size += len(self._messages[i]['content'])

            big_chunk = big_chunk + self._messages[i]['content']
        

        #add the size of our incial system set up
        token_size += 747

        #check if we are close to the token max threshold 4,000
        if token_size >= 4000:
            #we need to shorten our context in order to not risk running out of space
            tmp_messages.append({"role":"user", "content": big_chunk})
            #we can send a query to another instance of a gpt model with a diffrent system context to shorten it
            #we then use this response and return it as our new message
            tmp_response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages = tmp_messages, temperature = 0.5, max_tokens = 4000)
            new_system = tmp_response.choices[0].message.content

            #re_write our inspector system
            self._messages = [{"role": "system", "content": self.context+new_system}]
            return

        else:
            return


        


        

           
            


        

    





