'''Owner commands'''
import modules.commands as commands
import os
import json
import git
import sys
import asyncio

with open("database/adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("database/storage.json", "r") as infile:
    storage = json.loads(infile.read())

with open("database/storage2.json", "r") as infile:
    storage2 = json.loads(infile.read())

'''Restart bot.'''
async def restart_logic(message, client):
    if message.author.id == client.bot_info.owner.id:
        await client.send_message(message.channel, 'Restarting... Please wait 5-10 seconds before trying to run any commands!')
        os.execl(sys.executable,  sys.executable, *sys.argv)
    else:
        await client.send_message(message.channel, 'ERROR you need to be a bot owner!')
commands.add_command(command_name='restart', command_function=restart_logic, alias='reset, reload')


'''Update bot from github(only works if git cloned! working on a fix).'''
async def update_logic(message, client):
    if message.author.id in client.bot_info.owner.id:
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
commands.add_command(command_name='update', command_function=update_logic, alias='upgrade ')


'''Broadcast a message to ALL servers the bot is in.'''
async def broadcast_server(message, client):
    broadcast_message = message.content.replace(message.content.split()[0] + ' ', '')
    for server in client.servers[:]:
        try:
            if storage[message.server.id] == "broadcast0" and message.author.id == client.bot_info.owner.id:
                await client.send_message(server.default_channel, broadcast_message)
        except discord.Forbidden:
            if storage[message.server.id] == "broadcast0"  and message.author.id == client.bot_info.owner.id:
                await client.send_message(message.channel, server.name + ' couldn\'t send broadcast!')
commands.add_command(command_name='broadcast', command_function=broadcast_server)


'''Toggle if Broadcast will message current server.'''
async def broadcast_server_toggle(message, client):
    if message.content.split(' ')[1] == 'off':
        if message.author.id == message.server.owner.id or message.author.id == client.bot_info.owner.id:
            storage[message.server.id] = "broadcast1"
            await client.send_message(message.channel, "you set broadcasts off!")
    if message.content.split(' ')[1] == 'on':
        if message.author.id == message.server.owner.id or message.author.id == client.bot_info.owner.id:
            storage[message.server.id] = "broadcast0"
            await client.send_message(message.channel, "you set broadcasts on!")
    with open("database/storage.json", "w+") as outfile:
        outfile.write(json.dumps(storage))    
commands.add_command(command_name='set_broadcast', command_function=broadcast_server_toggle, alias='setbroadcast, broadcastset, broadcast_set')


'''Toggle if the bot will welcome new people.'''
async def welcome_msg_toggle(message, client):
    if message.content.split(' ')[1] == 'off':
        if message.author.id == message.server.owner.id or message.author.id == client.bot_info.owner.id:
            storage2[message.server.id] = "message1"
            await client.send_message(message.channel, "you set welcome message off!")
    if message.content.split(' ')[1] == 'on':
        if message.author.id == message.server.owner.id or message.author.id == client.bot_info.owner.id:
            storage2[message.server.id] = "message0"
            await client.send_message(message.channel, "you set welcome message on!")
    with open("database/storage2.json", "w+") as outfile:
        outfile.write(json.dumps(storage2))
commands.add_command(command_name='set_welcome_msg', command_function=broadcast_server_toggle, alias='setwelcomemsg, welcomeset')

'''Suspend commands.'''
async def suspend_logic(message, client):
    if message.author.id == client.bot_info.owner.id:
        client.suspend = True
        await client.send_message(message.channel, 'Commands Suspended!')
    else:
        await client.send_message(message.channel, 'Error couldn\'t suspend , maybe you aren\'t bot owner? ')
commands.add_command(command_name='suspend', command_function=suspend_logic)


'''Resume commands.'''
async def resume_logic(message, client):
    if message.author.id == client.bot_info.owner.id:
        client.suspend = False
        await client.send_message(message.channel, 'Commands Resumed!')
    else:
        await client.send_message(message.channel, 'Error couldn\'t resume, maybe you aren\'t bot owner?')
commands.add_command(command_name='resume', command_function=resume_logic)


'''runs python code.'''
async def eval_logic(message, client):
    if str(message.author.id) in client.bot_info.owner.id:
        print(str(message.author) + ': ' + message.content)
        try:
            evalt = message.content.replace(message.content.split()[0] + ' ', '')
            if len(str(eval(evalt))) >= 2000:
                await client.send_message(message.channel, '```Python\n' + str(eval(evalt))[:1990] + '```' + '__Truncated!__')
            else:
                await client.send_message(message.channel, '```Python\n' + str(eval(evalt)) + '```')
        except Exception as x:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            messagex = template.format(str(type(x).__name__), str(x))
            await client.send_message(message.channel, '''```Python
''' + messagex + '```')
commands.add_command(command_name='eval', command_function=eval_logic, alias='run, shell')


'''runs python code in a loop.'''
async def repl_logic(message, client):
    if str(message.author.id) in client.bot_info.owner.id:
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
commands.add_command(command_name='repl', command_function=repl_logic)


'''run python code, not in a code block.'''
async def eval_clean_logic(message, client):
    if str(message.author.id) in client.bot_info.owner.id:
        try:
            evalt = message.content.replace(message.content.split()[0] + ' ', '')
            await client.send_message(message.channel, str(eval(evalt)))
            print(str(message.author.id) + ': ' + message.content)
        except Exception as x:
            template = "An exception of type {0} occured. Arguments:\n{1!r}"
            messagex = template.format(str(type(x).__name__), str(x))
            await client.send_message(message.channel, '''```Python
''' + messagex + '```')
commands.add_command(command_name='eval_clean', command_function=eval_clean_logic, alias='run_clean, shell_clean')
