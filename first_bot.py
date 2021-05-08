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

def id_gen():
    return ''.join(random.choice(string.ascii_letters) for x in range(5))
    
class Bet:
    
    def __init__(self, title, users, pot, wager):
        self.title = title
        self.users = users
        self.pot = pot
        self.wager = wager
        self.id = id_gen()
        
    def announce(self):
        return f'Title: {self.title}, users: {self.users}, pot: {self.pot}, wager: {self.wager}, id: {id}'    
        
        
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
    
        bet_title = message.content[5:]
        print(f'NEW BET: {bet_title}')
        bets[bet_title] = Bet(bet_title, [message.author], 10, 10)
        
        
    if message.content.startswith('!openbets'):
        for bet in bets:
            await message.channel.send(bet)
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
