from aiohttp import web
from colorama import Fore


@web.middleware
async def unhandled_route(request: web.Request, handler: web.RequestHandler) -> web.Response:
    """
    Middleware responsible for checking if the route requested exists, and prints to console
    if it does not.
    :param request: aiohttp request object
    :param handler: aiohttp request handler
    """

    method = request.method
    route = request.path

    try:
        response = await handler(request)

        if response.status != 404:
            return response

        print(f'{Fore.YELLOW}Unhandled {method} request for {route}')
    except web.HTTPException:
        print(f'{Fore.YELLOW}Unhandled {method} request for {route}')

    return web.json_response({'error': 'Unhandled route'})
