import modules.commands as commands
import aiohttp
import random
import json
import discord
import asyncio

BASE_URL = 'http://pokeapi.co'

async def fetch(session, url):
    with aiohttp.Timeout(10, loop=session.loop):
        async with session.get(url) as response:
            tmp = await response.text()
            return (tmp, response.status)


'''Gets raw data for pokemon!'''
async def getPokemonData2(resource_url, message, client):
    loop = asyncio.get_event_loop()
    async with aiohttp.ClientSession(loop=loop) as session:
        url = '{0}{1}'.format(BASE_URL, resource_url)
        html = await fetch(session, url)
        if html[1] == 200:
            return json.loads(html[0])
        elif html[1] == 524:
            await client.send_message(message.channel, 'PokeAPI Timed Out! Oh No! :scream: Maybe thier website is down? try in a few minutes')


'''gets a random pokemon'''
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
commands.add_command(command_name='pokemon', command_function=randPokemon, alias='pokémon')



'''Gets info on a pokemon name/id/pokedexentry'''
async def getPokemon(message, client):
    try:
        parsedPokemon = message.content.replace(message.content.split()[0] + ' ','')

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
commands.add_command(command_name='pokedex', command_function=getPokemon, alias='pokédex')
