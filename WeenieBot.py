import discord
import asyncio
import random
import json
import time
import cleverbot
import requests
import git
import subprocess
import sys
import os
import modules.commands as command
import modules.botToken as botToken
from google import search

#changes! testing updates heehee

with open("quoteweenie.json","r") as infile:
    Quotes_All = json.loads(infile.read())

with open("adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("quoteweenie.json", "w+") as outfile:
    outfile.write(json.dumps(Quotes_All))
with open("adminweenie.json", "w+") as outfile:
    outfile.write(json.dumps(admin))

status = {
    'online': 'Online',
    'offline': 'Offline',
    'idle': 'Idle',
    'dnd': 'Do Not Disturb'
}

x33 = '%m-%d-%Y'

counter1 = len(Quotes_All)
counter2 = len(Quotes_All) - 1
timer = 0
client = discord.Client()
cb1 = cleverbot.Cleverbot()


async def user(message):
    if message.content.startswith('!user'):
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        try:
            username = message.content.replace('!user ', '')
            print(username)
            roles_member = message.server.get_member_named(username).roles
            user_details = discord.Embed(title='', description='', colour=int(rr, 16))
            user_details.add_field(name='Username:', value=message.server.get_member_named(username).name, inline=True)
            user_details.add_field(name='Nick:', value=message.server.get_member_named(username).nick, inline =True)
            user_details.add_field(name='Current Status:', value=status[str(message.server.get_member_named(username).status)], inline=True)
            user_details.add_field(name='Playing:', value=message.server.get_member_named(username).game, inline =True)
            user_details.add_field(name='Joined Server:', value=message.server.get_member_named(username).joined_at.strftime(x33), inline =True)
            user_details.add_field(name='User Roles:', value= ', '.join([i.name.replace('@', '') for i in roles_member]), inline=True)
            user_details.add_field(name='Account Created:', value=message.server.get_member_named(username).created_at.strftime(x33), inline=True)
            user_details.set_footer(text='Made in Python3.5+ with discord.py library!', icon_url='http://findicons.com/files/icons/2804/plex/512/python.png')
            user_details.set_author(name=message.server.get_member_named(username).display_name, icon_url=message.server.get_member_named(username).avatar_url)
            await client.send_message(message.channel, embed=user_details)

        except AttributeError:
            if message.content == '!user':
                roles_member = message.author.roles
                user_details = discord.Embed(title='', description='', colour=int(rr, 16))
                user_details.add_field(name='Username:', value=message.author.name, inline=True)
                user_details.add_field(name='Nick:', value=message.author.nick, inline =True)
                user_details.add_field(name='Current Status:', value=status[str(message.author.status)], inline=True)
                user_details.add_field(name='Playing:', value=message.author.game, inline =True)
                user_details.add_field(name='Joined Server:', value=message.author.joined_at.strftime(x33), inline =True)
                user_details.add_field(name='User Roles:', value= ', '.join([i.name.replace('@', '') for i in roles_member]), inline=True)
                user_details.add_field(name='Account Created:', value=message.author.created_at.strftime(x33), inline=True)
                user_details.set_footer(text='Made in Python3.5+ with discord.py library!', icon_url='http://findicons.com/files/icons/2804/plex/512/python.png')
                user_details.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                await client.send_message(message.channel, embed=user_details)
            else:
                print(username)
                await client.send_message(message.channel, 'Invalid User Name')



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('<Members>')
    for server in client.servers:
        for member in server.members:
            print(member)
    print('------')


@client.event
async def on_member_join(member):
    await client.send_message(member.server.default_channel, "{0.mention} has joined {0.server.name} give them a warm welcome!".format(member))    

@client.event
async def on_message(message):
    global timer
    await client.change_nickname(message.server.me, 'WeenieBot')

    if message.content.lower().startswith('weeniebot'):
        await command.cleverbot_logic(message)

    if message.content == '!messages':
        await command.user_messages(message)

    if message.content == '!purge':
        await purge(message)

    if message.content == '!update':
        g = git.cmd.Git()
        u = g.pull('-v')
        await client.send_message(message.channel, str(u))
        os.execl(sys.executable, sys.executable, *sys.argv)
       
    if message.content.startswith('!user'):
        await command.user(message)

    if message.content == '!admins':
        await command.admin_amount(message)

    if message.content.startswith('!pokemon'):
        await command.getPokemonData(message)

    if message.content.startswith('!google'):
        await command.google_search(message)

    if message.content == '!good?':
        await client.send_message(message.channel, 'I am as Fit as a Fiddle!')
    
    if message.content.startswith('!sleep'):
        await command.sleep(message)

    if message.content == '!quotenumber':
        await command.quote_amount(message)

    if timer == 0 and message.content == '!turtles':
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=o4PBYRN-ndI')
        timer = 1
    elif  timer == 1 and message.content == '!turtles':
        command.cooldown(message)

    if message.content.lower() == 'hello weeniebot':
        await client.send_message(message.channel, message.author.mention + ' ' + 'Hello! I am WeenieBot, your robot friend, here to help you with your needs on this server! type !help to see what I can do for you!')


    if message.content == '!quoteadd':
        await command.quoteadd_logic(message)


    if timer == 0 and message.content == '!quote':
        await command.rand_quote(message)
    elif  timer == 1 and message.content == '!quote':
        await command.cooldown(message)

    if message.content.startswith('!delquote'):
        try:
            del_quote = int(message.content.strip('!delquote '))
            if message.author.name in admin:
                try:
                    await client.send_message(message.channel, 'Quote {} Deleted'.format(del_quote))
                    del Quotes_All[del_quote]
                    with open("quoteweenie.json", "w+") as outfile:
                        outfile.write(json.dumps(Quotes_All))
                except IndexError:
                    await client.send_message(message.channel, 'That quote doesn\'t exist!')
            elif message.author.name not in admin:
                await client.send_message(message.channel, 'ERROR You are not Admin')
        except:
            pass

        if message.content.startswith('!editquote'):
            edit_quote = int(message.content.strip('!editquote '))
            if message.author.name in admin:
                try:
                    await client.send_message(message.channel, 'Editing Quote {}'.format(edit_quote))
                    msg = await client.wait_for_message(author=message.author)
                    Quotes_All[edit_quote] = msg.content
                    await client.send_message(message.channel, 'Quote Edited')
                    with open("quoteweenie.json", "w+") as outfile:
                        outfile.write(json.dumps(Quotes_All))
                except IndexError:
                    await client.send_message(message.channel, 'That quote doesn\'t exist!')
            elif message.author.name not in admin:
                await client.send_message(message.channel, 'ERROR You are not Admin')

    if timer == 0 and message.content.split(' ')[0] == '!quote':
        try:
            try:
                open("quoteweenie.json","r")
                quote_number = int(message.content.strip('!quote '))
                print(quote_number)
                await client.send_message(message.channel, Quotes_All[quote_number])
                timer = 1
                await asyncio.sleep(8)
                timer = 0
            except IndexError:
                await client.send_message(message.channel, 'That quote doesn\'t exist!')
        except ValueError:
            pass
    elif timer == 1 and message.content.split(' ')[0] == '!quote':
        try:
            try:
                quote_number = int(message.content.strip('!quote '))
                print('COOLDOWN')
                await client.send_message(message.author, '10 second Command Cooldown please be patient and don\'t spam commands! :)')
                await asyncio.sleep(2)
                timer = 0
            except ValueError:
                pass
        except IndexError:
            await client.send_message(message.channel, 'That quote doesn\'t exist!')

    if message.content == '!addadmin':
        await command.add_admin_logic(message)

    if message.content.startswith('!deladmin'):
        try:
            del_admin = str(message.content.replace('!deladmin ', ''))
            if message.author.name in admin:
                if del_admin in admin:
                    await client.send_message(message.channel, 'Admin Removed')
                    admin.remove(del_admin)
                    with open("adminweenie.json", "w+") as outfile:
                        outfile.write(json.dumps(admin))
                else:
                    await client.send_message(message.channel, 'ERROR {} was never an Admin!'.format('`' + del_admin + '`'))
            elif message.author.name not in admin:
                await client.send_message(message.channel, 'ERROR You are not Admin')
        except:
            pass

    if message.content.startswith('!admintest'):
        open("adminweenie.json","r")
        if message.author.name in admin:
            await client.send_message(message.channel, 'Hello Admin!')
        elif message.author.name not in admin:
            await client.send_message(message.channel, 'Not Admin!')

    if message.content == '!help':
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        help_details = discord.Embed(title='Commands:', description='''
!quote --- picks a random quote to tell everyone.
!quote <number> --- picks a specific quote to tell everyone.
!quoteadd --- adds a new quote
!delquote <number> --- deletes specific quote
!sleep --- bot goes to sleep for 5 seconds.
!messages --- tells you how many messages there are in the channel you are in.
!admintest --- check if you are admin!
!deladmin --- deletes admin by user id
!addadmin <Persons Discord ID>--- adds admin by user id
hello weeniebot --- bot greets you.
WeenieBot <question> --- asks weeniebot a question, that he will do his best to answer :)''', colour=int(rr, 16))
        help_details.set_author(name=message.server.me, icon_url=message.server.me.avatar_url)
        await client.send_message(message.channel, embed=help_details)



client.run(botToken.token)
