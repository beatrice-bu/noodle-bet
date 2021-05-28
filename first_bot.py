from os.path import join
import discord
import json
import os
from numpy.random import rand
import string
import random
client = discord.Client()
import time

with open('token.txt', 'r') as t:
    token = t.read()

bets = {}


#TODO add a bets loading option



def transaction_check(function):

    def check_wrapper(bet_id, bet_amount, bet_title, bet_user):
        
        bet_amount = int(bet_amount)
        user_id = str(bet_user.id)
        print(
            f'Betting user ID: {user_id}'
        )
        user_name = str(bet_user.display_name)
        
        #checking if user has enough noodles
        
        with open(user_id + '.json', 'r') as user_json:
            #open json attached to user id
            print('Opening users .json data...')
            user_data = json.load(user_json)
            #load json data attached to user id
            user_available_noodles = user_data["noodles"]
            print(f'User has {user_available_noodles} noodles...')
            #load the user's available noodles to available noodles
        
        if user_available_noodles < bet_amount:
        #if user does not have enough noodles
            #then let them know lol
            raise Exception('User tried to wager a bet, but didnt have enough noodles.')
        
        
        else:
        #if they DO have enough noodles
        
            #create bet, without any users
            print(
                f'User has enough noodles. Creating bet {bet_id}'
            )
            function(bet_id, bet_amount, bet_title)
            #add current user to bet. this 
            
            bets[bet_id].users_id.append(user_id)
            bets[bet_id].users_name.append(user_name)
            print(
                f'Adding user to bet ledger'
            )
            print(
                f'Adding wager to pot. {bets[bet_id].pot} + {bet_amount} = {bets[bet_id].pot + bet_amount}'
            )
            #adding wager to pot
            bets[bet_id].pot += bet_amount
            
            #add user to bet's ledger
            print(
                f'Taking {bet_amount} noodles from user. {user_available_noodles} - {bet_amount} = {user_available_noodles - bet_amount}'
            )
            #remove noodles from user
            user_data["noodles"] -= bet_amount
            
            print(
                f'Writing new noodle quantity to file...'
            )
            with open(user_id + '.json', 'w') as user_json:
                json.dump(user_data, user_json)
            
            print(
                'TRANSACTION COMPLETE'
            )
            
            return 'Ding!'
    return check_wrapper

def id_gen():
    
    #pull new id
    print(
        f'Acquiring new ID for bet..'
    )
    possible_id = ''.join(random.choice(string.ascii_letters) for x in range(5))
    '''
    NOT WORKING YET
    
    if bets[possible_id] not in globals():
        #try again
        possible_id = ''.join(random.choice(string.ascii_letters) for x in range(5))
        print(
            f'Using id {possible_id}...'
        )'''
    return possible_id
    
