# https://github.com/Rapptz/discord.py/blob/async/examples/reply.py
import discord
import time
import asyncio

# from discord.ext import commands

token = 'NDQ4NTQzNjgwNDU0ODUyNjI4.DeZPaw.RHAWgz1vmD2B_uq7-4HtJuf--Tw'
client = discord.Client()

retweeted_messages = []

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # purging
    # if message.content.startswith('!purge '):
    #     isMod = False
    #     for r in message.author.roles:
    #         if r.name == 'Fisting Fairy' or r.name == 'Here is my Glamour Luke':
    #             isMod = True
    #     if isMod:
    #         try:
    #             number = int(message.content[7:])
    #             await client.purge_from(message.channel, limit=number)
    #         except ValueError:
    #             msg = 'Enter a real number, you fucking idiot'.format(message)
    #             await client.send_message(message.channel, msg)
    #     else:
    #         msg = 'Nice try, baby bitch'.format(message)
    #         await client.send_message(message.channel, msg)

    # auto-replies
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!die'):
        msg = 'Oh :('.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('!hendy'):
        msg = 'NO'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith('?google') or message.content.startswith('!google'):
        msg = 'Bots can\'t use Google anymore, you dumb bitch'.format(message)
        await client.send_message(message.channel, msg)

    # if message.content.startswith('!birthday'): #!birthday YYYY-mm-dd
    #     msg = '{0.author.mention}\'s birthday recorded.'.format(message)
    #     await client.send_message(message.channel, msg)

async def check_for_retweets():
    await client.wait_until_ready()
    try:
        while not client.is_closed:
            print(time.time() % 60)
            # file = open('retweeted_messages.txt', 'r+')
            # retweeted_messages = []
            # for m in file.readlines():
            #     retweeted_messages.append(m.strip())
            new_messages = []
            new_messages_timestamps = []
            new_messages_rcount = []
            #get all messages with the proper number of retweet emojis
            for c in client.get_all_channels():
                async for m in client.logs_from(client.get_channel(c.id), limit=100000):
                    for r in m.reactions:
                        if r.custom_emoji:
                            if r.emoji.name == 'retweet' and r.count > 2 and m.id not in retweeted_messages \
                                    and m.author != client.user:
                                new_messages.append(m)
                                new_messages_timestamps.append(m.timestamp)
                                new_messages_rcount.append(r.count)
            #post messages in order of timestamp
            timestamps_order = sorted(range(len(new_messages_timestamps)), key=lambda k: new_messages_timestamps[k]) # indices of sorted
            for index in timestamps_order:
                m = new_messages[index]
                msg = '<:retweet:449394937541427230> x ' + str(new_messages_rcount[index])
                em = discord.Embed(description=m.content, colour=0000000)
                if m.author.nick is None:
                    nickname = m.author.name
                    em.set_author(name=nickname, icon_url=m.author.avatar_url)
                else:
                    nickname = m.author.nick
                    em.set_author(name=nickname, icon_url=m.author.avatar_url)
                if len(m.attachments) > 0:
                    image_url = m.attachments[0].get('url')
                    em.set_image(url=image_url)
                else:
                    if len(m.embeds) > 0:
                        image_url = m.embeds[0].get('url')
                        em.set_image(url=image_url)
                em.set_footer(text="#" + m.channel.name)
                print(m.content)
                print(m.id)
                retweeted_messages.append(m.id)
                await client.send_message(client.get_channel('448621029930303488'),
                                          msg,
                                          embed=em)
                #
                # 449644920412831755
            print('Sleeping')
            await asyncio.sleep(60)  # task runs every 60 seconds
    except Exception:
        print(Exception.with_traceback())
        await asyncio.sleep(60)

@client.event
async def on_ready():
    file = open('retweeted_messages.txt', 'r+')
    for m in file.readlines():
        retweeted_messages.append(m.strip())

    # new_messages = []
    # for c in client.get_all_channels():
    #     async for m in client.logs_from(client.get_channel(c.id), limit = 100000):
    #         for r in m.reactions:
    #             if r.custom_emoji:
    #                 if r.emoji.name == 'retweet' and r.count > 2 and m.id not in retweeted_messages:
    #                     #new_messages.append(m.id)
    #                     print(m.content)
    #                     print(m.id)
    #
    #                     #451474931801128968
    # for m in new_messages:
    #     file.write(m + '\n')
    # file.close()

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    # for x in client.get_all_channels():
    #     print(x)
    #     print(x.id)
    print('------')

client.loop.create_task(check_for_retweets())

client.run(token)
