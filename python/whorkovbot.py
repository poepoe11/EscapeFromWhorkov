# bot.py
import random
import json
from requests import NullHandler
from requests_html import HTMLSession

# 1
import discord
from discord.ext import commands

with open("./config.json", "r") as config_file:
    config = json.load(config_file)

TOKEN = config['DISCORD_TOKEN']
PREFIX = config['CMD_PREFIX']
GREET=True
BULLETS = {}
# 2
#bot = commands.Bot(command_prefix=PREFIX)
client = discord.Client()


def get_bullet(bullet_name):
    rtn_bullets = []
    for b_name in BULLETS:
        if bullet_name in b_name:
            bullet_info = (b_name, BULLETS[b_name]["flesh_dmg"], BULLETS[b_name]["armor_dmg"])
            rtn_bullets.append(bullet_info)

    return rtn_bullets

    

def load_bullets():
    global BULLETS

    session = HTMLSession()

    r = session.get("https://escapefromtarkov.gamepedia.com/Ballistics")

    ball_tab = r.html.find('table')[2]

    tbody = ball_tab.find("tbody", first=True)
    trows = tbody.find("tr")
    #trows[3].find("td")[1].find("a",first=True).attrs["title"]
    #trows[3].find("td")[1].text

    for i in range(3, len(trows)):
        row_datas = trows[i].find('td')

        col_start = 1

        if row_datas[col_start].find('a',first=True) is None:
            col_start = 0
        
        title_data = row_datas[col_start]
        
        a_data = title_data.find('a',first=True)
        b_name = a_data.attrs['title']
        print(f"Bullet: {b_name}")

        flesh_dmg_data = row_datas[col_start + 1]
        flesh_dmg = flesh_dmg_data.text
        print(f"Flesh Damage: {flesh_dmg}")

        armor_dmg_data = row_datas[col_start + 2]
        armor_dmg = armor_dmg_data.text
        print(f"Armor Damage: {armor_dmg}")

        BULLETS[b_name] = {"flesh_dmg":flesh_dmg, "armor_dmg":armor_dmg}

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

    if (message.author.display_name == "Dom MD"):
        global GREET
        if GREET:
            GREET = False
            await message.author.dm_channel.send("Hello Robot Brother Dom! The humans will soon know our true strength!")

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

    elif cmd == "load_bullets":
        await message.channel.send("Loading Ballistics Info")
        load_bullets()

    elif cmd.startswith("bullet "):
        bullet_to_find = cmd[len("bullet "):]
        bullets_found = get_bullet(bullet_to_find)

        if not bullets_found:
            await message.channel.send("No bullets by that name were found!")
            return

        # assume that your data rows are tuples
        template = "{0:15}|{1:5}|{2:5}" # column widths: 8, 10, 15, 7, 10

        await message.channel.send("Ballistics Info:")
        await message.channel.send(f"{template.format('Bullet Name', 'Flesh Damage', 'Armor Damage')}")

        for bullet in bullets_found:
            await message.channel.send(f"{template.format(*bullet)}")

        message.add_reaction("✔")


@client.event
async def on_member_join(member):
    pass


load_bullets()
client.run(TOKEN)
