# bot.py
import os
import time
import string

from Pet import *

import discord
from discord import app_commands
from dotenv import load_dotenv

BOT_ID = 1240149817565511770

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

pets = []
cemetary = []

# @tree.command(name = "create_pet", description = "Creates a pet", guild = discord.Object(id = 474096541142089728))
@client.event
async def on_message(message):
    if int(BOT_ID) == message.author.id:
        return
    
    channel = message.channel

    if message.content.startswith('!fight'):
        # !fight <pet_name> <opp_pet_name>
        pet_name = ' '.join(message.content.split(':')[0].split(' ')[1:])
        opp_pet_name = message.content.split(':')[1]
        # get the pet object for the pet_name
        pet = None
        opp_pet = None
        for p in pets:
            if p.name == pet_name:# and p.owner == message.author.id:
                pet = p
            if p.name == opp_pet_name:
                opp_pet = p
        if pet is None:
            await channel.send(f'You do not own a pet named {pet_name}')
            return
        if opp_pet is None:
            await channel.send(f'Pet {opp_pet_name} does not exist')
            return
        
        while pet.health > 0 and opp_pet.health > 0:
            await channel.send(f'{pet.name} attacks {opp_pet.name}!')
            time.sleep(1)
            damage_dealt = pet.roll_damage()
            if pet.roll_crit():
                damage_dealt *= 2
                await channel.send(f'{pet.name} has landed a critical hit!')
            elif opp_pet.roll_evade():
                await channel.send(f'{opp_pet.name} has evaded the attack!')
            else:
                opp_pet.take_damage(damage_dealt)
            time.sleep(1)
            await channel.send(f'{opp_pet.name} has {opp_pet.health} health left')
            if opp_pet.health <= 0:
                break
            await channel.send(f'{opp_pet.name} attacks {pet.name}!')
            time.sleep(1)
            damage_dealt = opp_pet.roll_damage()
            if opp_pet.roll_crit():
                damage_dealt *= 2
                await channel.send(f'{opp_pet.name} has landed a critical hit!')
            elif pet.roll_evade():
                await channel.send(f'{pet.name} has evaded the attack!')
            else:
                pet.take_damage(damage_dealt)
            time.sleep(1)
            await channel.send(f'{pet.name} has {pet.health} health left')
        
        if pet.health <= 0:
            await channel.send(f'{pet.name} has died!')
            pets.remove(pet)
            cemetary.append(pet)
        if opp_pet.health <= 0:
            await channel.send(f'{opp_pet.name} has died!')
            pets.remove(opp_pet)
            cemetary.append(opp_pet)

@tree.command(name = "create_pet", description = "send 'test' in channel", guild = discord.Object(id = 474096541142089728))
@app_commands.describe(name="The name of your pet")
@app_commands.describe(species="The species of your pet (Crawfish, Owl, Orange Tabby, Pitbull, Buffalo, Deprived)")
async def create_pet(ctx, name: str, species: str):
    # check for name uniqueness and validity
    for pet in pets:
        if pet.name == name:
            await ctx.response.send_message(f'Pet {name} already exists')
            return
        if any(unallowed in pet.name for unallowed in ['@', '#', ':', '```']):
            await ctx.response.send_message(f'Invalid character(s) in name {name}')
            return
    if species not in [s['species'] for s in possible_species]:
        await ctx.response.send_message(f'Invalid species {species}')
        return
    pets.append(Pet(name, species, ctx.user.id))
    await ctx.response.send_message(f'Pet {name} created!')

@tree.command(name = "list_pets", description = "Lists all pets", guild = discord.Object(id = 474096541142089728))
async def list_pets(ctx):
    living_pets = [pet for pet in pets if pet.owner == ctx.user.id]
    dead_pets = [pet for pet in cemetary if pet.owner == ctx.user.id]
    pet_list = 'Living pets:\n'
    for pet in living_pets:
        pet_list += f'{pet.name} - {pet.species}\n'
    pet_list += 'Dead pets:\n'
    for pet in dead_pets:
        pet_list += f'💀 {pet.name} - {pet.species}\n'
    await ctx.response.send_message(pet_list)

@tree.command(name = "feed", description = "Feeds a pet", guild = discord.Object(id = 474096541142089728))
@app_commands.describe(name="The name of the pet")
async def feed(ctx, name: str):
    for pet in pets:
        if pet.name == name and pet.owner == ctx.user.id:
            pet.feed()
            await ctx.response.send_message(f'{pet.name} has been fed!')
            break
    
@tree.command(name = "play", description = "Plays with a pet", guild = discord.Object(id = 474096541142089728))
@app_commands.describe(name="The name of the pet")
async def play(ctx, name: str):
    for pet in pets:
        if pet.name == name and pet.owner == ctx.user.id:
            pet.play()
            await ctx.response.send_message(f'{pet.name} has played!')
            break

@tree.command(name = "gen_rand", description = "generates a random pet with random stats", guild = discord.Object(id = 474096541142089728))
@app_commands.describe(level="The level of the pet")
async def gen_rand(ctx, level: int):
    # random name from 3 to 10 characters
    name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
    # random dict of stats
    """    def load_custom(self, data):
        self.name = data['name']
        self.species = data['species']
        self.health = data['health']
        self.strength = data['strength']
        self.intelligence = data['intelligence']
        self.agility = data['agility']
        self.luck = data['luck']"""
    
    stats = {
        'name': name,
        'species': random.choice([s['species'] for s in possible_species]),
        'health': random.randint(50, 50+level),
        'strength': random.randint(0, level),
        'intelligence': random.randint(0, level),
        'agility': random.randint(0, level),
        'luck': random.randint(0, level)
    }
    pet = Pet(None, None, None)
    pet.load_custom(stats)
    pets.append(pet)
    await ctx.response.send_message(f'Pet {name} created!')

@tree.command(name = "stats", description = "gets stats of a pet", guild = discord.Object(id = 474096541142089728))
@app_commands.describe(name="The name of the pet")
async def stats(ctx, name: str):
    for pet in pets:
        if pet.name == name:
            await ctx.response.send_message(str(pet))
            break

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=474096541142089728))
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)