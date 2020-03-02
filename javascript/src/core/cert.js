const fetch = require('node-fetch')
const fs = require('fs')
const path = require('path')

const config = require('../config')


const CERT_ENDPOINT = `https://${config.SERVER_HOST}/cert`


/**
 * Fetch the filename from the parent directory of this file
 * @param {*} filename The filename to fetch
 */
const rootDir = (filename) => {
    return path.resolve(__dirname, '..', '..', filename)
}


/**
 * Create a certificate by requesting a new one from the server and writing it to the root directory.
 */
const createCertificate = async () => {
    const response = await fetch(CERT_ENDPOINT, {
        method: 'POST'
    })

    if (response.status === 200) {
        const data = await response.json()

        const privateKey = data['private']
        const publicKey = data['public']
        const certificate = data['cert']

        fs.writeFileSync(rootDir('player.key'), privateKey)
        fs.writeFileSync(rootDir('player.pub'), publicKey)
        fs.writeFileSync(rootDir('player.crt'), certificate)
    } else {
        throw new Error('Got non-200 response from server')
    }
}


/**
 * Initialize the player certificate by checking if it exists.
 * If it does not, a new certificate will be fetched from the server
 * before starting.
 */
const initCertificate = async () => {
    key = rootDir('player.key')
    cert = rootDir('player.crt')

    if (!(fs.existsSync(key) && fs.existsSync(cert))) {
        await createCertificate()
    }
}


module.exports = {
    initCertificate: initCertificate
}
