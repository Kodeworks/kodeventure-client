const log = require('../log')


/**
 * Example, simple function based quest handler that only needs to reply a response and must be added
 * to the web server manually in the Player class.
 *
 * @param {*} request The express.js request object
 * @param {*} response The express.js response object
 */
function exampleQuestHandler(request, response) {
  if (request.method === 'POST') {
    // We will always get JSON from the server
    const data = request.body

    // Let's see what the server is asking
    log.info(`Server sent POST to /my-simple-quest: ${JSON.stringify(data)}`)

    // Ok so we know that the question is "Who invented C++?"
    // The request always contains a "msg" field, and the response always contains an "answer" field
    const reply = {'answer': 'bjarne stroustrup'}

    // The web server always expects a JSON response
    response.send(JSON.stringify(reply))
  } else {
    log.error('This quest is supposed to handle POST requests')
  }
}


/**
 * Example, class based quest handler that will self-register when constructed.
 * This example accepts the Player object as a constructor argument, so we can access
 * all relevant properties of the Player.
 */
class ExampleQuestHandler {
  /**
   * Construct a MyQuest quest handler
   *
   * @param {Player} player The player object
   */
  constructor(player) {
    this.player = player

    // Set up the player so that this quest answers for requests to /my-quest
    this.player.express.post('/my-simple-quest', this.handleRequest.bind(this))
  }

  /**
   * Controller that will handle incoming requests for '/my-quest'
   *
   * @param {*} request Express.js request object
   * @param {*} response Express.js response object
   */
  handleRequest(request, response) {
    if (request.method === 'POST') {
      // We will always get JSON from the server
      const data = request.body
  
      // Let's see what the server is asking
      log.info(`Server sent POST to /my-simple-quest: ${JSON.stringify(data)}`)

      // Ok so we know that the question is "Who invented C++?"
      // The request always contains a "msg" field, and the response always contains an "answer" field
      const reply = {'answer': 'bjarne stroustrup'}

      // The web server always expects a JSON response
      response.send(JSON.stringify(reply))
    } else {
      log.error('This quest is supposed to handle POST requests')
    }
  }
}

module.exports = {
  exampleQuestHandler: exampleQuestHandler,
  ExampleQuestHandler: ExampleQuestHandler
}