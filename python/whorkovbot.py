# bot.py
import os
import random
import json
from dotenv import load_dotenv

# 1
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('CMD_PREFIX')

# 2
#bot = commands.Bot(command_prefix=PREFIX)
client = discord.Client()

#@bot.event
@client.event
async def on_ready():
    for guild in client.guilds:
        print(
            f'{client.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # All message reactions
    if "I died" in message.content or "i died" in message.content or "killed me" in message.content:
        with open("./death_responses.json", "r") as responses_file:
            responses = json.load(responses_file)
        await message.channel.send(random.choice(responses))

    # Message Commands
    # If the message doesn't start with the command prefix
    if not ( message.content.startswith(PREFIX)):
        # do nothing
        return

    # Else it has command prefix, chop it off
    cmd = message.content[len(PREFIX):].strip()
    print(f"cmd:{cmd}")
    if cmd == "ping":
        await message.channel.send("pong")


@client.event
async def on_member_join(member):
    if (member.user == "Dom MD"):
        defaultChannel = discord.utils.get(member.guild.text_channels, name="general")
        await defaultChannel.send("Hello Robot Brother Dom! The humans will soon know our true strength!")


client.run(TOKEN)
