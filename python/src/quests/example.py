from aiohttp import web

from log import Log


async def example_quest(request: web.Request, player) -> web.Response:
    """
    Example quest handler that handles a POST request with a computer science trivia question

    :param request: The request object
    :param player: The player object
    """

    # Verify that it is a POST request, since that's what this quest is supposed to handle
    if request.method == 'POST':
        # We will always get JSON from the server, so convert it to a Python dict
        data = request.json()

        # Let's see what the server is asking
        print(data)

        # Ok so we know that the question is "Who invented C++?"
        # The request always contains a "msg" field, and the response always expects a "msg" field
        response = { 'msg': 'bjarne stroustrup' }

        # The server always expects a JSON response
        return web.json_response(response)
    else:
        Log.error('This quest is supposed to handle POST requests')