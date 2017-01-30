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
import aiohttp
import re
from datetime import datetime
from google import search
alphabet = list('abcdefghijklmnopqrstuvwxyz')

with open("database/AFINN-111.json", "r") as infile:
    words = json.loads(infile.read())

with open("database/prefix.json", "r") as infile:
    prefix = json.loads(infile.read())

with open("database/storage.json", "r") as infile:
    storage = json.loads(infile.read())

with open("database/storage2.json", "r") as infile:
    storage2 = json.loads(infile.read())
    
with open("database/quoteweenie.json","r") as infile:
    Quotes_All = json.loads(infile.read())

with open("database/adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("database/storage.json", "w+") as outfile:
    outfile.write(json.dumps(storage))    

with open("database/storage2.json", "w+") as outfile:
    outfile.write(json.dumps(storage2))  
    
with open("database/quoteweenie.json", "w+") as outfile:
    outfile.write(json.dumps(Quotes_All))

with open("database/adminweenie.json", "w+") as outfile:
    outfile.write(json.dumps(admin))

with open("database/prefix.json", "w+") as outfile:
    outfile.write(json.dumps(prefix))
    
status = {
    'online': 'Online',
    'offline': 'Offline',
    'idle': 'Idle',
    'dnd': 'Do Not Disturb'
}
botaccount = False
counter1 = len(Quotes_All) + 1
counter2 = len(Quotes_All) + 1
cb1 = cleverbot.Cleverbot('WeenieBot')
x33 = '%m-%d-%Y'
def bdel(s, r): return (s[len(r):] if s.startswith(r) else s)
BASE_URL = 'http://pokeapi.co'
open("database/prefix.json", "r")
start = datetime.now()

async def ccipher(message, client):
    if message.content.split()[1] == 'e':
        encode = True
    elif message.content.split()[1] == 'd':
        encode = False
    else:
        await client.send_message(message.channel, 'You didn\'t specify a mode!')

    key = message.content.split()[2]

    phrase = re.search(r'.+\s+.\s+.\s+(.+)', message.content).group(1)
    x = ''
    for i in phrase:
        if i.lower() in alphabet:
            if encode is True:
                word = alphabet.index(i.lower()) + int(key)
            elif encode is False:
                word = alphabet.index(i.lower()) - int(key)
            x += alphabet[word % len(alphabet)]
            print(x)
        else:
            x += i
        print(x)
    await client.send_message(message.channel, x)

async def update_logic(message, client):
    if str(message.author.id) in str(str(client.bot_info.owner.id)):
        await client.send_message(message.channel, 'Updating...')
        g = git.cmd.Git()
        u = g.pull('-v')
        await client.send_message(message.channel, '```' + str(u) + '```')
        if str(u) == 'Already up-to-date.':
            await client.send_message(message.channel, 'Already Up To Date! Not restarting')
        else:
            await client.send_message(message.channel, 'Update successful restarting!')
            os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        await client.send_message(message.channel, 'Error Didn\'t update maybe you aren\'t an admin?')

async def restart_logic(message, client):
    if str(message.author.id) == str(str(client.bot_info.owner.id)):
        await client.send_message(message.channel, 'Restarting... Please wait 5-10 seconds before trying to run any commands!')
        os.execl(sys.executable,  sys.executable, *sys.argv)
    else:
        await client.send_message(message.channel, 'ERROR you need to be a bot owner!')

async def broadcast_server(message, client):
    broadcast_message = message.content.replace(client.pfix + 'broadcast', '')
    for server in client.servers:
        try:
            if storage[message.server.id] == "broadcast0" and str(message.author.id) == str(str(client.bot_info.owner.id)):
                await client.send_message(server.default_channel, broadcast_message)
        except discord.Forbidden:
            if storage[message.server.id] == "broadcast0"  and str(message.author.id) == str(str(client.bot_info.owner.id)):
                await client.send_message(message.channel, server.name + ' couldn\'t send broadcast!')
        
async def broadcast_server_toggle(message, client):
    if message.content.split(' ')[1] == 'off':
        if message.author.id == message.server.owner or str(message.author.id) == str(str(client.bot_info.owner.id)):
            storage[message.server.id] = "broadcast1"
            await client.send_message(message.channel, "you set broadcasts off!")
    if message.content.split(' ')[1] == 'on':
        if message.author.id == message.server.owner or str(message.author.id) == str(str(str(client.bot_info.owner.id))):
            storage[message.server.id] = "broadcast0"
            await client.send_message(message.channel, "you set broadcasts on!")
    with open("database/storage.json", "w+") as outfile:
        outfile.write(json.dumps(storage))    

async def welcome_msg_toggle(message, client):
    if message.content.split(' ')[1] == 'off':
        if message.author.id == message.server.owner or str(message.author.id) == str(str(str(client.bot_info.owner.id))):
            storage2[message.server.id] = "message1"
            await client.send_message(message.channel, "you set welcome message off!")
    if message.content.split(' ')[1] == 'on':
        if message.author.id == message.server.owner or str(message.author.id) == str(str(str(client.bot_info.owner.id))):
            storage2[message.server.id] = "message0"
            await client.send_message(message.channel, "you set welcome message on!")
    with open("database/storage2.json", "w+") as outfile:
        outfile.write(json.dumps(storage2)) 
        
async def bot_account(message, client):
    if str(message.author.id) == str(str(str(client.bot_info.owner.id))):
        botaccount = True
        bot_say_input = input('Beefywhale: ')
        await client.send_message(message.channel, bot_say_input)
        if bot_say_input in 'endbot':
            if str(message.author.id) == str(str(str(client.bot_info.owner.id))):
                botaccount = False
                print('Exited')   
        else:
            await bot_account(message, client)

async def cancel_bot_account(message, client):
    if str(message.author.id) == str(str(str(client.bot_info.owner.id))):
        botaccount = False
        print('Exited')    
async def help_logic(message, client):
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        help_details = discord.Embed(title='__***Commands***__', description='''
Info Commands
    server --- get info about server
    user <name>--- get's info about a user
    help --- brings up help dialog
    ping --- testing command to see if bot is up!
    admins --- list of all the admins!
    !prefix --- figure out the current command prefix!

Quotes:
    quote --- picks a random quote to tell everyone.
    quote <number> --- picks a specific quote to tell everyone.''', colour=int(rr, 16))
        
        help_details.add_field(name='__***Commands 2:***__', value='''
Random:
    sleep --- bot goes to sleep for 5 seconds.
    jfgi --- just fucking google it.
    messages --- tells you how many messages there are in the channel you are in.
    dog --- random dog picture.
    cat --- random cat picture.
    hotdog --- find out ;)
    ccipher <encode/decode> <key> <phrase> --- Decode/Encode in Ceaser Cipher!
    googlefight <entry 1> <entry 2> --- a link to see what is searched more.(use + for spaces EX: !googlefight Space+Jam Smash+Mouth)

Music/Voice:
    join <channelname> --- Makes bot join specified voice channel.
    play <songname/link/token> --- Bot plays music specified.
    currentsong --- Tells ya current song that it playing.
    volume --- Sets volume. (EX: `!volume 0.5` = 50% voulme.)
    disconnect --- Disconnects bot from current voice channel.
    pause --- Pauses Music.
    unpause -- Unpases Music.''', inline=True)

        
        help_details2 = discord.Embed(title='', description='', colour=int(rr, 16))
        help_details2.add_field(name='__***Commands 3:***__', value='''
Admin:
    clear <number> --- deletes amount of messages specified
    quoteadd --- adds a new quote
    delquote <number> --- deletes specific quote
    editquote <number> --- next message you send changes the quote you specified
    admintest --- check if you are admin!
    deladmin --- deletes admin by user name.
    addadmin <DiscordName#Dicrim> --- adds admin by user name and discrim.

Bot Owner:
    suspend --- suspends ALL commands
    resume --- resume's all commands!
    setprefix <prefix> --- set the prefix for the current server!
    set_welcome_msg <off/on> --- turns welcome message off or on.
    eval --- evaluates some code!
    update --- updates bot to newest version!
    broadcast --- boradcast message to all servers!
    restart --- restarts bot!

WeenieBot:
    hello weeniebot --- bot greets you.
    WeenieBot <question> --- asks weeniebot a question, that he will do his best to answer :smiley:''', inline=True)

        help_details.set_author(name=message.server.me, icon_url=message.server.me.avatar_url)
        await client.send_message(message.channel, '**I\'ve private messaged you my help!**')
        await client.send_message(message.author, embed=help_details)
        await client.send_message(message.author, embed=help_details2)


async def support(message, client):
    await client.send_message(message.channel, 'Check out my support channel if you need help, have questions or suggestions! https://discord.gg/5VcPZMj')
        
async def ping_logic(message, client):
    await client.send_message(message.channel, 'Pong')

async def suspend_logic(message, client):
    if str(message.author.id) in str(str(str(client.bot_info.owner.id))):
        client.suspend = True
        await client.send_message(message.channel, 'Commands Suspended!')
    else:
        await client.send_message(message.channel, 'Error couldn\'t suspend , maybe you aren\'t bot owner? ')
async def resume_logic(message, client):
    if str(message.author.id) in str(str(str(client.bot_info.owner.id))):
        client.suspend = False
        await client.send_message(message.channel, 'Commands Resumed!')
    else:
        await client.send_message(message.channel, 'Error couldn\'t resume, maybe you aren\'t bot owner?')

async def clear(message, client):
    if str(message.author.id) in admin:
        try:
            amount = message.content.split(' ')
            amount_number = amount[1]
            amount = int(amount_number) + 1
            print(message.author.name + ' cleared {} messages'.format(amount))
            deleted = await client.purge_from(message.channel, limit=int(amount), check=None)
            tbd = await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))
            await asyncio.sleep(5)
            await client.delete_message(tbd)

        except ValueError:
            await client.send_message(message.channel, 'Error, Did you specify number?')
    elif str(message.author.id) not in admin:
        await client.send_message(message.channel, 'Only Admins can Clear channels! If you would like to get admin please contact ' + str(str(str(str(client.bot_info.owner.id)))))

        

