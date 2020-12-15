import sqlitebck
from core.setup import *
from functions import *
import asyncio


async def Auto_task(bot):
    guild = bot.guilds[0]

    AdminRole = guild.get_role(db['Admin'])
    while True:
        if 21 <= now_time_info('hour') <= 23 or 0 <= now_time_info('hour') <= 6:
            data.execute('SELECT Id, Status FROM account;')
            Accs = data.fetchall()

            for acc in Accs:
                user = await guild.fetch_member(acc[0])
                if acc[1] == 1:
                    await user.add_roles(AdminRole)
                elif acc[1] == 0:
                    await user.remove_roles(AdminRole)
            await getChannel('_Report').send(f'[Update]Guild logined member admin role. {now_time_info("whole")}')

        # db backup
        temp_file = open('dyn_setting.json', mode='r', encoding='utf8')
        dyn = json.load(temp_file)
        temp_file.close()

        if dyn['ldbh'] != now_time_info('hour'):
            file_name = 'db_backup/' + str(now_time_info('hour')) + '_backup.db'
            bck_db_conn = sqlite3.connect(file_name)
            await asyncio.sleep(20)
            sqlitebck.copy(connection, bck_db_conn)

            dyn['ldbh'] = now_time_info('hour')

            temp_file = open('dyn_setting.json', mode='w', encoding='utf8')
            json.dump(dyn, temp_file)
            temp_file.close()

        await asyncio.sleep(600)
