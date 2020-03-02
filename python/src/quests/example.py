from aiohttp import web

from log import Log


async def example_quest(request: web.Request) -> web.Response:
    """
    Example quest handler that handles a POST request with a computer science trivia question

    :param request: The request object
    """

    # Verify that it is a POST request, since that's what this quest is supposed to handle
    if request.method == 'POST':
        # We will always get JSON from the server, so convert it to a Python dict
        data = await request.json()

        # Let's see what the server is asking
        print(f'Server sent POST to /my-simple-quest:', data)

        # Ok so we know that the question is "Who invented C++?"
        # The request always contains a "msg" field, and the response always expects an "answer" field
        response = { 'answer': 'bjarne stroustrup' }

        # The server always expects a JSON response
        return web.json_response(response)
    else:
        Log.error('This quest is supposed to handle POST requests')


async def example_websocket_quest(data, player):
    """
    Example quest handler that handles a quest request from the websocket

    :param data: The JSON data received as a Python dictionary
    :param player: The player object, so we have access to different components, for instance sending a reply.
    """

    # Let's see what the server is asking
    print(f'Server sent over websocket:', data)

    # Ok, so we know the server is needy, and expects a response within 2 seconds, better hurry!
    # The request data always contains a "msg" field, and the response always must have a "type" and "data" field,
    # where "data" is whatever the server demands.
    response = { 'msg': 'Calm your processor! Here, have some bits'}

    payload = { 'type': 'player_quest_response', 'data': response }

    await player.ws.send(payload)