async def uptime(message, client):
    await client.send_message(message.channel, "I have been awake for: " + str(datetime.now()-start))

async def afinn_logic(message, client):
    if message.content.split(' ')[0] == client.pfix + 'afinn':
        winput = bdel(message.content, client.pfix + "afinn ")
        if winput.lower() in words:
            await client.send_message(message.channel, "Sentiment analysis for " + winput.lower() + " is: " + str(words[winput.lower()]))
        else:
            await client.send_message(message.channel, "That word doesnt have a sentiment analysis!")
            print(winput)

async def admintest(message, client):
    open("database/adminweenie.json","r")
    if str(message.author.id) in admin:
        await client.send_message(message.channel, 'Hello Admin!')
    elif str(message.author.id) not in admin:
        await client.send_message(message.channel, 'Not Admin!')

async def say(message, client):
    if message.content.split(' ')[0] == client.pfix + 'say':
        saying = message.content.replace(client.pfix + 'say', '')
        await client.send_message(message.channel, saying)

async def get_prefix(message, client):
    await client.send_message(message.channel, 'Current command prefix: `' + client.pfix + '`')

async def hotdog(message, client):
    await client.send_message(message.channel, ':hotdog: :hotdog: :hotdog: :hotdog: :hotdog: :hotdog: :hotdog: :hotdog: :hotdog: ')

