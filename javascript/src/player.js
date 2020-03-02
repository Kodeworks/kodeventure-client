const model = require('./core/model')
const example = require('./quests/example')


/**
 * Implementation of the Player model
 */
class Player extends model.PlayerModel {
  /**
   * Construct a Kodeventure Player
   */
  constructor() {
    super()
  }

  /**
   * Register all your quest handlers here
   */
  loadQuests() {
    // Add a quest handler for a regular HTTP POST request
    this.express.post('/my-simple-quest', example.exampleQuestHandler)

    // Uncomment to use a class based quest handler instead of the above
    // this.exampleQuest = new example.ExampleQuestHandler(this)

    // Add a quest handler for a quest request over websocket
    this.ws.questHandlers.push(example.exampleWsQuestHandler)
  }
}


module.exports = {
  Player: Player
}