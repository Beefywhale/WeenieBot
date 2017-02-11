import discord
import asyncio


#cb1 = cleverbot.Cleverbot('WeenieBot')
cmdDict = {}

def add_command(*, command_name=None, command_function=None, alias=None):
    if alias != None:
        command_final = command_name.lower() + ', ' + alias.lower()
        command_final = command_final.split(', ')
    else:
        command_final = command_name.split()
    cmdDict[tuple(command_final)] = command_function

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
add_command(command_name='help', command_function=help_logic)
    
'''disabled due to new cleverbot api changes'''
'''async def cleverbot_logic(message, client):
    global cb1
    q = message.content.split(' ')
    question = str(q[1:])
    answer = cb1.ask(question)
    await client.send_message(message.channel, message.author.mention + ' ' + answer)
add_command(command_name='weeniebot', command_function=cleverbot_logic, alias='wbot')'''