async def about(message, client):
    a_details = discord.Embed(title='About Me', description='', colour=0x1f3A44)
    a_details.add_field(name='Creator\'s Discord Name:', value='beefywhale#5424', inline=True)
    a_details.add_field(name='Creator\'s GitHub:', value='https://github.com/Beefywhale', inline=True)
    a_details.add_field(name='My Website:', value='https://beefywhale.github.io/WeenieBot/', inline=True)
    a_details.add_field(name='Invite Me:', value='https://tiny.cc/weeniebot', inline=True)
    a_details.add_field(name='People I can see:', value=len([i.name for i in client.get_all_members()]), inline=True)
    a_details.set_footer(text='Made in Python3.5+ with discord.py library!', icon_url='http://findicons.com/files/icons/2804/plex/512/python.png')
    a_details.set_image(url=message.server.me.avatar_url)
    a_details.set_author(name=message.server.me, icon_url=message.server.me.avatar_url)
    await client.send_message(message.channel, embed=a_details)

async def eval_logic(message, client):
    if str(message.author.id) in str(str(str(client.bot_info.owner.id))):
        print(str(message.author) + ': ' + message.content)
        try:
            evalt = message.content.replace(client.pfix + 'eval ', '')
            if len(str(exec(evalt))) >= 2000:
                await client.send_message(message.channel, '```Python\n' + str(eval(evalt))[:1990] + '```' + '__Truncated!__')
            else:
                await client.send_message(message.channel, '```Python\n' + str(eval(evalt)) + '```')
        except Exception as x:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            messagex = template.format(str(type(x).__name__), str(x))
            await client.send_message(message.channel, '''```Python
''' + messagex + '```')


