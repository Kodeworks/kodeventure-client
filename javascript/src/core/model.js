const bodyParser = require('body-parser')
const chalk = require('chalk')
const express = require('express')
const fs = require('fs')
const https = require('https')
const path = require('path')

const config = require('../config.js')
const log = require('../log')
const middleware = require('./middleware.js')
const websocket = require('./websocket.js')

/**
 * Kodeventure Player class hosting a web server and maintaining an active
 * websocket connection to the Kodeventure game server.
 */
class PlayerModel {
  /**
   * Construct a Player object
   */
  constructor() {
    this.express = express()
    this.headers = {'Authorization': config.PLAYER_TOKEN }

    const cert = this.loadSslCertificate()
    this.httpServer = https.createServer(cert, this.express)
    this.ws = new websocket.WebSocketHandler(this)

    this.config()
  }

  /**
   * Connect to the Kodeventure game server
   */
  connect() {
    // Start the player web server
    this.httpServer.listen(config.PLAYER_PORT, config.PLAYER_HOST)
    // Connect to the game server to register player and receive notifications
    this.ws.connect()
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

    // This will capture all other requests and print to console before sending an empty reply
    this.express.use('*', (req, res, next) => {
      const data = req.body
      const route = req.baseUrl
      const method = req.method

      log.error(`Unhandled ${method} request to ${route}: ${JSON.stringify(data)}`)

      res.json({})
    })
  }

  /**
   * Helper to load SSL certificate from disk
   */
  loadSslCertificate() {
    const privateKeyPath = path.resolve(__dirname, '..', '..', 'player.key')
    const certificatePath = path.resolve(__dirname, '..', '..', 'player.crt')

    const privateKey  = fs.readFileSync(privateKeyPath, 'utf8');
    const certificate = fs.readFileSync(certificatePath, 'utf8');

    return { key: privateKey, cert: certificate }
  }
}


module.exports = {
  PlayerModel: PlayerModel
}
