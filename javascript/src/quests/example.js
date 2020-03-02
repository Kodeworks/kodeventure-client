/**
 * Example, simple function based quest handler that only needs to reply a response and must be added
 * to the web server manually in the Player class.
 *
 * @param {*} request The express.js request object
 * @param {*} response The express.js response object
 */
function exampleQuestHandler(request, response) {
  const reply = JSON.stringify({'answer': 'bjarne stroustrup'})

  response.send(reply)
}


/**
 * Example, class based quest handler that will self-register when constructed
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
    this.player.express.get('/my-simple-quest', this.handleRequest.bind(this))
  }

  /**
   * Controller that will handle incoming requests for '/my-quest'
   *
   * @param {*} request Express.js request object
   * @param {*} response Express.js response object
   */
  handleRequest(request, response) {
    const reply = JSON.stringify({'answer': 'bjarne stroustrup'})

    response.send(reply)
  }
}

module.exports = {
  exampleQuestHandler: exampleQuestHandler,
  ExampleQuestHandler: ExampleQuestHandler
}