async def repl_logic(message, client):
    if str(message.author.id) in str(str(client.bot_info.owner.id)):
        await client.send_message(message.channel, 'Starting REPL session.')
        client.repl = True
        print(str(message.author) + ': ' + message.content)
        while client.repl is True:
            try:
                evalt = await client.wait_for_message(author=message.author)
                if evalt.content == '|rexit':
                    client.repl = False
                    await client.send_message(message.channel, 'Ending REPL session.')
                elif evalt.content.startswith('|'):
                    if len(str(eval(evalt.content[1:]))) >= 1990:
                        await client.send_message(message.channel, '```Python\n' + str(eval(evalt.content[1:]))[:1950] + '```' + '__Truncated!__')
                    else:
                        await client.send_message(message.channel, '```Python\n' + str(eval(evalt.content[1:])) + '```')
            except Exception as x:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                messagex = template.format(str(type(x).__name__), str(x))
                await client.send_message(message.channel, '''```Python
''' + messagex + '```')            
            
async def eval_logic_block(message, client):
    if str(message.author.id) in str(str(client.bot_info.owner.id)):
        try:
            evalt = message.content.replace(client.pfix + 'evalt ', '')
            await client.send_message(message.channel, str(exec(evalt)))
            print(str(message.author.id) + ': ' + message.content)
        except Exception as x:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            messagex = template.format(str(type(x).__name__), str(x))
            await client.send_message(message.channel, '''```Python
''' + messagex + '```')

async def delquote_logic(message, client):
    open("database/quoteweenie.json", "r")
    try:
        del_q = message.content.split(' ')
        del_quote = int(del_q[1])
        if str(message.author.id) in admin:
            try:
                del Quotes_All[del_quote]
                await client.send_message(message.channel, 'Quote {} Deleted'.format(del_quote))
                with open("database/quoteweenie.json", "w+") as outfile:
                    outfile.write(json.dumps(Quotes_All))
            except IndexError:
                 await client.send_message(message.channel, 'That quote doesn\'t exist!')
        elif str(message.author.id) not in admin:
            await client.send_message(message.channel, 'ERROR You are not Admin. If you would like to get admin please contact ' + str(str(str(client.bot_info.owner.id))))
    except:
        pass

async def prefix_logic(message, client):
    if str(message.author.id) == str(str(str(client.bot_info.owner.id))):
        with open("database/prefixMap.json", "r") as infile:
            prefixMap = json.loads(infile.read())
        print(client.pfix)
        sprefix = bdel(message.content, client.pfix + "setprefix ")
        prefixMap[message.server.id] = sprefix
        await asyncio.sleep(1)
        await client.send_message(message.channel, 'set prefix to' + ' `' + prefixMap[message.server.id] + ' `')
        print(prefixMap[message.server.id])
        with open("database/prefixMap.json", "w+") as outfile:
            outfile.write(json.dumps(prefixMap))
        client.pfix = prefixMap[message.server.id]
        print(prefixMap)


async def deladmin_logic(message, client):
    open("database/adminweenie.json","r")
    try:
        del_admin = str(message.content.replace(client.pfix + 'deladmin ', ''))
        if str(message.author.id) in admin:
            if del_admin in admin:
                deleted_admin = message.server.get_member_named(del_admin)
                await client.send_message(message.channel, 'Admin Removed')
                admin.remove(deleted_admin.id)
                with open("database/adminweenie.json", "w+") as outfile:
                    outfile.write(json.dumps(admin))
            else:
                await client.send_message(message.channel, 'ERROR {} was never an Admin!'.format('`' + del_admin + '`'))
        elif str(message.author.id) not in admin:
             await client.send_message(message.channel, 'ERROR You are not Admin.  If you would like to get admin please contact ' + str(str(str(client.bot_info.owner.id))))
    except:
        pass

async def quote_logic(message, client):
    if message.content.split(' ')[0] == client.pfix + 'quote':
        open("database/quoteweenie.json", "r")
        try:
            try:
                q_number = message.content.split(' ')
                quote_number = int(q_number[1])
                print(quote_number)
                await client.send_message(message.channel, Quotes_All[quote_number])
            except IndexError:
                await client.send_message(message.channel, 'That quote doesn\'t exist!')
        except ValueError:
            pass

