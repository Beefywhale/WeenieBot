import modules.commands as commands
import aiohttp
import asyncio

'''parsing and cleaning raw html for custom google search'''
async def g_search_custom(message, client, search):
    loop = asyncio.get_event_loop()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    search = search.replace(' ', '+')
    async with aiohttp.get('https://www.google.com/search?q={}&start=1&num=1'.format(search), headers=headers) as gr:
        try: 
            from BeautifulSoup import BeautifulSoup
        except ImportError:
            from bs4 import BeautifulSoup
        html = await gr.text()
        results = []
        parsed_html = BeautifulSoup(html, "html.parser")
        for item in parsed_html.find_all('h3', attrs={'class': 'r'}):
            results.append(str(item.a['href']).replace('/url?q=', '').split('&sa=U&ved=')[0])
    await client.send_message(message.channel, 'Top result for `{}`: '.format(search) + ''.join(results[0]))

'''searches google'''
async def search_google(message, client):
    search_google = message.content.replace(message.content.split()[0] + ' ', '')
    await g_search_custom(message, client, search_google)
commands.add_command(command_name='google', command_function=search_google, alias='search')