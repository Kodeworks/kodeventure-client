/**
 * Example, simple function based quest handler that only needs to reply a response and must be added
 * to the web server manually in the Player class.
 *
 * @param {*} request The express.js request object
 * @param {*} response The express.js response object
 */
function mySimpleQuest(request, response) {
  const reply = JSON.stringify({'answer': 'Functional Hello World!'})

  response.send(reply)
}


/**
 * Example, class based quest handler that will self-register when constructed
 */
class MyQuest {
  /**
   * Construct a MyQuest quest handler
   *
   * @param {Player} player The player object
   */
  constructor(player) {
    this.player = player

    // Set up the player so that this quest answers for requests to /my-quest
    this.player.express.get('/my-quest', this.handleRequest)
  }

  /**
   * Controller that will handle incoming requests for '/my-quest'
   *
   * @param {*} request Express.js request object
   * @param {*} response Express.js response object
   */
  handleRequest(request, response) {
    const reply = JSON.stringify({'answer': 'Classy Hello World!'})

    response.send(reply)
  }

  toString() {
    return `MyQuest (${this.method} ${this.route})`
  }
}

module.exports = {
  mySimpleQuest: mySimpleQuest,
  MyQuest: MyQuest
}