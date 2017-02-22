'''Admin commands'''
import modules.commands as commands
import json
import discord
import re
import asyncio

with open("database/adminweenie.json","r") as infile:
    admin = json.loads(infile.read())

with open("database/warn.json","r") as infile:
    warnings = json.loads(infile.read())    
    
'''Clear/Removes a given amount of messages.'''
async def clear_logic(message, client):
    if message.author.permissions_in(message.channel).manage_messages:
        try:
            amount = message.content.split(' ')
            amount_number = amount[1]
            amount = int(amount_number) + 1
            print(message.author.name + ' cleared {} messages'.format(amount))
            deleted = await client.purge_from(message.channel, limit=int(amount), check=None)
            await asyncio.sleep(1)
            tbd = await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))
            await asyncio.sleep(8)
            await client.delete_message(tbd)
        except ValueError:
            await client.send_message(message.channel, 'Error, Did you specify number?')
    else:
        await client.send_message(message.channel, 'You need manage messages permission on this server, to use this commands')
commands.add_command(command_name='clear', command_function=clear_logic)

async def warning_add(message, client):
    if message.author.permissions_in(message.channel).ban_members:
        person = re.sub('[!@<>]', '', message.content)
        person = person.replace('warn', '')
        print(person)
        if person not in warnings:
            warnings[person] = []
        warnings[person].append(message.content.split(person)[1])
        if len(warnings[person]) > 3:
            if len(warnings[person]) > 2:
                await client.send_message(message.server.get_member(person), message.content.split(person)[1])
            else:
                await client.send_message(message.server.get_member(person), message.content.split(person)[1])
                await client.send_message(message.channel, 'The next warning this person gets will result in a ban!')
        else:
            await client.send_message(message.server.get_member(person), message.content.split(person)[1])
            await client.send_message(message.channel, 'Banning is not added yet! D:')
    else:
        await client.send_message(message.channel, '`ban_members` permission is needed for this command!')
commands.add_command(command_name='warn', command_function=warning_add)

async def warning_amount(message, client):
    person = message.content.strip('<>@!')
    if person in warnings:
        await client.send_message(message.channel, '\n'.join(warnings[person]))
    else:
        await client.send_message(message.channel, 'That person has no warnings!')
commands.add_command(command_name='warnings', command_function=warning_amount, alias='warns')
        
async def admintest_logic(message, client):
    if str(message.author.id) in admin:
        await client.send_message(message.channel, 'Hello Admin!')
    elif str(message.author.id) not in admin:
        await client.send_message(message.channel, 'Not Admin!')
commands.add_command(command_name='admintest', command_function=admintest_logic, alias='testadmin, admin')


'''Deletes Admin.'''
async def deladmin_logic(message, client):
    try:
        del_admin = str(message.content.replace(message.content.split()[0] + ' ', ''))
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
             await client.send_message(message.channel, 'ERROR You are not Admin.  If you would like to get admin please contact ' + client.bot_info.owner.id)
    except:
        pass
commands.add_command(command_name='deladmin', command_function=deladmin_logic, alias='admindel, removeadmin, remove_admin')


'''Adds Admin.'''
async def add_admin_logic(message, client):
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
        await client.send_message(message.channel, 'ERROR You are not Admin. If you would like to get admin please contact ' + client.bot_info.owner.id)
commands.add_command(command_name='addadmin', command_function=add_admin_logic, alias='adminadd')


'''Adds quote.'''
async def quoteadd_logic(message, client):
    if str(message.author.id) in admin:
        msg = message.content.replace(message.content.split()[0] + ' ', '')
        global counter1
        counter1 = len(Quotes_All)
        await client.send_message(message.channel, 'Quote {} Added!'.format(counter1))
        counter1
        counter1 = len(Quotes_All) + 1
        Quotes_All.append(str(len(Quotes_All)) +': ' + msg)
        with open("database/quoteweenie.json", "w+") as outfile:
            outfile.write(json.dumps(Quotes_All))
    elif str(message.author.id) not in admin:
        await client.send_message(message.channel, 'Only Admins can Add Quotes! If you would like to get admin please contact ' + client.bot_info.owner.id)
commands.add_command(command_name='quoteadd', command_function=quoteadd_logic, alias='addquote')


'''Edits quote.'''
async def editquote_logic(message, client):
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
        await client.send_message(message.channel, 'ERROR You are not Admin. If you would like to get admin contact another admin or ' + client.bot_info.owner.id)
commands.add_command(command_name='editquote', command_function=editquote_logic, alias='quoteedit')


'''Deletes quote.'''
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
            await client.send_message(message.channel, 'ERROR You are not Admin. If you would like to get admin please contact ' + client.bot_info.owner.id)
    except:
        pass
commands.add_command(command_name='delquote', command_function=delquote_logic, alias='quotedel')


'''Lists all admins'''
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
commands.add_command(command_name='admins', command_function=admin_amount, alias='adminlist, admin_amount')


'''Purges channel of ALL messages!.'''
async def purge(message, client):
    if str(message.author.id) in admin and message.author.permissions_in(message.channel).manage_messages:
        deleted = await client.purge_from(message.channel, limit=500, check=None)
        await asyncio.sleep(1)
        await client.send_message(message.channel, 'Deleted {} message(s)'.format(len(deleted)))
    elif str(message.author.id) not in admin:
        await client.send_message(message.channel, 'Only Admins can Purge channels!. If you would like to get admin please contact ' + client.bot_info.owner.id)
commands.add_command(command_name='purge', command_function=purge, alias='nuke')
