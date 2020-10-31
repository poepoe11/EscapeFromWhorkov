from utils import constants as CONST

CLIENT = None


def set_client(discord_client):
    global CLIENT
    CLIENT = discord_client


async def confirm_message_cmd(message):
    await message.add_reaction(CONST.EMOJIS.CMD_CONFIRM)


async def fail_reaction(message):
    await message.add_reaction(CONST.EMOJIS.CMD_FAIL)


async def send_msg(channel, msg_string):
    """
    utility method for sending messages to have
    a single location for safety checks
    """
    if len(msg_string) > CONST.MESSAGE.MAX_LEN:
        last_char = 1990
        msg_end = "\n.\n.\n."

        if CONST.MESSAGE.CODE_BLOCK in msg_string[last_char:]:
            last_char = 1987
            msg_end = msg_end + CONST.MESSAGE.CODE_BLOCK

        msg_string = msg_string[:last_char] + msg_end

    try:
        await channel.send(msg_string)

    except Exception as e:
        print(f"Exception occurred:\n{e}")
        return False

    return True


async def send_cmd_response(message, msg_string):
    """
    Utility method for sending a message when it is in
    response to a command message. This allows will respond
    to the original command in case of message send failure
    """

    if not await send_msg(channel=message.channel, msg_string=msg_string):
        await fail_reaction(message=message)