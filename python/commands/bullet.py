from commands import icommand
from requests_html import HTMLSession

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
        bullets_found = self.get_bullet(bullet_to_find)

        if not bullets_found:
            await message.channel.send("No bullets by that name were found!")
            return

        # assume that your data rows are tuples
        template = "{:<25}|{:<15}|{:<15}" # column widths: 8, 10, 15, 7, 10

        await message.channel.send("Ballistics Info:")

        bullet_msg_str = f"```\n{template.format('Bullet Name', 'Flesh Damage', 'Armor Damage')}\n"
        #await message.channel.send(f"{template.format('Bullet Name', 'Flesh Damage', 'Armor Damage')}")

        for bullet in bullets_found:
            #await message.channel.send(f"{template.format(*bullet)}")
            bullet_msg_str += f"{template.format(*bullet)}\n"
        
        bullet_msg_str += "```"

        await message.channel.send(bullet_msg_str)

    def get_bullet(self, bullet_name):
        rtn_bullets = []
        for b_name in self.bullets:
            if bullet_name.lower() in b_name.lower():
                bullet_info = (b_name, self.bullets[b_name]["flesh_dmg"], self.bullets[b_name]["armor_dmg"])
                rtn_bullets.append(bullet_info)

        return rtn_bullets

      

    def load_bullets(self):

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
            
            #a_data = title_data.find('a',first=True)
            #b_name = a_data.attrs['title']
            b_name = title_data.text
            print(f"Bullet: {b_name}")

            flesh_dmg_data = row_datas[col_start + 1]
            flesh_dmg = flesh_dmg_data.text
            print(f"Flesh Damage: {flesh_dmg}")

            armor_dmg_data = row_datas[col_start + 2]
            armor_dmg = armor_dmg_data.text
            print(f"Armor Damage: {armor_dmg}")

            self.bullets[b_name] = {"flesh_dmg":flesh_dmg, "armor_dmg":armor_dmg}