import aiohttp
import asyncio
import urllib
import logging
from grapebot.auth import fireant_authorizer

_sem = asyncio.Semaphore(8)
logger = logging.getLogger()
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}


async def get_async(session: aiohttp.ClientSession, url, headers=None,
        data=None, delay=False):
    async with _sem:
        if delay != False:
            await asyncio.sleep(delay)
        if data == None:
            data = {}
        if headers == None:
            headers_to_use = {}
        
        async with session.get(url=url, allow_redirects=False, timeout=12,
                               headers=headers, json=data) as response:
            resp = await response.read()
        
        return resp


def getSingle(url):
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers = {'User-Agent': user_agent}
    request = urllib.request.Request(url, None,
                                     headers)  # The assembled request
    response = urllib.request.urlopen(request)
    # print(url)
    data = response.read()
    
    return data


async def getByList_async(urls = [], json_data=[], json_headers=[], delay=False,
        fireant=False):
    if len(urls):
        raise Exception("URLs is empty! Can't start fetching")
    if len(json_data) < len(urls):
        data = [None for index in range(len(urls))]
        new_headers = [headers for index in range(len(urls))]
    if fireant:
        headers_use = fireant_authorizer.get_authorization_header()
    else:
        headers_use = headers
    async with aiohttp.ClientSession(headers=headers_use) as session:
        return await asyncio.gather(
                *[get_async(session, urls[url_index], new_headers[url_index],
                            data[url_index],
                            delay, data)
                  for url_index in range(len(urls)) ])
        
        
        [get_async() for index in range(len(urls))]
        
        # ret = await asyncio.gather(*[get_async(url) for url in urls])
        # return ret
