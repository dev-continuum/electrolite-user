import aiohttp
import simplejson
from fastapi import HTTPException, status
from utility.custom_logger import logger


def generate_calling_function(session, calling_method):
    calling_method = calling_method.lower()
    if calling_method == "post":
        return session.post
    elif calling_method == "get":
        return session.get
    elif calling_method == "put":
        return session.put
    elif calling_method == "delete":
        return session.delete


def generate_calling_data(url, params=None, body=None):
    if params and body:
        calling_data = {"url": url, "params": params, "data": simplejson.dumps(body)}
    elif params:
        calling_data = {"url": url, "params": params}
    elif body:
        calling_data = {"url": url, "data": simplejson.dumps(body)}
    else:
        calling_data = {"url": url}
    logger.info(f"calling data is {calling_data}")
    return calling_data


async def make_async_http_request(url, params=None, body=None):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=simplejson.dumps(body)) as resp:
                response = await resp.json()
    except aiohttp.ClientConnectorError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is not available")
    except simplejson.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unable to decode data")
    else:
        return response


async def make_generic_async_http_request(url, params=None, body=None, header=None, calling_method="POST"):
    try:
        async with aiohttp.ClientSession(headers=header) as session:
            async with generate_calling_function(session, calling_method)(
                    **generate_calling_data(url, params, body)) as resp:
                logger.debug(f"Response object received from server {resp}")
                if resp.status == status.HTTP_200_OK:
                    response = resp
                else:
                    raise HTTPException(
                        status_code=resp.status,
                        detail=resp.reason)

    except aiohttp.ClientConnectorError:
        logger.exception("Http client error")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is not available")
    except simplejson.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unable to decode data")
    else:
        return response
