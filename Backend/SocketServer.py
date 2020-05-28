from aiohttp import web
import socketio
import sys

static_path = None
# creates a new Async Socket IO Server
sio = socketio.AsyncServer()
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)

async def index(request):
    """
    handler for index GET requests
    """
    print('Index requested')
    with open(static_path+'index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('message')
async def print_message(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message
    print("Socket ID: " , sid)
    print(message)

@sio.on('connect')
async def new_connection(sid, message):
    print("New connection from: " + sid)

@sio.on('generate schedule')
async def generate_schedule(sid, class_list):
    sio.emit('processing')
    # prcess the schedule
    sio.emit('schedule done', 'replace this with a schedule')

def main():
    """ 
    prep necessary routes then start the server. 
    """
    # router
    global static_path
    static_path = '/var/www/html/'
    app.router.add_get('/', index) # redirect to index on initial visit. 
    app.router.add_static('/', static_path) # automatically add routes for everything else
   
    # app.add_routes([web.static('/', static_path)]) # this works 
    # We kick off our server
    web.run_app(app, host='asap.ucsd.edu', port=80)
    print('done')
    # web.run_app(app) # localhost for debugging

if __name__ == '__main__':
    main()
