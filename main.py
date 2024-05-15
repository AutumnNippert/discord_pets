# bot.py
import os

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

# @tree.command(name = "create_pet", description = "Creates a pet", guild = discord.Object(id = 474096541142089728))
@client.event
async def on_message(message):
    if int(BOT_ID) == message.author.id:
        return
    
    channel = message.channel
    if message.content == '!create_pet':
        await channel.send('Let\'s make you a pet! What is the name of your pet?')
        while True:
            msg = await client.wait_for('message', check=lambda message: message.author == message.author)
            if msg.author == message.author:
                break
        pet_name = msg.content
        await channel.send('What is the species of your pet? (Pitbull, Buffalo, Crawfish, Owl)')
        while True:
            while True:
                msg = await client.wait_for('message', check=lambda message: message.author == message.author)
                if msg.author == message.author:
                    break
            pet_species = msg.content
            if pet_species in ['Pitbull', 'Buffalo', 'Crawfish', 'Owl']:
                break
            await channel.send('Invalid species. Please enter a valid species (Pitbull, Buffalo, Crawfish, Owl)')
        pet = Pet(pet_name, pet_species, message.author)
        await channel.send(f'Pet {pet_name} created!')
        await channel.send(f'{pet}')
        pets.append(pet)

    if message.content == '!list_pets':
        for pet in pets:
            if pet.owner == message.author:
                await channel.send(f'{pet}')
    
    if message.content.startswith('!feed'):
        # !feed <pet_name>
        pet_name = message.content.split(' ')[1]
        for pet in pets:
            if pet.name == pet_name and pet.owner == message.author:
                pet.hunger += 10
                await channel.send(f'{pet.name} has been fed!')
                break


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=474096541142089728))
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)