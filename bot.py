import discord
import asyncio
import random
import time
import sqlite3
import os
from datetime import datetime, timedelta
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
from discord.utils import get
from discord import FFmpegPCMAudio

bot = commands.Bot(command_prefix='.')

channelid = None
user_notify = []
conn = sqlite3.connect(':memory:')
c = conn.cursor()
c.execute('''CREATE TABLE ramadan
             (date text, FEJR text, DHUHR text, ASSER text, MAGHREB text, ICHA text)''')

dates = [('2019-05-18', '04:08:00', '13:48:00', '17:57:00', '21:32:00', '23:09:00'),
             ('2019-05-19', '04:06:00', '13:48:00', '17:57:00', '21:34:00', '23:10:00'),
             ('2019-05-20', '04:04:00', '13:48:00', '17:57:00', '21:35:00', '23:12:00'),
             ('2019-05-21', '04:02:00', '13:48:00', '17:57:00', '21:36:00', '23:14:00'),
             ('2019-05-22', '04:00:00', '13:48:00', '17:57:00', '21:38:00', '23:16:00'),
             ('2019-05-23', '03:58:00', '13:48:00', '17:57:00', '21:39:00', '23:17:00'),
             ('2019-05-24', '03:56:00', '13:48:00', '18:00:00', '21:40:00', '23:19:00'),
             ('2019-05-25', '03:55:00', '13:48:00', '18:00:00', '21:41:00', '23:21:00'),
             ('2019-05-26', '03:53:00', '13:48:00', '18:00:00', '21:42:00', '23:22:00'),
             ('2019-05-27', '03:51:00', '13:49:00', '18:01:00', '21:43:00', '23:24:00'),
             ('2019-05-28', '03:50:00', '13:49:00', '18:01:00', '21:45:00', '23:26:00'),
             ('2019-05-29', '03:48:00', '13:49:00', '18:02:00', '21:46:00', '23:27:00'),
             ('2019-05-30', '03:47:00', '13:49:00', '18:02:00', '21:47:00', '23:29:00'),
             ('2019-05-31', '03:45:00', '13:49:00', '18:03:00', '21:48:00', '23:30:00'),
             ('2019-05-01', '03:44:00', '13:49:00', '18:03:00', '21:49:00', '23:32:00'),
             ('2019-06-02', '03:42:00', '13:49:00', '18:03:00', '21:50:00', '23:33:00'),
             ('2019-06-03', '03:41:00', '13:50:00', '18:04:00', '21:51:00', '23:34:00'),
             ('2019-06-04', '03:40:00', '13:50:00', '18:04:00', '21:51:00', '23:36:00'),
             ('2019-06-05', '03:39:00', '13:50:00', '18:04:00', '21:52:00', '23:37:00'),
            ]

c.executemany('INSERT INTO ramadan VALUES (?,?,?,?,?,?)', dates)


                    
@bot.event
async def on_ready():
    print('Bot is on')
                    
                    
@bot.command()
async def stime(ctx):
    if ctx.message.author.guild_permissions.administrator:
        now = datetime.now() + timedelta(hours=2)
        await ctx.send(now.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        await ctx.send('fdp ta pas la perm')
    
@bot.command()
async def clear(ctx, args):
    try:
        amount = int(args)
    except:
        pass
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=amount)
        await ctx.send(str(amount)+' message.s supprimé.s')

    else:
        await ctx.send('fdp ta pas la perm')
    
        
@bot.command()
async def notify(ctx, choice):
    try:
        if choice == 'add':
            try:
                assert('<@'+str(ctx.author.id)+'>' not in user_notify)
                user_notify.append('<@'+str(ctx.author.id)+'>')
                await ctx.send(':heavy_plus_sign: Added to notify')
            except :
                await ctx.send(":no_entry: Vous êtes déjà inscrit à la notification, ramadan mubarak mon khey. :no_entry:")
        elif choice == 'remove':
            try:
                user_notify.remove('<@'+str(ctx.author.id)+'>')
                await ctx.send(':heavy_minus_sign: Removed from notify')
            except ValueError:
                await ctx.send(":no_entry: Vous n'êtes pas inscrit à la notification, ramadan mubarak mon khey. :no_entry:")
    except:
        await ctx.send(":no_entry: Connard. :no_entry:")
    

