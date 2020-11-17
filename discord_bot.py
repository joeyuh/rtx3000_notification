import os
import json
import discord
import asyncio
import datetime

if os.path.exists('config.json'):
    with open('config.json', 'r') as f:
        settings = json.load(f)
else:
    raise Exception('MISSING config.json')

UPTIME_NOTIFICATION_INTERVAL = 15
TOKEN = settings['discord_token']
GUILD = settings['discord_guild']
LOCAL_TIME_ZONE = str(datetime.datetime.now().astimezone().tzinfo)

client = discord.Client()
start_time = datetime.datetime.now()
alert_count = 0


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


async def uptime():
    await client.wait_until_ready()
    global alert_count
    while True:
        for channel in client.get_all_channels():
            if channel.name == 'uptime':
                delta = datetime.datetime.now() - start_time
                await channel.send(f'Bot is up! Last {UPTIME_NOTIFICATION_INTERVAL} minutes: {alert_count} alerts\n'
                                   f'Last startup: {start_time.isoformat()} {LOCAL_TIME_ZONE} \n'
                                   f'Total uptime {strfdelta(delta, "{days} days {hours} hours {minutes} minutes {seconds} seconds")}')
                alert_count = 0
        await asyncio.sleep(UPTIME_NOTIFICATION_INTERVAL * 60)


async def alert_task():
    await client.wait_until_ready()
    global alert_count

    while True:
        links = []

        if os.path.exists('history.json'):
            with open('history.json') as f:
                alert = json.load(f)

            for link in alert:
                if not alert[link]['discord_alerted']:
                    links.append(link)  # We haven't alert, add to links
                    alert_count += 1
                    alert[link]['discord_alerted'] = True  # We alerted

            for link in links:
                for channel in client.get_all_channels():
                    if isinstance(channel, discord.TextChannel):
                        if ''.join(i for i in channel.name if i.isdigit()) in link:
                            await channel.send(
                                f'ALERT: {channel.name}, {link}\nTime: {alert[link]["time"]} {LOCAL_TIME_ZONE}')

            with open('history.json', 'w') as f:
                json.dump(alert, f, indent=4)
        await asyncio.sleep(1)  # task runs every 1 seconds


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    for channel in client.get_all_channels():
        if channel.name == 'uptime':
            await channel.send(f'Bot restarted at {start_time.isoformat()} {LOCAL_TIME_ZONE} \n')


def main():
    client.loop.create_task(uptime())
    client.loop.create_task(alert_task())
    client.run(TOKEN)


if __name__ == '__main__':
    main()
