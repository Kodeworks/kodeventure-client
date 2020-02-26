// The host and port of the Kodeventure game server
const SERVER_HOST = '127.0.0.1:3001'
// The host to bind your player instance to
const PLAYER_HOST = '0.0.0.0'
// The port to bind your player instance to
const PLAYER_PORT = 4242

// The authorization token identifying your player in the game (received from the game masters)
const PLAYER_TOKEN = 'abc'
// The authorization token identifying the server in the game (received from the game masters)
const SERVER_TOKEN = 'def'

module.exports = {
    SERVER_HOST: SERVER_HOST,
    SERVER_TOKEN: SERVER_TOKEN,
    PLAYER_HOST: PLAYER_HOST,
    PLAYER_PORT: PLAYER_PORT,
    PLAYER_TOKEN: PLAYER_TOKEN,
}