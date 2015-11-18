WebSocketServer = require('ws').Server
Express = require 'express'
_ = require 'underscore'

app = Express()
app.use Express.static('./client')
server = app.listen (process.env.PORT || 3000), (->)

console.log "Started server on port #{process.env.PORT || 3000}"

machine = undefined
clients = []

wss = new WebSocketServer {server}
wss.on 'connection', (client) ->
  client.on 'message', (message) ->
    if message is "machine"
      console.log "Connected machine"
      if machine? then console.log "WARNING: There was already a machine connected"
      machine = client      
    else if message is "web"
      console.log "Connected web client"
      clients.push client
    else if client in clients and message.match(/[\d\.]+,[\d\.]+,[\d\.]+/)
      console.log "Received: #{message}"
      machine?.send message

  client.on 'close', ->
    if client is machine
      machine = undefined
    else if client in clients
      clients = _(clients).without client