'''Misc. commands!'''
import modules.commands as commands
import random
import json
import time
from datetime import datetime
import asyncio

with open("database/quoteweenie.json","r") as infile:
    Quotes_All = json.loads(infile.read())
with open("database/AFINN-111.json", "r") as infile:
    words = json.loads(infile.read())

t = time.process_time()
counter1 = len(Quotes_All) + 1
counter2 = len(Quotes_All) + 1
def bdel(s, r): return (s[len(r):] if s.startswith(r) else s)


'''A simple ping testing command.'''
async def ping_logic(message, client):
    await client.send_message(message.channel, 'Pong')
commands.add_command(command_name='ping', command_function=ping_logic, alias='test')

'''Gets bots current uptime.'''
async def uptime_logic(message, client):
    await client.send_message(message.channel, "I have been awake for: " + elapsed_time = time.process_time() - t)
commands.add_command(command_name='uptime', command_function=uptime_logic)


'''Gets sentiment analysis for a word in the AFINN-111 database'''
async def afinn_logic(message, client):
    winput = bdel(message.content, message.content.split()[0] + ' ')
    if winput.lower() in words:
        await client.send_message(message.channel, "Sentiment analysis for " + winput.lower() + " is: " + str(words[winput.lower()]))
    else:
        await client.send_message(message.channel, "That word doesnt have a sentiment analysis!")
        print(winput)
commands.add_command(command_name='afinn', command_function=afinn_logic, alias='se')


'''Bot repeats what you give it.'''
async def say_logic(message, client):
    saying = message.content.replace(message.content.split()[0] + '', '')
    await client.send_message(message.channel, saying)
commands.add_command(command_name='say', command_function=say_logic)


'''Gets current prefix.'''
async def get_prefix_logic(message, client):
    await client.send_message(message.channel, 'Current command prefix: `' + client.pfix + '`')
commands.add_command(command_name='prefix', command_function=get_prefix_logic)


'''Change current prefix'''
async def prefix_logic(message, client):
    if message.author.id == client.bot_info.owner.id or message.author.id == message.server.owner.id:
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
commands.add_command(command_name='set_prefix', command_function=prefix_logic, alias='setprefix, prefixset')


'''Gets specified quote'''
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


'''Gets a random quote'''
async def rand_quote(message, client):
    random_quote = random.randint(0, len(Quotes_All) - 1)
    await client.send_message(message.channel, (Quotes_All[random_quote]))


'''Current amount of quotes'''
async def quote_amount(message, client):
    global counter2
    counter2 = len(Quotes_All)
    counter2 = str(len(Quotes_All) - 1)
    await client.send_message(message.channel, message.author.mention + ' ' + 'There Are {} Quotes!'.format(counter2))
commands.add_command(command_name='quotes', command_function=quote_amount, alias='quotelist')
