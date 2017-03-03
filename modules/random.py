'''Random and Fun Commands!'''
import modules.commands as commands
import aiohttp
import re
import json
import asyncio

alphabet = list('abcdefghijklmnopqrstuvwxyz')
wingdings = '♋︎ ♌︎ ♍︎ ♎︎ ♏︎ ♐︎ ♑︎ ♒︎ ♓︎ &︎ &︎ ●︎ ❍︎ ■︎ □︎ ◻︎ ❑︎ ❒︎ ⬧︎ ⧫︎ ◆︎ ❖︎ ⬥︎ ⌧︎ ⍓︎ ⌘︎'.split()
'''Just F#cking Google it!'''
async def jfgi(message, client):
    await client.send_message(message.channel, 'http://www.justfuckinggoogleit.com/')
commands.add_command(command_name='jfgi', command_function=jfgi)


''';)'''
async def hotdog(message, client):
    await client.send_message(message.channel, ':hotdog: '*10)
commands.add_command(command_name='hotdog', command_function=hotdog)


'''Ceaser Cipher encoder/decoder.'''
async def ccipher(message, client):
    if message.content.split()[1] == 'e':
        encode = True
    elif message.content.split()[1] == 'd':
        encode = False
    else:
        await client.send_message(message.channel, 'You didn\'t specify a mode!')

    key = message.content.split()[2]

    try:
        phrase = re.search(r'.+\s+[ed]\s+[0-9]+\s+(.+)', message.content).group(1)
    except:
        pass
    x = ''
    for i in phrase:
        if i.lower() in alphabet:
            if encode is True:
                word = alphabet.index(i.lower()) + int(key)
            elif encode is False:
                word = alphabet.index(i.lower()) - int(key)
            x += alphabet[word % len(alphabet)]
        else:
            x += i
    await client.send_message(message.channel, x)
commands.add_command(command_name='ccipher', command_function=ccipher, alias='ceasercipher')

async def wingdingcipher(message, client):
    phrase = ' '.join(message.content.split()[1:])
    print('Phrase: ' + phrase)
    x = ''
    for i in phrase:
        if i.lower() in alphabet:
            word = alphabet.index(i.lower())
            x += '\\' + wingdings[word]
    await client.send_message(message.channel, x)
    print(x)
commands.add_command(command_name='wingding', command_function=wingdingcipher, alias='wd')


'''Compare two search results.'''
async def google_fight(message, client):
    fight = message.content.replace(message.content.split()[0],'')
    result = fight.split(' ')
    await client.send_message(message.channel, 'http://www.googlefight.com/{}-vs-{}.php'.format(result[1], result[2]))
    print(result[1])
    print(result[2])
commands.add_command(command_name='googlefight', command_function=google_fight, alias='gfight')


'''Random dog picture!'''
async def dog(message, client):
    data = 'http://random.dog/woof'
    loop = asyncio.get_event_loop()
    async with aiohttp.get(data) as dogr:
        if dogr.status == 200:
            dog = await dogr.read()
            dog = dog.decode()
            print(str(dog))
            await client.send_message(message.channel, 'http://random.dog/' + str(dog))
commands.add_command(command_name='dog', command_function=dog, alias='dawg, pupper, doggy')


'''Get a Minecraft servers info.'''
async def minecraft(message, client):        
    r = lambda: random.randint(0,255)
    rr = ('0x%02X%02X%02X' % (r(),r(),r()))
    loop = asyncio.get_event_loop()
    mc_server = message.content.replace(message.content.split()[0] + ' ', '')
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
commands.add_command(command_name='minecraft', command_function=minecraft, alias='mc')


'''Random Cat picture.'''
async def cats(message, client):
    loop = asyncio.get_event_loop()
    async with aiohttp.get('http://random.cat/meow') as catr:
        if catr.status == 200:
            js = await catr.json()
            await client.send_message(message.channel, js['file'])
commands.add_command(command_name='cat', command_function=cats, alias='kitty, meow')
