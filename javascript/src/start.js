const cert = require('./core/cert')
const player = require('./player')

const log = require('./log')

// Disable all TLS verification since we're dealing with self-signed certs
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0"

// Adjust accordingly
log.logLevel = log.DEBUG


cert.initCertificate().then(() => {
    const p = new player.Player()
    p.connect()
})
