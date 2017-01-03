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
from datetime import datetime
from google import search

with open("database/AFINN-111.json", "r") as infile:
    words = json.loads(infile.read())

with open("prefix.json", "r") as infile:
    prefix = json.loads(infile.read())

with open("database/storage.json", "r") as outfile:
    storage = json.loads(infile.read())
    
with open("quoteweenie.json","r") as infile:
    Quotes_All = json.loads(infile.read())

with open("adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("database/storage.json", "w+") as outfile:
    outfile.write(json.dumps(storage))    
    
with open("quoteweenie.json", "w+") as outfile:
    outfile.write(json.dumps(Quotes_All))

with open("adminweenie.json", "w+") as outfile:
    outfile.write(json.dumps(admin))

with open("prefix.json", "w+") as outfile:
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
cb1 = cleverbot.Cleverbot()
x33 = '%m-%d-%Y'
def bdel(s, r): return (s[len(r):] if s.startswith(r) else s)
BASE_URL = 'http://pokeapi.co'
open("prefix.json", "r")
start = datetime.now()

async def update_logic(message, client):
    if message.author.name in prefix["bot_owner"] or message.author.id == '146025479692877824':
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
    if message.author.name == prefix["bot_owner"]:
        await client.send_message(message.channel, 'Restarting... Please wait 5-10 seconds before trying to run any commands!')
        os.execl(sys.executable,  sys.executable, *sys.argv)
    else:
        await client.send_message(message.channel, 'ERROR you need to be a bot owner!')

async def broadcast_server(message, client):
    broadcast_message = message.content.replace(client.pfix + 'broadcast', '')
    for server in client.servers:
        try:
            if storage[message.server.id] == "broadcast0" and message.author.name == prefix["bot_owner"]:
                await client.send_message(server.default_channel, broadcast_message)
        except discord.Forbidden:
            if storage[message.server.id] == "broadcast0"  and message.author.name == prefix["bot_owner"]:
                await client.send_message(message.channel, server.name + ' couldn\'t send broadcast!')
        
async def broadcast_server_toggle(message, client):
    if message.content.split(' ')[1] == 'off':
        if message.author == client.server.owner:
            storage[message.server.id] = "broadcast1"
            await client.send_message(message.channel, "you set broadcasts off!")
    if message.content.split(' ')[1] == 'on':
        if message.author == client.server.owner:
            storage[message.server.id] = "broadcast0"
            await client.send_message(message.channel, "you set broadcasts on!")
        
        
async def bot_account(message, client):
    if message.author.name == prefix["bot_owner"]:
        botaccount = True
        bot_say_input = input('Beefywhale: ')
        await client.send_message(message.channel, bot_say_input)
        if bot_say_input in 'endbot':
            if message.author.name == prefix["bot_owner"]:
                botaccount = False
                print('Exited')   
        else:
            await bot_account(message, client)

async def cancel_bot_account(message, client):
    if message.author.name == prefix["bot_owner"]:
        botaccount = False
        print('Exited')    
async def help_logic(message, client):
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        help_details = discord.Embed(title='Commands:', description='', colour=int(rr, 16))
        help_details.add_field(name='__**Quotes**:__', value='\n'+
    '\n' + client.pfix + 'quote --- picks a random quote to tell everyone.\n'+
    '\n' + client.pfix + 'quote <number> --- picks a specific quote to tell everyone.\n'+
    '\n' + client.pfix + 'quoteadd --- adds a new quote\n'+
    '\n' + client.pfix + 'delquote <number> --- deletes specific quote\n'+
    '\n' + client.pfix + 'editquote <number> --- next message you send changes the quote you specified\n', inline=True)


        help_details.add_field(name='__**Random**:__', value='\n'+
    '\n' + client.pfix + 'support --- links to weeniebot\'s support channel! \n'+
    '\n' + client.pfix + 'sleep --- bot goes to sleep for 5 seconds.\n'+
    '\n' + client.pfix + 'jfgi --- just fucking google it.\n'+
    '\n' + client.pfix + 'googlefight <entry 1> <entry 2> --- generates a google fight link too see what is searched more.(use + for spaces EX: !googlefight Space+Jam Smash+Mouth)\n'+
    '\n' + client.pfix + 'messages --- tells you how many messages there are in the channel you are in.\n'+
    '\n' + client.pfix + 'cat --- random cat picture!.\n', inline=True)


        help_details.add_field(name='__**Admin**:__', value='\n'+
    '\n' + client.pfix + 'admintest --- check if you are admin!\n'+
    '\n' + client.pfix + 'deladmin --- deletes admin by user name.\n'+
    '\n' + client.pfix + 'addadmin <Persons Discord Name> --- adds admin by user name.\n'+
    '\n' + client.pfix + 'clear <number> --- clears a given amount of messages.\n', inline=True)

        
        help_details.add_field(name='__**Bot Owner**:__', value='\n'+
    '\n' + client.pfix + 'update --- updates bot to newest version! (do this frequently!!!)\n'+
    '\n' + client.pfix + 'eval --- evaluates code in python\n', inline=True)

        help_details.add_field(name='__**WeenieBot**:__', value='\n'+
    '\n' + 'hello weeniebot --- bot greets you.\n'+
    '\n' + client.pfix + 'WeenieBot <question> --- asks weeniebot a question, that he will do his best to answer :)\n', inline=True)

        help_details.set_author(name=message.server.me, icon_url=message.server.me.avatar_url)
        await client.send_message(message.channel, '**I\'ve private messaged you my help!**')
        await client.send_message(message.author, embed=help_details)

async def support(message, client):
    await client.send_message(message.channel, 'Check out my support channel if you need help, have questions or suggestions! https://discord.gg/5VcPZMj')
        
async def ping_logic(message, client):
    await client.send_message(message.channel, 'Pong')

async def suspend_logic(message, client):
    if message.author.name in prefix["bot_owner"]:
        client.suspend = True
        await client.send_message(message.channel, 'Commands Suspended!')
    else:
        await client.send_message(message.channel, 'Error couldn\'t suspend , maybe you aren\'t bot owner? ')

async def resume_logic(message, client):
    if message.author.name in prefix["bot_owner"]:
        client.suspend = False
        await client.send_message(message.channel, 'Commands Resumed!')
    else:
        await client.send_message(message.channel, 'Error couldn\'t resume, maybe you aren\'t bot owner?')

async def clear(message, client):
    if message.author.name in admin:
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
    elif message.author.name not in admin:
        await client.send_message(message.channel, 'Only Admins can Clear channels! If you would like to get admin please contact beefywhale#5424')

        

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
    open("adminweenie.json","r")
    if message.author.name in admin:
        await client.send_message(message.channel, 'Hello Admin!')
    elif message.author.name not in admin:
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
    a_details.set_footer(text='Made in Python3.5+ with discord.py library!', icon_url='http://findicons.com/files/icons/2804/plex/512/python.png')
    a_details.set_image(url=message.server.me.avatar_url)
    a_details.set_author(name=message.server.me, icon_url=message.server.me.avatar_url)
    await client.send_message(message.channel, embed=a_details)

async def eval_logic(message, client):
    if message.author.name in prefix["bot_owner"] or message.author.id in ['146025479692877824', '160567046642335746']:
        print(message.author.name + ': ' + message.content)
        try:
            evalt = message.content.replace(client.pfix + 'eval ', '')
            if len(str(eval(evalt))) >= 2000:
                await client.send_message(message.channel, '```Python\n' + str(eval(evalt))[:1950] + '```' + '__Truncated!__')
            else:
                await client.send_message(message.channel, '```Python\n' + str(eval(evalt)) + '```')
        except Exception as x:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            messagex = template.format(str(type(x).__name__), str(x))
            await client.send_message(message.channel, '''```Python
''' + messagex + '```')
            
async def eval_logic_block(message, client):
    if message.author.name in prefix["bot_owner"]:
        try:
            evalt = message.content.replace(client.pfix + 'evalt ', '')
            await client.send_message(message.channel, str(eval(evalt)))
            print(message.author.name + ': ' + message.content)
        except Exception as x:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            messagex = template.format(str(type(x).__name__), str(x))
            await client.send_message(message.channel, '''```Python
''' + messagex + '```')

async def delquote_logic(message, client):
    open("quoteweenie.json", "r")
    try:
        del_q = message.content.split(' ')
        del_quote = int(del_q[1])
        if message.author.name in admin:
            try:
                await client.send_message(message.channel, 'Quote {} Deleted'.format(del_quote))
                del Quotes_All[del_quote]
                with open("quoteweenie.json", "w+") as outfile:
                    outfile.write(json.dumps(Quotes_All))
            except IndexError:
                 await client.send_message(message.channel, 'That quote doesn\'t exist!')
        elif message.author.name not in admin:
            await client.send_message(message.channel, 'ERROR You are not Admin. If you would like to get admin please contact beefywhale#5424')
    except:
        pass

async def prefix_logic(message, client):
    if message.author.name == prefix["bot_owner"]:
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
    open("adminweenie.json","r")
    try:
        del_admin = str(message.content.replace(client.pfix + 'deladmin ', ''))
        if message.author.name in admin:
            if del_admin in admin:
                await client.send_message(message.channel, 'Admin Removed')
                admin.remove(del_admin)
                with open("adminweenie.json", "w+") as outfile:
                    outfile.write(json.dumps(admin))
            else:
                await client.send_message(message.channel, 'ERROR {} was never an Admin!'.format('`' + del_admin + '`'))
        elif message.author.name not in admin:
             await client.send_message(message.channel, 'ERROR You are not Admin.  If you would like to get admin please contact beefywhale#5424')
    except:
        pass

async def quote_logic(message, client):
    if message.content.split(' ')[0] == client.pfix + 'quote':
        open("quoteweenie.json", "r")
        try:
            try:
                q_number = message.content.split(' ')
                quote_number = int(q_number[1])
                print(quote_number)
                if message.server.id == '242887866730938378':
                    await client.send_message(message.channel, Quotes_All[quote_number])
                else:
                    await client.send_message(message.channel, Quotes_All[quote_number - 1])
            except IndexError:
                await client.send_message(message.channel, 'That quote doesn\'t exist!')
        except ValueError:
            pass

async def rand_quote(message, client):
    if message.content == client.pfix + 'quote':
        random_quote = random.randint(0, len(Quotes_All) - 1)
        await client.send_message(message.channel, (Quotes_All[random_quote]))

async def editquote_logic(message, client):
    open("quoteweenie.json", "r")
    e_quote = message.content.split(' ')
    edit_quote = int(e_quote[1])
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
        await client.send_message(message.channel, 'ERROR You are not Admin.  If you would like to get admin please contact beefywhale#5424')

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
    open("adminweenie.json","r")
    if message.author.name in admin:
        await client.send_message(message.channel, 'Type the ID you want to make admin. WARNING once someone has access to admin they can do commands like Clear! Becareful and add admins at your own expense!')
        msg3 = await client.wait_for_message(author=message.author)
        await client.send_message(message.channel, 'Admin Added')
        admin.append(msg3.content)
        with open("adminweenie.json", "w+") as outfile:
            outfile.write(json.dumps(admin))
    elif message.author.name not in admin:
        await client.send_message(message.channel, 'ERROR You are not Admin. If you would like to get admin please contact beefywhale#5424')

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
    if message.author.name in admin:
        deleted = await client.purge_from(message.channel, limit=500, check=None)
        await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))
    elif message.author.name not in admin:
        await client.send_message(message.channel, 'Only Admins can Purge channels!. If you would like to get admin please contact beefywhale#5424')