@bot.command()
async def here(ctx):
    if ctx.message.author.guild_permissions.administrator:
        global channelid
        channelid = ctx.channel.id
        await ctx.send('Le bot travaillera ici')
    else:
        await ctx.send('fdp ta pas la perm')
        
@bot.command()
async def test(ctx):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send(user_notify)
    else:
        await ctx.send('fdp ta pas la perm')
    
#@bot.command()
#async def send(ctx):
#    for user in user_notify:
#        await ctx.send('Coucou %s' %user)
                        
                    
@bot.command()
async def insertdate(ctx, DATE, FEJR, DHUHR, ASSER, MAGHREB, ICHA):
    if ctx.message.author.guild_permissions.administrator:
        c.execute("INSERT INTO ramadan VALUES ('{}','{}','{}','{}','{}','{}')".format(DATE, FEJR, DHUHR, ASSER, MAGHREB, ICHA))
        conn.commit()
    else:
        await ctx.send('fdp ta pas la perm')
    
@bot.command()
async def updatedate(ctx, n1, n2, n3):
    if ctx.message.author.guild_permissions.administrator:
        c.execute("UPDATE ramadan SET '{}' = '{}' WHERE date = '{}'".format(n1,n2,n3))
        await ctx.send('modifié ta mère')
    else:
        await ctx.send('fdp ta pas la perm')
        
@bot.command()
async def roulette(ctx):
    rand = random.uniform(0, 1)*100
    await ctx.send('Si le numéro tiré au sort est > à 50 tu es kick')
    await ctx.send('Et le numéro est ...')
    await ctx.send(int(rand))
    if rand > 50:
        await ctx.author.kick()
        await ctx.send('Dommage :(')
    else:
        await ctx.send('La chance :)')
    await ctx.channel.purge(limit=5)
    
@bot.command()
async def connect(ctx):
	if not discord.opus.is_loaded():
	# the 'opus' library here is opus.dll on windows
	# or libopus.so on linux in the current directory
	# you should replace this with the location the
	# opus library is located in and with the proper filename.
	# note that on windows this DLL is automatically provided for you
		discord.opus.load_opus('opus.dll')
	
    if ctx.message.author.guild_permissions.administrator:
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send("You are not connected to a voice channel")
            return
        voice = get(bot.voice_clients)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
    else:
        await ctx.send('fdp ta pas la perm')
        
@bot.command()
async def selectall(ctx):
    if ctx.message.author.guild_permissions.administrator:
        s = ""
        try:
            for row in c.execute('SELECT * FROM ramadan'):
                s+=str(row)+"\n"
            await ctx.send(s)
        except:
            await ctx.send('Table vide.')
    else:
        await ctx.send('fdp ta pas la perm')
        
@bot.command()
async def ping(ctx):
    await ctx.send('Pong')  
    
async def ramadan():
    await bot.wait_until_ready()
    
    while True:
            await asyncio.sleep(1)
            global channelid
            channel = bot.get_channel(channelid)
            while channelid != None:
                userL = ""
                ligne_jour = []
                now = datetime.now() + timedelta(hours=2)
                date = now.strftime("%Y-%m-%d")
                c.execute('SELECT * FROM ramadan WHERE date=?', [date])
                for LJ in c.fetchone():
                    ligne_jour.append(LJ)
                while now.strftime("%H:%M:%S") != "23:59:59":
                    await asyncio.sleep(0.5)
                    for x in ligne_jour[1:]:
                        now = datetime.now() + timedelta(hours=2)
                        if now.strftime("%H:%M:%S") == x:
                            await asyncio.sleep(1)
                            for user in user_notify:
                                userL += user+" "
                            s = ("Il est "+now.strftime("%H:%M:%S")+", et c'est l'heure du"+" "+str(ligne_jour.index(x))+" "+userL)
                            await channel.send(s.replace(' 1 ', ' FEJR :pray: ').replace(' 2 ', ' DHUHR :pray: ').replace(' 3 ', ' ASSER :pray: ').replace(' 4 ', ' MAGHREB :pray: ').replace(' 5 ', ' ICHA :pray: '))                            
                            userL = ""
                            source = FFmpegPCMAudio('allah3.mp3')
                            player = voice.play(source)
    
bot.loop.create_task(ramadan())
bot.run(os.getenv('BOT_TOKEN'))