async def rand_quote(message, client):
    if message.content == client.pfix + 'quote':
        random_quote = random.randint(0, len(Quotes_All) - 1)
        await client.send_message(message.channel, (Quotes_All[random_quote]))

async def editquote_logic(message, client):
    open("database/quoteweenie.json", "r")
    e_quote = message.content.split(' ')
    edit_quote = int(e_quote[1])
    if str(message.author.id) in admin:
        try:
            await client.send_message(message.channel, 'Editing Quote {}'.format(edit_quote))
            msg = await client.wait_for_message(author=message.author)
            Quotes_All[edit_quote] = msg.content
            await client.send_message(message.channel, 'Quote Edited')
            with open("database/quoteweenie.json", "w+") as outfile:
                outfile.write(json.dumps(Quotes_All))
        except IndexError:
            await client.send_message(message.channel, 'That quote doesn\'t exist!')
    elif str(message.author.id) not in admin:
        await client.send_message(message.channel, 'ERROR You are not Admin. If you would like to get admin contact another admin or ' + str(str(str(client.bot_info.owner.id))))
        
async def cleverbot_logic(message, client):
    global cb1
    q = message.content.split(' ')
    question = str(q[1:])
    answer = cb1.ask(question)
    await client.send_message(message.channel, message.author.mention + ' ' + answer)

async def cleverbot_logictwo(message, client):
    global cb1
    q = message.content.split(' ')
    question = str(q[1:])
    answer = cb1.ask(question)
    await client.send_message(message.channel, message.author.mention + ' ' + answer)

async def add_admin_logic(message, client):
    open("database/adminweenie.json","r")
    if str(message.author.id) in admin:
        username = message.content.split(' ')[1]
        try:
            msg3 = message.server.get_member_named(username)
            await client.send_message(message.channel, msg3.display_name + ' has been added as an admin')
            admin.append(msg3.id)
            with open("database/adminweenie.json", "w+") as outfile:
                outfile.write(json.dumps(admin))
        except:
            await client.send_message(message.channel, 'Could not find user with this name, try doing name#discrim')

    elif str(message.author.id) not in admin:
        await client.send_message(message.channel, 'ERROR You are not Admin. If you would like to get admin please contact ' + str(str(str(client.bot_info.owner.id))))

async def fetch(session, url):
    with aiohttp.Timeout(10, loop=session.loop):
        async with session.get(url) as response:
            tmp = await response.text()
            return (tmp, response.status)

async def getPokemonData2(resource_url, message, client):
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        url = '{0}{1}'.format(BASE_URL, resource_url)
        html = await fetch(session, url)
        if html[1] == 200:
            return json.loads(html[0])
            return None
        elif html[1] == 524:
            await client.send_message(message.channel, 'PokeAPI Timed Out! Oh No! :scream: Maybe thier website is down? try in a few minutes')


async def getPokemonData(resource_url, message, client):
    url = '{0}{1}'.format(BASE_URL, resource_url)
    response = requests.get(url)

    if response.status_code == 200:
        return json.loads(response.text)
    return None

async def randPokemon(message, client):
    parsedPokemon = random.randint(0, 709)
    try:
        pokemon = await getPokemonData2('/api/v1/pokemon/' + str(parsedPokemon), message, client)

        sprite_uri = pokemon['sprites'][0]['resource_uri']
        description_uri = pokemon['descriptions'][0]['resource_uri']
        type_uri = pokemon['types'][0]['resource_uri']


        sprite = await getPokemonData2(sprite_uri, message, client)
        description = await getPokemonData2(description_uri, message, client)
        ptype = await getPokemonData2(type_uri, message, client)

        p_details = discord.Embed(title='', description='', colour=0x1f3A44)
        p_details.add_field(name='Pokemon:', value=pokemon['name'], inline=True)
        p_details.add_field(name='National Pokedex ID:', value=pokemon['national_id'], inline=True)
        p_details.add_field(name='Desc:', value=description['description'], inline=True)
        p_details.add_field(name='Type:', value=ptype['name'], inline=True)
        p_details.add_field(name='Defense:', value=pokemon['defense'], inline=True)
        p_details.add_field(name='Health Points:', value=pokemon['hp'], inline=True)
        p_details.add_field(name='Attack:', value=pokemon['attack'], inline=True)
        p_details.set_footer(text='Made in Python3.5+ with discord.py library!', icon_url='http://findicons.com/files/icons/2804/plex/512/python.png')
        p_details.set_image(url=BASE_URL + sprite['image'])
        p_details.set_author(name=pokemon['name'], icon_url=BASE_URL + sprite['image'])
        if message.server.id not in ['242887866730938378']:
            await client.send_message(message.channel, embed=p_details)
            print(pokemon['name'])
            print(description['description'])
            print(ptype['name'])
            print(pokemon['hp'])
            print(pokemon['defense'])
            print(pokemon['attack'])
            print(pokemon['national_id'])
            print(BASE_URL + sprite['image'])
    except TypeError as e:
        print(e)
        if message.server.id not in ['242887866730938378']:
            await client.send_message(message.channel, 'ERROR {} is not in the Pokedex! Try using all lowercase!'.format(parsedPokemon))


