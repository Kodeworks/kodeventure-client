const chalk = require('chalk')


const DEBUG = 0
const INFO = 10
const WARNING = 20
const ERROR = 30


/**
 * Simple console output utility
 */
const Log = {
    logLevel: DEBUG,

    /**
     * Print in color
     * @param {*} msg The message 
     */
    debug(msg) {
        if (Log.logLevel === DEBUG) {
            console.log(chalk.cyan(msg))
        }
    },

    /**
     * Print a server message in a light blue color
     * @param {*} eventType The event type from the server payload
     * @param {*} msg The message
     */
    server(eventType, msg) {
        console.log(chalk.blueBright(`[SERVER] (${eventType}) ${msg}`))
    },

    /**
     * Print a regular unformatted message
     * @param {*} msg 
     */
    info(msg) {
        if (Log.logLevel <= INFO) {
            console.log(msg)
        }
    },

    /**
     * Print a warning message in yellow color
     * @param {*} msg The message
     */
    warning(msg) {
        if (Log.logLevel <= WARNING) {
            console.log(chalk.yellow(msg))
        }
    },

    /**
     * Print an error message in red color
     * @param {*} msg The message
     */
    error(msg) {
        if (Log.logLevel <= ERROR) {
            console.log(chalk.red(msg))
        }
    }
}


module.exports = {
    debug: Log.debug,
    info: Log.info,
    warning: Log.warning,
    error: Log.error,
    server: Log.server,
    DEBUG: DEBUG,
    INFO: INFO,
    WARNING: WARNING,
    ERROR: ERROR
}
