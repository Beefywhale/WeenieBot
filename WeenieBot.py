import discord
import asyncio
import cleverbot 
import random
import json
import time


with open("quoteweenie.json","r") as infile:
    Quotes_All = json.loads(infile.read())

with open("adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("quoteweenie.json", "w+") as outfile:
   outfile.write(json.dumps(Quotes_All))      
with open("adminweenie.json", "w+") as outfile:
    outfile.write(json.dumps(admin))                              

counter1 = len(Quotes_All)
counter2 = len(Quotes_All) - 1
timer = 0
client = discord.Client()
cb1 = cleverbot.Cleverbot()

async def cleverbot_logic(message):
    global cb1
    question = str(message.content.strip('weeniebot '))
    answer = cb1.ask(question)
    await client.send_message(message.channel, message.author.mention + ' ' + answer)

async def add_admin_logic(message):
    if message.author.name in admin:
        await client.send_message(message.channel, 'Type the ID you want to make admin.')
        msg3 = await client.wait_for_message(author=message.author)
        await client.send_message(message.channel, 'Admin Added')
        admin.append(msg3.content)
        with open("adminweenie.json", "w+") as outfile:
            outfile.write(json.dumps(admin))  
    elif message.author.name not in admin:
        await client.send_message(message.channel, 'ERROR You are not Admin')

async def purge(message):
    if message.author.name in admin:
        deleted = await client.purge_from(message.channel, limit=500, check=None)
        await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))
    elif message.author.name not in admin:
        await client.send_message(message.channel, 'Only Admins can Purge channels!')
        
async def sleep(message):
    tmp = await client.send_message(message.channel, 'ZzzzzzzZZzzzz...')
    await asyncio.sleep(5)
    await client.edit_message(tmp, 'Done sleeping')

async def cooldown(message):
    await client.send_message(message.author, '10 second Command Cooldown please be patient and don\'t spam commands! :)')
    await asyncio.sleep(8)
    timer = 0
    
async def rand_quote(message):
    random_quote = random.randint(0, len(Quotes_All) - 1)
    await client.send_message(message.channel, (Quotes_All[random_quote]))
    timer = 1
    
async def quoteadd_logic(message):
    if message.author.name in admin:
            await client.send_message(message.channel, 'Type quote to add.')
            test = await client.wait_for_message(author=message.author)
            global counter1
            counter1 = len(Quotes_All)
            await client.send_message(message.channel, 'Quote {} Added!'.format(counter1))
            counter1
            counter1 = len(Quotes_All)
            Quotes_All.append(test.content)        
            with open("quoteweenie.json", "w+") as outfile:
                outfile.write(json.dumps(Quotes_All))  
    elif message.author.name not in admin:
        await client.send_message(message.channel, 'Only Admins can Add Quotes!')
            
async def user_messages(message):
    counter = 0
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    async for log in client.logs_from(message.channel, limit=500):
        if log.author == message.author:
            counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
            print(counter)
        
async def quote_amount(message):
    global counter2
    counter2 = len(Quotes_All) - 1
    await client.send_message(message.channel, message.author.mention + ' ' + 'There Are {} Quotes!'.format(counter2))

async def admin_amount(message):
    if message.author.name in admin:
        await client.send_message(message.channel, message.author.mention + ' ' + 'Admins {}'.format(admin))    
    
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
async def on_message(message):
    global timer
    await client.change_nickname(message.server.me, 'WeenieBot')
    if message.content.lower().startswith('weeniebot'):
        await cleverbot_logic(message)

    if message.content == '!messages':
        await user_messages(message)
    
    if message.content == '!purge':
        await pure(message)
        
    if message.content == '!admins':
        await admin_amount(message)
    
    if message.content == '!good?':
        await client.send_message(message.channel, 'I am as Fit as a Fiddle!')        
        
    if message.content.startswith('!sleep'):
        await sleep(message)         

    if message.content == '!quotenumber':
        await quote_amount(message)

    if timer == 0 and message.content == '!turtles':
        await client.send_message(message.channel, 'https://www.youtube.com/watch?v=o4PBYRN-ndI')
        timer = 1
    elif  timer == 1 and message.content == '!turtles':
        cooldown(message)

    if message.content == '!quoteadd': 
        await quoteadd_logic(message)

    
    if timer == 0 and message.content == '!quote':
        await rand_quote(message)
    elif  timer == 1 and message.content == '!quote':
        await cooldown(message)
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
    
    
    if message.content.lower() == 'hello weeniebot':
        await client.send_message(message.channel, message.author.mention + ' ' + 'Hello! I am WeenieBot, your robot friend, here to help you with your needs on this server! type !help to see what I can do for you!')
    
    if message.content == '!addadmin':
        await add_admin_logic(message)
    
    if message.content.startswith('!deladmin'):
        try:
            del_admin = str(message.content.strip('!deladmin '))
            if message.author.name in admin:
                await client.send_message(message.channel, 'Admin Removed')
                admin.remove(del_admin)  
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
        await client.send_message(message.channel, '''```[Command List]
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
WeenieBot <question> --- asks weeniebot a question, that he will do his best to answer :)```''')



client.run('Your-Bot-Token-Here!')