async def getPokemon(message, client):
    try:
        parsedPokemon = message.content.replace(client.pfix + 'pokedex ','')

        pokemon = await getPokemonData2('/api/v1/pokemon/' + parsedPokemon, message, client)

        sprite_uri = pokemon['sprites'][0]['resource_uri']
        description_uri = pokemon['descriptions'][0]['resource_uri']
        type_uri = pokemon['types'][0]['resource_uri']

        sprite = await getPokemonData2(sprite_uri, message, client)
        description = await getPokemonData2(description_uri, message, client)
        ptype = await getPokemonData2(type_uri, message, client)
        p_details = discord.Embed(title='', description='', colour=0x1f3A44)
        p_details.add_field(name='Pokemon:', value=pokemon['name'], inline=True)
        p_details.add_field(name='National Pokedex ID:', value=pokemon['national_id'], inline=True)
        p_details.add_field(name='Desc:', value=description['description'], inline=True)
        p_details.add_field(name='Type:', value=ptype['name'], inline=True)
        p_details.add_field(name='Defense:', value=pokemon['defense'], inline=True)
        p_details.add_field(name='Health Points:', value=pokemon['hp'], inline=True)
        p_details.add_field(name='Attack:', value=pokemon['attack'], inline=True)
        p_details.set_footer(text='Made in Python3.5+ with discord.py library!', icon_url='http://findicons.com/files/icons/2804/plex/512/python.png')
        p_details.set_image(url=BASE_URL + sprite['image'])
        p_details.set_author(name=pokemon['name'], icon_url=BASE_URL + sprite['image'])
        if message.server.id not in ['242887866730938378']:
            await client.send_message(message.channel, embed=p_details)
            print(pokemon['name'])
            print(description['description'])
            print(ptype['name'])
            print(pokemon['hp'])
            print(pokemon['defense'])
            print(pokemon['attack'])
            print(pokemon['national_id'])
            print(BASE_URL + sprite['image'])
    except TypeError:
        if message.server.id not in ['242887866730938378']:
            await client.send_message(message.channel, 'ERROR {} is not in the Pokedex!'.format(parsedPokemon))

async def server_info(message, client):
    r = lambda: random.randint(0,255)
    rr = ('0x%02X%02X%02X' % (r(),r(),r()))
    server_details = discord.Embed(title='', description='', colour=int(rr, 16))
    server_details.add_field(name='Server Name:', value=message.server.name, inline=True)
    server_details.add_field(name='Number of Voice and Text Channel(s):', value=len(message.server.channels), inline =True)
    server_details.add_field(name='Number of Role(s):', value=len(message.server.role_hierarchy), inline=True)
    server_details.add_field(name='Number of User(s):', value=message.server.member_count, inline =True)
    server_details.add_field(name='Server Made:', value=message.server.created_at.strftime(x33), inline =True)
    server_details.add_field(name='Server Owner:', value=message.server.owner, inline=True)
    server_details.add_field(name='Default Channel:', value=message.server.default_channel, inline=True)
    server_details.set_author(name=message.server.name, icon_url=message.server.icon_url)
    server_details.set_image(url=message.server.icon_url)
    await client.send_message(message.channel, embed=server_details)            
            
async def cats(message, client):
    loop = asyncio.get_event_loop()
    async with aiohttp.get('http://random.cat/meow') as catr:
        if catr.status == 200:
            js = await catr.json()
            await client.send_message(message.channel, js['file'])
            
