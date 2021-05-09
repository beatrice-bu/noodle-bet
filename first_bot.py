from os.path import join
import discord
import json
import os
from numpy.random import rand
import string
import random
client = discord.Client()

with open('token.txt', 'r') as t:
    token = t.read()

bets = {}


#TODO add a bets loading option


def id_gen():
    return ''.join(random.choice(string.ascii_letters) for x in range(5))
    
class Bet:
    
    def __init__(self, title, users, pot, wager, id):
        self.title = title
        self.users = users
        self.pot = pot
        self.wager = wager
        self.id = id
        
        
    def __str__(self):
        return 'Title: {} - Participants: {}. Total Pot: {} noodles. Current wager: {} noodles. Join with code: {}'\
            .format(self.title, self.users, self.pot, self.wager, self.id)
    
    
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
        new_id = id_gen()
        bet_text = message.content
        bet_amount = bet_text.split(" ")[-1]
        bet_title = ''.join([i for i in bet_text[5:] if not i.isdigit()])
        
        await message.channel.send(f'NEW BET: **{bet_amount} noodles** => *"{bet_title}"*. Use code "{new_id}" to join in bet.')
        bets[new_id] = bets.get(new_id, Bet(title=bet_title, users=[message.author.display_name], pot=bet_amount, wager=bet_amount, id=new_id))
        
        
    if message.content.startswith('!openbets'):
        await message.channel.send('CURRENTLY OPEN BETS:')
        for bet in bets:
            await message.channel.send(bets[bet])


    if message.content.startswith('!wager'):
        #TODO check that user has money to wager
        #TODO take money from user
        #try else except
        try:
            join_id = message.content[7:12]
            print(join_id)
            bet_to_join = bets[join_id]
            
            
            
            if message.author.display_name in bet_to_join.users:
                raise ValueError("User is already a participant in the bet.")
        except ValueError as ve:
            print(ve)
            await message.channel.send('You are already a participant in this bet!')
        else:
            bet_to_join.users.append(message.author.display_name)
            await message.channel.send(f'{message.author.display_name} has joined in on: {bet_to_join.title}. Join in with code: {join_id}!')
        
        

##TODO add a winner function
#TODO closes bet

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


client.run(token)
