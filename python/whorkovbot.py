# bot.py
import random
import json
import os

# TODO: Use importlib
import imp

import utils.util as UTILS

# 1
import discord
from discord.ext import commands


def load_config(filename="./config.json"):
    with open(filename, "r") as config_file:
        config = json.load(config_file)

    return config


class WhorkovBotClient(discord.Client):
    def __init__(self):
        """
        constructor/init
        """
        # List of registered commands
        self.cmd_classes = []

        # call super init
        super(WhorkovBotClient, self).__init__()

        # greet bool so it only happens once
        self.greet = True

        # load the config file into a json dict
        self.config = load_config()
        # parse that dict into self values
        self.parse_config()

        self.load_commands()

        UTILS.set_client(self)

    def load_commands(self, dir="./commands"):
        list_modules = os.listdir(dir)
        list_modules.remove("icommand.py")
        for module_name in list_modules:
            if module_name.split(".")[-1] == "py":
                print(f"Load module ' {module_name} ' :")
                cmd_module = imp.load_source("module", dir + os.sep + module_name)
                self.cmd_classes.append(cmd_module.get_cmd_class())

    def parse_config(self):
        """
        parse config dict into specific self vars
        """
        self.token = self.config["DISCORD_TOKEN"]
        self.cmd_prefix = self.config["CMD_PREFIX"]

    async def on_ready(self):
        """
        on connect to discord server
        """
        for guild in self.guilds:
            print(
                f"{self.user} is connected to the following guild:\n"
                f"{guild.name}(id: {guild.id})"
            )

    async def on_message(self, message):
        """
        when a message is sent
        """
        # if the author of the message is the bot user
        if message.author == self.user:
            # don't respond, because it's yourself
            return

        # If the message content contains one of the died trigger phrase
        if (
            "I died" in message.content
            or "i died" in message.content
            or "killed me" in message.content
        ):
            # open the death responses file
            with open("./death_responses.json", "r") as responses_file:
                # load the death response file into a json dict
                responses = json.load(responses_file)

            # send a random response
            await message.channel.send(random.choice(responses))

        if message.author.display_name == "Dom MD":
            if self.greet:
                self.greet = False
                await message.author.dm_channel.send(
                    "Hello Robot Brother Dom! The humans will soon know our true strength!"
                )

        # Message Commands
        # If the message doesn't start with the command prefix
        if not (message.content.startswith(self.cmd_prefix)):
            # do nothing
            return

        # Else it has command prefix
        # chop it off
        full_cmd_str = message.content[len(self.cmd_prefix) :].strip()

        # get the specific command word
        cmd_str = full_cmd_str.split()[0]

        # the rest of the wprds must be arguments
        arg_str = full_cmd_str[len(cmd_str) :].strip()

        # print command
        print(f"cmd:{cmd_str}")

        # for each of the registered commands
        for cmd_class in self.cmd_classes:
            # use command class method to test if this is the correct cmd
            if cmd_class.is_cmd(cmd_str=cmd_str):
                # found class
                print(f"Found cmd class: {cmd_class.__class__} for cmd: {cmd_str}")
                try:
                    # execute command
                    await cmd_class.execute_cmd(arg_str, message)
                except Exception as e:
                    print(f"Exception when executing command!\n{e}")
                    UTILS.fail_reaction(message=message)
                    raise e
                break

        await UTILS.confirm_message_cmd(message)

    async def on_member_join(self, member):
        pass


if __name__ == "__main__":
    botty_client = WhorkovBotClient()
    botty_client.run(botty_client.token)
