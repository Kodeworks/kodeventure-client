const chalk = require('chalk')
const WebSocket = require('ws')

const config = require('../config.js')
const log = require('../log')

const WS_URI = `wss://${config.SERVER_HOST}/ws`

/**
 * A WebSocket handler that parses messages from the server and spits them out accordingly
 */
class WebSocketHandler {
  /**
   * Construct a websocket handler
   * @param {Player} player The player object
   */
  constructor(player) {
    this.player = player
    this.ws = new WebSocket(WS_URI, { headers: player.headers, rejectUnauthorized: false })

    this.ws.on('open', this.handleOpen.bind(this))
    this.ws.on('message', this.handleMessage.bind(this))
    this.ws.on('error', this.handleError.bind(this))
    this.ws.on('close', this.handleClose.bind(this))
  }

  /**
   * WebSocket handler for open events
   */
  handleOpen() {
    log.info(`[WS] Connected to ${WS_URI}`)
  }

  /**
   * WebSocket event handler for message events
   * @param {String} msg The message from the server
   */
  handleMessage(msg) {
    const payload = JSON.parse(msg)
    const eventType = payload['type']
    const data = payload['data']

    switch (eventType) {
      case "game_started":
      case "game_message":
      case "game_paused":
      case "game_unpaused":
      case "game_ended":
        log.server(eventType, data['msg'])
        break
      case "player_error":
        log.error(`[SERVER] (${eventType}) ${data['error']}`)
        break
      default:
        log.server(eventType, JSON.stringify(data))
    }
  }

  /**
   * WebSocket event handler for error events
   * @param {Number} code The error code if available
   * @param {String} reason The reason if given
   */
  handleError(code, reason) {
    log.error(`[WS] ${code} ${reason}`)
  }

  /**
   * WebSocket event handler for close events
   */
  handleClose() {
    log.info(`[WS] WebSocket connection closed`)
  }
}

module.exports = {
  WebSocketHandler: WebSocketHandler
}
