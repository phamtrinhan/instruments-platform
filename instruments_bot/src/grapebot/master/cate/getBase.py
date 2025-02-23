import aiohttp
import asyncio
import urllib
import logging
from grapebot.auth import fireant_authorizer
_sem = asyncio.Semaphore(10)
logger = logging.getLogger()
headers_default = {

    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'content-type': 'application/json',
}


async def get_async(session: aiohttp.ClientSession, url, headers=None,
                    data=None, delay=False):

    if delay != False:
        async with _sem:

            if data == None:
                data = {}
            else:
                data = data
            if headers == None:
                headers_to_use = {}
            else:
                headers_to_use = headers
            async with session.get(url=url, allow_redirects=False, timeout=120000,
                                   headers=headers_to_use, json=data) as response:
                resp = await response.read()
                logger.info("Done at " + str(url))

                return resp
    else:
        if data == None:
            data = {}
        else:
            data = data
        if headers == None:
            headers_to_use = {}
        else:
            headers_to_use = headers
        async with session.get(url=url, allow_redirects=False, timeout=120000,
                               headers=headers_to_use, json=data) as response:
            resp = await response.read()

            return resp


async def post_async(session: aiohttp.ClientSession, url, headers=None,
                     data=None, delay=False):

    if delay != False:
        async with _sem:
            if data == None:
                data = {}
            else:
                data = data
            if headers == None:
                headers_to_use = {}
            else:
                headers_to_use = headers
            async with session.post(url=url, allow_redirects=False, timeout=120000,
                                    headers=headers_to_use, json=data) as response:
                resp = await response.read()

            return resp
    else:
        if data == None:
            data = {}
        else:
            data = data
        if headers == None:
            headers_to_use = {}
        else:
            headers_to_use = headers
        async with session.post(url=url, allow_redirects=False, timeout=120000,
                                headers=headers_to_use, json=data) as response:
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


async def getByList_async(urls=[], json_data=[], json_headers=[], delay=False,
                          fireant=False):
    # logger.info(urls)
    if len(urls) == 0:
        raise Exception("URLs is empty! Can't start fetching")
    if len(json_data) < len(urls):
        data = [{} for index in urls]
        new_headers = [headers_default for index in urls]
    else:
        data = json_data
        new_headers = json_headers
    if len(json_headers) < len(urls):
        new_headers = [headers_default for index in urls]

    # logger.info(new_headers)
    if fireant:
        headers_use = fireant_authorizer.get_authorization_header()
    else:
        headers_use = headers_default
    async with aiohttp.ClientSession(headers=headers_use) as session:
        return await asyncio.gather(
            *[get_async(session, urls[A], new_headers[A], data[A], delay)
              for A in range(len(urls))])


async def postByList_async(urls=[], json_data=[], json_headers=[], delay=False,
                           fireant=False):
    # logger.info(urls)
    if len(urls) == 0:
        raise Exception("URLs is empty! Can't start fetching")
    if len(json_data) < len(urls):
        logger.warning("Using default headers. RG: 1")
        data = [{} for index in urls]
        new_headers = [headers_default for index in urls]
    else:
        data = json_data
        new_headers = json_headers
    if len(json_headers) < len(urls):

        logger.warning("Using default headers. RG: 2")
        new_headers = [headers_default for index in urls]

    # logger.info(new_headers)
    if fireant:
        headers_use = fireant_authorizer.get_authorization_header()
    else:
        headers_use = headers_default
    async with aiohttp.ClientSession(headers=headers_use) as session:
        return await asyncio.gather(
            *[post_async(session, urls[A], new_headers[A], data[A], delay)
              for A in range(len(urls))])
