'''
данный код представляет собой часть веб парсера сайта inoriginal
так как удобно подавать в строку запроса аргументы
aiohttp.client_exceptions.ClientConnectorError:
 Cannot connect to host inoriginal.online:443 ssl:default [None]
'''
import aiohttp
import asyncio

async def web_parser(args):
    link = f'https://inoriginal.online/?story={args}&do=search&subaction=search'
    print(link)

    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(link) as response:
            return await response.text()

async def main():
    result = await web_parser('мадагаскар')
    print(result)

if __name__ == "__main__":
    asyncio.run(main())



import requests
from bs4 import BeautifulSoup 

def web_parser():
    link = 'https://www.kinopoisk.ru/film/89514/'
    print(link)

    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

result = web_parser()
print(result)
