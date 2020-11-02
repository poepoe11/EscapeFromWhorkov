from commands import icommand
from requests_html import HTMLSession
from log import whorkovlogger as LOGGER
from utils import util as UTILS

logger = LOGGER.get_logger(__name__)


def get_cmd_class():
    return WeaponCaliberCmd()


class WeaponCaliberCmd(icommand.WhorkovCmd):
    def __init__(self):
        super(WeaponCaliberCmd, self).__init__()
        self.cmd_string_long = "weapon_caliber"
        self.cmd_string_short = "wc"

        self.weapon_calibers = {}

        self.load_weapons()

    async def execute_cmd(self, arg_str, message):
        caliber = arg_str

        weapons_list = self.get_weapons(caliber)

        if not weapons_list:
            await message.channel.send("No weapons using that caliber were found!")
            return

        h1_cols = ("Name", "Firing Modes", "Rate of fire")
        weapons_list.insert(0, h1_cols)

        lens = []
        for col in zip(*weapons_list):
            lens.append(max([len(v) for v in col]))
        template = "  ".join(["|{:<" + str(l) + "}" for l in lens])
        template += "  |"

        weapon_msg = "```\n"

        for weapon in weapons_list:
            weapon_msg += f"{template.format(*weapon)}\n"

        weapon_msg += "```"

        if not await UTILS.send_msg(channel=message.channel, msg_string=weapon_msg):
            UTILS.fail_reaction(message=message)

    def get_weapons(self, caliber):
        rtn_weapons = []

        for cal_str in self.weapon_calibers:
            if caliber.lower() in cal_str.lower():
                rtn_weapons += self.weapon_calibers[cal_str]

        return rtn_weapons

    def load_weapons(self):
        session = HTMLSession()

        r = session.get("https://escapefromtarkov.gamepedia.com/Weapons")

        tables = r.html.find("table")

        weapon_tables = range(0, 10)

        for i in weapon_tables:
            weapon_table = tables[i]

            tbody = weapon_table.find("tbody", first=True)

            trows = tbody.find("tr")

            for i in range(1, len(trows)):
                data_cols = [1, 3, 4]
                cal_col = 2

                row_datas = trows[i].find("td")

                if len(row_datas) >= 6:
                    data_cols = [1, 4, 5]
                    cal_col = 3

                col_start = -1

                caliber_data = row_datas[col_start + cal_col]

                caliber = caliber_data.text

                if not caliber:
                    logger.debug("Caliber not found")

                row_vals = []

                for i in data_cols:
                    col_data = (
                        row_datas[col_start + i]
                        .text.replace("\n", ", ")
                        .replace("Single", "S")
                        .replace("Full‑Auto", "A")
                        .replace("3‑round\xa0Burst", "3-rd")
                        .replace("(Pump\xa0action)", "*P")
                        .replace("(Bolt\xa0Action)", "*B")
                        .replace("(Bolt\xa0action)", "*B")
                    )

                    row_vals.append([col_data])

                row_width = 0

                for j in row_vals:
                    row_width = max(row_width, len(j))

                rows = []

                for i in range(0, row_width):
                    vals = []
                    for row in row_vals:
                        if i < len(row):
                            vals.append(row[i])
                        else:
                            vals.append("")
                    rows.append(vals)
                # sep = []
                # for row in row_vals:
                #     sep.append("-")
                # rows.append(sep)

                if caliber not in self.weapon_calibers:
                    self.weapon_calibers[caliber] = []

                for row in rows:
                    self.weapon_calibers[caliber].append(tuple(row))
