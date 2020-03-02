const cert = require('./core/cert')
const player = require('./player')

// Disable all TLS verification since we're dealing with self-signed certs
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0"

cert.initCertificate().then(() => {
    const p = new player.Player()
    p.connect()
}).catch(e => {
    console.error(e)
})