async def LoL_api(message, client):
    summoner_name = message.content.lower().strip(client.pfix + 'lol ')
    loop = asyncio.get_event_loop()
    r = lambda: random.randint(0,255)
    rr = ('0x%02X%02X%02X' % (r(),r(),r()))
    async with aiohttp.get('https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/' + summoner_name + '?api_key=' + prefix["lolKey"]) as lolr:
        if lolr.status == 200:
            js = await lolr.json()
            summoner_details = discord.Embed(title=js[summoner_name.lower()]['name'], description='', colour=int(rr, 16))
            summoner_details.add_field(name='Summoner ID:', value=js[summoner_name.lower()]['id'])
            summoner_details.add_field(name='Summoner Level:', value=js[summoner_name.lower()]['summonerLevel'])
            await client.send_message(message.channel, embed=summoner_details)
        else:
            await client.send_message(message.channel, 'Something went wrong with the API! :scream:')
            
async def minecraft(message, client):        
    r = lambda: random.randint(0,255)
    rr = ('0x%02X%02X%02X' % (r(),r(),r()))
    loop = asyncio.get_event_loop()
    mc_server = message.content.replace(client.pfix + 'minecraft ', '')
    async with aiohttp.get('https://mcapi.us/server/status?ip=' + mc_server) as mcr:
        if mcr.status == 200:
            js = await mcr.json()
            mc_details = discord.Embed(title='', description='', colour=int(rr, 16))
            if js['server']['name'] != '':
                mc_details.add_field(name='Server Version: ', value=js['server']['name'])
            if js['online'] == 'True':
                mc_details.add_field(name='Server Online:', value=':thumbsup:')
            elif js['online'] == 'False':
                mc_details.add_field(name='Server Online:', value=':thumbsdown:')
            
            mc_details.add_field(name='Players:', value=str(js['players']['now']) + '/' + str(js['players']['max']))
            if js['motd'] != '':
                mc_details.add_field(name='Description:', value=js['motd'].replace('§', ''))
            await client.send_message(message.channel, embed=mc_details)
        else:
            await client.send_message(message.channel, 'Something went wrong with the API! :scream:')

            
async def dog(message, client):
    data = 'http://random.dog/woof'
    loop = asyncio.get_event_loop()
    async with aiohttp.get(data) as dogr:
        if dogr.status == 200:
            dog = await dogr.read()
            dog = dog.decode()
            print(str(dog))
            await client.send_message(message.channel, 'http://random.dog/' + str(dog))
            
async def google_Fight(message, client):
    fight = message.content.replace(client.pfix + 'googlefight','')
    result = fight.split(' ')
    await client.send_message(message.channel, 'http://www.googlefight.com/{}-vs-{}.php'.format(result[1], result[2]))
    print(result[1])
    print(result[2])

async def purge(message, client):
    if str(message.author.id) in admin:
        deleted = await client.purge_from(message.channel, limit=500, check=None)
        await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))
    elif str(message.author.id) not in admin:
        await client.send_message(message.channel, 'Only Admins can Purge channels!. If you would like to get admin please contact ' + str(str(str(client.bot_info.owner.id))))

async def sleep(message, client):
    tmp = await client.send_message(message.channel, 'ZzzzzzzZZzzzz...')
    await asyncio.sleep(5)
    await client.edit_message(tmp, 'Done sleeping')

async def cooldown(message, client, num):
    await asyncio.sleep(num)
    client.timer = 0

async def quoteadd_logic(message, client):
    open("database/quoteweenie.json","r")
    if str(message.author.id) in admin:
        msg = message.content.replace(client.pfix + 'quoteadd', '')
        global counter1
        counter1 = len(Quotes_All)
        await client.send_message(message.channel, 'Quote {} Added!'.format(counter1))
        counter1
        counter1 = len(Quotes_All) + 1
        Quotes_All.append(str(len(Quotes_All)) +': ' + msg)
        with open("database/quoteweenie.json", "w+") as outfile:
            outfile.write(json.dumps(Quotes_All))
    elif str(message.author.id) not in admin:
        await client.send_message(message.channel, 'Only Admins can Add Quotes! If you would like to get admin please contact ' + str(str(str(client.bot_info.owner.id))))

async def user_messages(message, client):
    counter = 0
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    async for log in client.logs_from(message.channel, limit=500):
        if log.author == message.author:
            counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
            print(counter)

async def google_search(message, client):
    search_google = message.content.replace(client.pfix + 'google ', '')
    for url in search(search_google, stop=5):
        await client.send_message(message.channel, url)
        break

