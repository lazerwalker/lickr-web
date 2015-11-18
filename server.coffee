Express = require 'express'

app = Express()
app.use Express.static('./client')
server = app.listen (process.env.PORT || 3000), (->)

console.log "Started server on port #{process.env.PORT || 3000}"