class Bet:
    
    def __init__(self, title, wager, bet_id):
        self.title = title
        self.users_id = []
        self.users_name = []
        self.pot = 0
        self.wager = wager
        self.bet_id = bet_id
        self.settled = False
        
    def __str__(self):
        return 'Title: {} - Participants: {}. Total Pot: **{} noodles.** Current wager: {} noodles. Join with code: **{}**'\
            .format(self.title, self.users_name, self.pot, self.wager, self.bet_id)


        
    def to_json(self):
        
        template ={
            
            "title":str(self.title),
            "users_id":str(self.users_id),
            "users_name":str(self.users_name),
            "pot":str(self.pot),
            "wager":str(self.wager),
            "id":str(self.id),
            "settled":str(self.settled)
            }
        
        bet_file_name = str(self.id)
        with open(bet_file_name + '.json', 'w') as wo:
            json.dump(template, wo)
    
    
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!hello'):
        print(f'Saying hello to {message.author}...')
        await message.channel.send(f'Hello, {message.author.display_name}.')
    
    if message.content.startswith('!register'):
        print(f'Registering {message.author}...')
        try:
            await register_user(message.author)
        except:
            await message.channel.send(f'Uh-oh, something went wrong. Contact your server admin.')
        else:
            await message.channel.send(f"Hi, {message.author.display_name}! You've been registered. You've been given an initial stipend of 100 noodles.")

    if message.content.startswith('!unregister'):
        print(f'Unregistering {message.author}...')
        await message.channel.send(f"Goodbye, {message.author.display_name}.")
        await unregister_user(message.author.id)
        
    
    if message.content.startswith('!noodles'):
        print(f'Checking how many noodles {message.author} has...')
        await message.channel.send(f'Hello, {message.author.display_name}. You have {noodles(message.author.id)} noodles.') 

    
    if message.content.startswith('!bet'):
        #TODO actually take noodles from user
        #TODO check if user has money
        #try else except for that
        
        fresh_id = id_gen()
        bet_text = message.content
        fresh_bet_amount = bet_text.split(" ")[-1]
        fresh_bet_title = ''.join([i for i in bet_text[5:] if not i.isdigit()])
        fresh_bet_user = message.author
        
        print(
            f'{fresh_bet_user} is attempting to make bet {fresh_bet_title} for {fresh_bet_amount}...'
            )

        try:
            await message.channel.send(createBet(fresh_id, fresh_bet_amount, fresh_bet_title, fresh_bet_user))
        except Exception as ex:
            print(ex)
            await message.channel.send('Bet creation failed. :( Not enough Noodles.')
        else:
            await message.channel.send(f'NEW BET: **{fresh_bet_amount} noodles** => *"{fresh_bet_title}"*. Use code "{fresh_id}" to join in bet.')
    
        
        
        
    if message.content.startswith('!openbets'):
        await message.channel.send('CURRENTLY OPEN BETS:')
        for bet in bets:
            await message.channel.send(bets[bet])


    if message.content.startswith('!wager'):
        
        #TODO take money from user

        wagering_user = message.author
        join_id = message.content[7:12]
        bet_to_join = bets[join_id]
        
        await message.channel.send(
            createWager(bet_to_join, bet_to_join.wager, bet_to_join.title, wagering_user)
            )
    
        
        
#TODO check if I am in a bet, or if someone else is in a bet
##TODO add a winner function
#TODO closes bet
#TODO possibly refactor with-as json read/writes as one function. this wuold affect 

@transaction_check
def createBet(new_id, bet_amount, bet_title):
    bets[new_id] = bets.get(new_id, Bet(title=bet_title, wager=bet_amount, bet_id=new_id))
        

@transaction_check
def createWager(bet_id, bet_amount, bet_title, bet_user):
    
    bet = bets[bet_id]
    wager_amount = bet.wager
    #initial wager amount
    
    user_to_check = str(user.id)
    #the unique id of the user
    
    
    try:
        if user_to_check in bet.users:
            #if the user is already in bet
            raise ValueError("User is already a participant in the bet.")
    
            #probably not a value error
    except ValueError as already_in_bet:
        #return error if user already in bet
        print(already_in_bet)
        return 'You are already a participant in this bet!'
    
    else:
        return f"{user.disaply_name} has joined in on the bet! The pot is now **{bet.pot}!**. Use code **{bet.id}** to join as well."
            
        
        
async def declare_winner(bet, user):
    ...
    payout = bet.pot
    winner_id = str(user.id)
    
    with open(winner_id + 'json', 'rw') as winner_json:
    
        winner_data = json.load(winner_json)
        winner_data["noodles"] += payout
        json.dump(winner_data)
    
    
async def register_user(user):
    base_noodles = 100
    recovery = rand(3,3,3)

    template ={
            "user_id":str(user.id),
            "latest_display_name":str(user.name),
            "noodles":base_noodles,
            "recovery_id":str(recovery)
            }
    user_file_name = str(user.id)
    with open(user_file_name + '.json', 'w') as wo:
        json.dump(template, wo)

async def unregister_user(user):
    id_to_read = str(user)
    full_json = id_to_read + '.json'
    if os.path.exists(full_json):
        os.remove(full_json)


def noodles(user):
    id_to_read = str(user)
    full_json = id_to_read + '.json'
    with open(full_json, 'r') as json_data:
        opened_json = json.load(json_data)
        
    loaded_noodles = opened_json["noodles"]

    return str(loaded_noodles)

#universal read-write because we have so many json opens 
def readWrite(output_name: str, action: str, data: dict =None):
    with open(output_name + '.json', action) as json_data:
        if action == 'r':
            return json.load(json_data)
        elif action == 'w':
            try:
                if data == None:
                    raise ValueError("No dict given for write out action.")
            except ValueError as no_data_given:
                print(no_data_given)
                return
            else:
                json.dump(data, json_data)
            
async def activeBackup():
    #for bet in bets:
        #write out bets 
    #for bet in wo_bets:
        #load in bets
    ...
client.run(token)

