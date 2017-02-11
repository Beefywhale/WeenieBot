import modules.commands as commands
import discord
import random
import json
import time
import asyncio

status = {
    'online': 'Online',
    'offline': 'Offline',
    'idle': 'Idle',
    'dnd': 'Do Not Disturb'
}
x33 = '%m-%d-%Y'

'''info about the bot'''
async def about(message, client):
    a_details = discord.Embed(title='About Me', description='', colour=0x1f3A44)
    a_details.add_field(name='Creator\'s Discord Name:', value='Beefywhale#5424', inline=True)
    a_details.add_field(name='Creator\'s GitHub:', value='https://github.com/Beefywhale', inline=True)
    a_details.add_field(name='My Website:', value='https://beefywhale.github.io/WeenieBot/', inline=True)
    a_details.add_field(name='Invite Me:', value='https://tiny.cc/weeniebot', inline=True)
    a_details.add_field(name='Servers I am in:', value=len(client.servers), inline=True)
    a_details.add_field(name='Current Bot Owner:', value=str(client.bot_info.owner), inline=True)
    a_details.set_footer(text='Made in Python3.5+ with discord.py library!', icon_url='http://findicons.com/files/icons/2804/plex/512/python.png')
    a_details.set_image(url=message.server.me.avatar_url)
    a_details.set_author(name=message.server.me, icon_url=message.server.me.avatar_url)
    await client.send_message(message.channel, embed=a_details)
commands.add_command(command_name='about', command_function=about, alias='info')


'''Gets a users info'''
async def user(message, client):
    if message.content.startswith(client.pfix + 'user'):
        r = lambda: random.randint(0,255)
        rr = ('0x%02X%02X%02X' % (r(),r(),r()))
        try:
            username = message.content.replace(message.content.split()[0] + ' ', '')
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
            await client.send_message(message.channel, embed=embed_commands.user_details)

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
commands.add_command(command_name='user', command_function=user)


'''Gets current server info'''
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
commands.add_command(command_name='server', command_function=server_info, alias='server_info, serverinfo')
