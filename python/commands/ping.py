from commands import icommand

from log import whorkovlogger as LOGGER

logger = LOGGER.get_logger(__name__)


def get_cmd_class():
    return PingCmd()


class PingCmd(icommand.WhorkovCmd):
    def __init__(self):
        super(PingCmd, self).__init__()
        self.cmd_string_long = "ping"
        self.cmd_string_short = "p"

    async def execute_cmd(self, arg_str, message):
        await message.channel.send("pong!")