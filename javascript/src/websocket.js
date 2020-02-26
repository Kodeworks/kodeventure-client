const WebSocket = require('ws')

const config = require('./config.js')

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
    this.ws = new WebSocket(`ws://${config.SERVER_HOST}/ws`, { headers: player.headers })

    this.ws.on('open', this.handleOpen.bind(this))
    this.ws.on('message', this.handleMessage.bind(this))
    this.ws.on('error', this.handleError.bind(this))
    this.ws.on('close', this.handleClose.bind(this))
  }

  /**
   * WebSocket handler for open events
   */
  handleOpen() {
    console.log(`Connected to ${config.SERVER_HOST}`)
  }

  /**
   * WebSocket event handler for message events
   * @param {String} msg The message from the server
   */
  handleMessage(msg) {
    const payload = JSON.parse(msg)
    const eventType = payload['type']
    const data = payload['data']

    // TODO: Push type and data into an event parser
    // TOOD: Make constants for each event type
    if (eventType === "game_message") {
      console.log(`[SERVER] ${data['msg']}`)
    } else {
      console.log(`[SERVER] (${eventType}) ${JSON.stringify(data)}`)
    }
  }

  /**
   * WebSocket event handler for error events
   * @param {Number} code The error code if available
   * @param {String} reason The reason if given
   */
  handleError(code, reason) {
    console.error(`[ERROR] ${code} ${reason}`)
  }

  /**
   * WebSocket event handler for close events
   */
  handleClose() {
    console.warn(`[WS] WebSocket connection closed`)
  }
}

module.exports = {
  WebSocketHandler: WebSocketHandler
}