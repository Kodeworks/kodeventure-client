const bodyParser = require('body-parser')
const express = require('express')

const config = require('./config.js')
const example = require('./quests/example.js')
const middleware = require('./middleware.js')
const websocket = require('./websocket.js')

/**
 * Kodeventure Player class hosting a web server and maintaining an active
 * websocket connection to the Kodeventure game server.
 */
class Player {
  /**
   * Construct a Player object
   */
  constructor() {
    this.express = express()
    this.headers = {'Authorization': config.PLAYER_TOKEN }
  }

  /**
   * Configure the web server to use your quest handlers
   */
  loadQuests() {
    // Simple version, where we just attach a quest handler that will respond to HTTP GET
    this.express.get('my-simple-quest', example.mySimpleQuest)

    // Class based version, where the quest handler has the full power of the Player object to use
    // when solving the quest.
    this.myQuest = new example.MyQuest(this)
  }

  /**
   * Connect to the Kodeventure game server
   */
  connect() {
    // Start the player web server
    this.express.listen(config.PLAYER_PORT, config.PLAYER_HOST)

    // Connect to the game server to register player and receive notifications
    this.ws = new websocket.WebSocketHandler(this)
  }

  /**
   * Configure express.js
   */
  config() {
    this.express.use(middleware.serverAuthMiddleware)
    // TODO: Check if we actually need this content type middleware
    this.express.use(middleware.jsonContentTypeMiddleware)
    this.express.use(bodyParser.json())
    this.express.use(bodyParser.urlencoded({ extended: false }))

    this.loadQuests()
  }
}

const player = new Player()

player.connect()