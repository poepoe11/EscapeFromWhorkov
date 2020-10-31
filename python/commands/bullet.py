from commands import icommand
from requests_html import HTMLSession
from utils import util as UTILS


def get_cmd_class():
    return BulletCmd()


class BulletCmd(icommand.WhorkovCmd):
    def __init__(self):
        super(BulletCmd, self).__init__()
        self.cmd_string_long = "bullet"
        self.cmd_string_short = "b"

        # empty bullets dict
        self.bullets = {}

        self.load_bullets()

    async def execute_cmd(self, arg_str, message):

        bullet_to_find = arg_str

        print(f"Finding ballistics info for bullet: {arg_str}")

        bullets_found = self.get_bullet(bullet_to_find)

        if not bullets_found:
            await message.channel.send("No bullets by that name were found!")
            return

        h2_cols = (
            "Bullet Name",
            "Flesh Damage",
            "Pen Power",
            "Armor damage %",
            "Accuracy %",
            "Recoil %",
            "Frag. Chance",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
        )
        bullets_found.insert(0, h2_cols)

        lens = []
        for col in zip(*bullets_found):
            lens.append(max([len(v) for v in col]))
        template = "  ".join(["|{:<" + str(l) + "}" for l in lens])
        template += "  |"
        top_template = "  ".join([" {:<" + str(l) + "}" for l in lens[0:7]])
        big_l = 0
        for l in lens[6:]:
            big_l += l

        top_template += "  |{:<" + f"{big_l}" + "}   |"
        # assume that your data rows are tuples
        # template = "{:<25}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}|{:<5}"  # column widths: 8, 10, 15, 7, 10

        await UTILS.send_msg(channel=message.channel, msg_string="Ballistics Info:")

        h1_str = top_template.format(
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "Armor Pen Statistics",
        )

        bullet_msg_str = f"```\n{h1_str}\n"
        # await message.channel.send(f"{template.format('Bullet Name', 'Flesh Damage', 'Armor Damage')}")

        for bullet in bullets_found:
            # await message.channel.send(f"{template.format(*bullet)}")
            bullet_msg_str += f"{template.format(*bullet)}\n"

        bullet_msg_str += "```"

        if not await UTILS.send_msg(channel=message.channel, msg_string=bullet_msg_str):
            await UTILS.fail_reaction(message=message)

    def get_bullet(self, bullet_name):
        rtn_bullets = []
        for b_name in self.bullets:
            if bullet_name.lower() in b_name.lower():
                bullet_info = self.bullets[b_name]
                rtn_bullets.append(bullet_info)

        return rtn_bullets

    def load_bullets(self):

        session = HTMLSession()

        r = session.get("https://escapefromtarkov.gamepedia.com/Ballistics")

        ball_tab = r.html.find("table")[2]

        tbody = ball_tab.find("tbody", first=True)
        trows = tbody.find("tr")
        # trows[3].find("td")[1].find("a",first=True).attrs["title"]
        # trows[3].find("td")[1].text

        for i in range(3, len(trows)):
            row_datas = trows[i].find("td")

            col_start = 1

            if row_datas[col_start].find("a", first=True) is None:
                col_start = 0

            title_data = row_datas[col_start]

            # a_data = title_data.find('a',first=True)
            # b_name = a_data.attrs['title']
            b_name = title_data.text
            # print(f"Bullet: {b_name}")

            # flesh_dmg_data = row_datas[col_start + 1]
            # flesh_dmg = flesh_dmg_data.text
            # print(f"Flesh Damage: {flesh_dmg}")

            # armor_dmg_data = row_datas[col_start + 2]
            # armor_dmg = armor_dmg_data.text
            # print(f"Armor Damage: {armor_dmg}")

            vals = []
            for i in range(0, 13):
                vals.append(row_datas[col_start + i].text)

            self.bullets[b_name] = tuple(vals)
