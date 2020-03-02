from aiohttp import web
from colorama import Fore


@web.middleware
async def unhandled_route(request: web.Request, handler: web.RequestHandler) -> web.Response:
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