async def sleep(message, client):
    tmp = await client.send_message(message.channel, 'ZzzzzzzZZzzzz...')
    await asyncio.sleep(5)
    await client.edit_message(tmp, 'Done sleeping')

async def cooldown(message, client, num):
    await asyncio.sleep(num)
    client.timer = 0

async def quoteadd_logic(message, client):
    open("quoteweenie.json","r")
    if message.author.name in admin:
        msg = message.content.replace(client.pfix + 'quoteadd', '')
        global counter1
        counter1 = len(Quotes_All)
        await client.send_message(message.channel, 'Quote {} Added!'.format(counter1))
        counter1
        counter1 = len(Quotes_All) + 1
        if message.server.id == '242887866730938378':
            Quotes_All.append(str(len(Quotes_All)) +': ' + msg)
        else:
            Quotes_All.append(str(len(Quotes_All) + 1) +': ' + msg)
        with open("quoteweenie.json", "w+") as outfile:
            outfile.write(json.dumps(Quotes_All))
    elif message.author.name not in admin:
        await client.send_message(message.channel, 'Only Admins can Add Quotes! If you would like to get admin please contact beefywhale#5424')

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
    open("quoteweenie.json","r")
    global counter2
    counter2 = len(Quotes_All)
    if message.server.id == '242887866730938378':
        counter2 = str(len(Quotes_All) - 1)
        await client.send_message(message.channel, message.author.mention + ' ' + 'There Are {} Quotes!'.format(counter2))
    else:
        await client.send_message(message.channel, message.author.mention + ' ' + 'There Are {} Quotes!'.format(counter2))
        
async def admin_amount(message, client):
    open("quoteweenie.json","r")
    await client.send_message(message.channel, message.author.mention + ' ' + 'Admins {}'.format(', '.join(admin)))

async def user(message, client):
    if message.content.startswith(client.pfix + 'user'):
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        try:
            username = message.content.replace(client.pfix + 'user ', '')
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
                print(username)
                await client.send_message(message.channel, 'Invalid User Name')
cmdDict = {
  "support": support,  
  "uptime": uptime,
  "afinn": afinn_logic,
  "admintest": admintest,
  "say": say,
  "prefix": get_prefix,
  "hotdog": hotdog,
  "about": about,
  "eval": eval_logic,
  "setbroadcast": broadcast_server_toggle
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
  "messages": user_messages,
  "google": google_search,
  "quotes": quote_amount,
  "admins": admin_amount,
  "user": user,
  "ping": ping_logic,
  "restart": restart_logic,
  "update": update_logic,
  "suspend": suspend_logic,
  "help": help_logic,
  "clear": clear,
  "enterbot": bot_account,
  "endbot": cancel_bot_account,
  "evalt": eval_logic_block,
  "server": server_info,
  "dog": dog,
  "broadcast": broadcast_server
}
