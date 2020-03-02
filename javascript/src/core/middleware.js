const config = require('../config.js')
const log = require('../log')

/**
 * Express middleware that will ensure that we are talking to the real game server and not someone trying
 * to play some dirty over level 9000 pro gamer moves on you.
 *
 * @param {*} request The express.js request object
 * @param {*} response The express.js response object
 * @param {*} next Invoke the next handler
 */
const serverAuthMiddleware = (request, response, next) => {
  if (request.headers.authorization !== config.SERVER_TOKEN) {
    log.error(`Received a request from ${request.connection.remoteAddress} with an incorrect server token!`)

    response.status(401)
    response.send('Unauthorized')
  } else {
    // Pass the request along to the next handler
    next()
  }
}

/**
 * Express.js middleware that will attach the correct content type to the response.
 *
 * @param {*} request The express.js request object
 * @param {*} response The express.js response object
 * @param {*} next Invoke the next handler
 */
const jsonContentTypeMiddleware = (request, response, next) => {
    response.setHeader('Content-Type', 'application/json')
    // Pass the request along to the next handler
    next()
}

module.exports = {
    serverAuthMiddleware: serverAuthMiddleware,
    jsonContentTypeMiddleware: jsonContentTypeMiddleware
}