async def quote_amount(message, client):
    open("database/quoteweenie.json","r")
    global counter2
    counter2 = len(Quotes_All)
    counter2 = str(len(Quotes_All) - 1)
    await client.send_message(message.channel, message.author.mention + ' ' + 'There Are {} Quotes!'.format(counter2))

async def admin_amount(message, client):
    names = []
    ids = []
    for i in admin:
        try:
            user = message.server.get_member(i)
            names.append(user.name)
            ids.append(user.id)
        except:
            names.append('**User not in current server!***')
            ids.append('**User not in current server!***')
    admin_details = discord.Embed(title='Admins', description='', colour=0x79CDCD)
    admin_details.add_field(name='Names:', value='\n'.join(names), inline=True)
    admin_details.add_field(name='ID\'s:', value='\n'.join(ids), inline=False)
    await client.send_message(message.channel, embed=admin_details)

async def user(message, client):
    if message.content.startswith(client.pfix + 'user'):
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        try:
            username = message.content.replace(client.pfix + 'user ', '')
            roles_member = message.server.get_member_named(username).roles
            user_details = discord.Embed(title='', description='', colour=int(rr, 16))
            user_details.add_field(name='Username:', value=message.server.get_member_named(username).name, inline=True)
            user_details.add_field(name='Nick:', value=message.server.get_member_named(username).nick, inline =True)
            user_details.add_field(name='Current Status:', value=status[str(message.server.get_member_named(username).status)], inline=True)
            user_details.add_field(name='Playing:', value=message.server.get_member_named(username).game, inline =True)
            user_details.add_field(name='Joined Server:', value=message.server.get_member_named(username).joined_at.strftime(x33), inline =True)
            user_details.add_field(name='User Roles:', value= ', '.join([i.name.replace('@', '') for i in roles_member]), inline=True)
            user_details.add_field(name='Account Created:', value=message.server.get_member_named(username).created_at.strftime(x33), inline=True)
            user_details.set_author(name=message.server.get_member_named(username).display_name, icon_url=message.server.get_member_named(username).avatar_url)
            await client.send_message(message.channel, embed=user_details)

        except AttributeError:
            if message.content == client.pfix + 'user':
                roles_member = message.author.roles
                user_details = discord.Embed(title='', description='', colour=int(rr, 16))
                user_details.add_field(name='Username:', value=message.author.name, inline=True)
                user_details.add_field(name='Nick:', value=message.author.nick, inline =True)
                user_details.add_field(name='Current Status:', value=status[str(message.author.status)], inline=True)
                user_details.add_field(name='Playing:', value=message.author.game, inline =True)
                user_details.add_field(name='Joined Server:', value=message.author.joined_at.strftime(x33), inline =True)
                user_details.add_field(name='User Roles:', value= ', '.join([i.name.replace('@', '') for i in roles_member]), inline=True)
                user_details.add_field(name='Account Created:', value=message.author.created_at.strftime(x33), inline=True)
                user_details.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                await client.send_message(message.channel, embed=user_details)
            else:
                await client.send_message(message.channel, 'Invalid User Name')
cmdDict = {
  "support": support,
  "uptime": uptime,
  "afinn": afinn_logic,
  "admintest": admintest,
  "say": say,
  "set_welcome_msg": welcome_msg_toggle,
  "prefix": get_prefix,
  "hotdog": hotdog,
  "about": about,
  "eval": eval_logic,
  "set_broadcast": broadcast_server_toggle,
  "delquote": delquote_logic,
  "setprefix": prefix_logic,
  "deladmin": deladmin_logic,
  "editquote": editquote_logic,
  "addadmin": add_admin_logic,
  "pokemon": randPokemon,
  "pokedex": getPokemon,
  "cat": cats,
  "googlefight": google_Fight,
  "sleep": sleep,
  "quoteadd": quoteadd_logic,
  "lol": LoL_api,
  "messages": user_messages,
  "google": google_search,
  "repl": repl_logic,
  "quotes": quote_amount,
  "admins": admin_amount,
  "user": user,
  "ping": ping_logic,
  "restart": restart_logic,
  "update": update_logic,
  "suspend": suspend_logic,
  "help": help_logic,
  "clear": clear,
  "minecraft": minecraft,
  "enterbot": bot_account,
  "endbot": cancel_bot_account,
  "evalt": eval_logic_block,
  "server": server_info,
  "dog": dog,
  "ccipher": ccipher,
  "broadcast": broadcast_server
}
