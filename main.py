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
        pet = Pet.get_pet(pet_name)
        opp_pet = Pet.get_pet(opp_pet_name)

        if pet is None:
            await channel.send(f'{pet_name} does not exist!')
            return
        if opp_pet is None:
            await channel.send(f'{opp_pet_name} does not exist!')
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
        if opp_pet.health <= 0:
            await channel.send(f'{opp_pet.name} has died!')

@tree.command(name = "create_pet", description = "send 'test' in channel", guild = discord.Object(id = 474096541142089728))
@app_commands.describe(name="The name of your pet")
@app_commands.describe(species="The species of your pet (Crawfish, Owl, Orange Tabby, Pitbull, Buffalo, Deprived)")
async def create_pet(ctx, name: str, species: str):
    # check for name uniqueness and validity
    pets = Pet.get_all_pets()
    if any(unallowed in name for unallowed in ['@', '#', ':', '```']):
        await ctx.response.send_message(f'Invalid character(s) in name {name}')
        return
    for pet in pets:
        if pet.name == name:
            await ctx.response.send_message(f'Pet {name} already exists')
            return

    if species not in [s['species'] for s in possible_species]:
        await ctx.response.send_message(f'Invalid species {species}')
        return
    Pet.create(name, species, ctx.user.id)
    await ctx.response.send_message(f'Pet {name} created!')

@tree.command(name = "list_pets", description = "Lists all of your pets", guild = discord.Object(id = 474096541142089728))
async def list_pets(ctx):
    living_pets = Pet.get_pets(ctx.user.id)
    dead_pets = Pet.get_dead_pets(ctx.user.id)
    pet_list = 'Living pets:\n'
    for pet in living_pets:
        pet_list += f'{pet.name} - {pet.species}\n'
    pet_list += 'Dead pets:\n'
    for pet in dead_pets:
        pet_list += f'💀 {pet.name} - {pet.species}\n'
    await ctx.response.send_message(pet_list)

@tree.command(name = "all_pets", description = "Lists every pet", guild = discord.Object(id = 474096541142089728))
async def all_pets(ctx):
    pets = Pet.get_all_pets()
    pet_list = ''
    for pet in pets:
        pet_list += f'{pet.name} - {pet.species}\n'
    await ctx.response.send_message(pet_list)

@tree.command(name = "feed", description = "Feeds a pet", guild = discord.Object(id = 474096541142089728))
@app_commands.describe(name="The name of the pet")
async def feed(ctx, name: str):
    pet = Pet.get_pet(name)
    if pet is None:
        await ctx.response.send_message(f'{name} does not exist!')
        return
    if pet.check_ownership(ctx.user.id) is False:
        await ctx.response.send_message(f'{name} is not your pet!')
        return
    pet.feed()
    await ctx.response.send_message(f'{pet.name} has been fed!')
    
@tree.command(name = "play", description = "Plays with a pet", guild = discord.Object(id = 474096541142089728))
@app_commands.describe(name="The name of the pet")
async def play(ctx, name: str):
    pet = Pet.get_pet(name)
    if pet is None:
        await ctx.response.send_message(f'{name} does not exist!')
        return
    if pet.check_ownership(ctx.user.id) is False:
        await ctx.response.send_message(f'{name} is not your pet!')
        return
    pet.play()
    await ctx.response.send_message(f'{pet.name} has been played with!')

@tree.command(name = "gen_rand", description = "generates a random pet with random stats", guild = discord.Object(id = 474096541142089728))
@app_commands.describe(level="The level of the pet")
async def gen_rand(ctx, level: int):
    # random name from 3 to 10 characters
    name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 10)))
    # random dict of stats
    """    def load_custom(self, data):
        self.name = data['name']
        self.gender = data['gender']
        self.species = data['species']
        self.owner = data['owner']
        self.age = data['age']
        self.health = data['health']
        self.food = data['food']
        self.energy = data['energy']
        self.sanity = data['sanity']
        self.strength = data['strength']
        self.intelligence = data['intelligence']
        self.agility = data['agility']
        self.luck = data['luck']"""
    
    distribution = distribute_numbers(level, 4)
    stats = {
        'name': name,
        'gender': random.choice(['Male', 'Female']),
        'species': random.choice([s['species'] for s in possible_species]),
        'owner': ctx.user.id,
        'age': level,
        'health': random.randint(1, 100),
        'food': random.randint(1, 100),
        'energy': random.randint(1, 100),
        'sanity': random.randint(1, 100),
        # for the rest of the stats, we want to make sure they add up to the level the user input
        'strength': distribution[0],
        'intelligence': distribution[1],
        'agility': distribution[2],
        'luck': distribution[3]
    }
    pet = Pet(None, None, None)
    pet.load_custom(stats)
    pet.update()
    await ctx.response.send_message(f'Pet {name} created!')

@tree.command(name = "stats", description = "gets stats of a pet", guild = discord.Object(id = 474096541142089728))
@app_commands.describe(name="The name of the pet")
async def stats(ctx, name: str):
    pet = Pet.get_pet(name)
    if pet is None:
        await ctx.response.send_message(f'{name} does not exist!')
        return
    await ctx.response.send_message(f'{pet.name} - {pet.species}\nHealth: {pet.health}\nStrength: {pet.strength}\nIntelligence: {pet.intelligence}\nAgility: {pet.agility}\nLuck: {pet.luck}')

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=474096541142089728))
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)