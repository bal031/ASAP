from aiohttp import web
import socketio
import sys
sys.path.append('/home/nate/ASAP/Log')
from LogASAP import log, setup_log, LogASAP
import json
from time import sleep, time



static_path = None
# creates a new Async Socket IO Server
sio = socketio.AsyncServer()
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)


class User(): # implicit inheritance from object Python 3.x
    """
    defines a user object to store user information while connected to a socket. 
    """
    def __init__(self, sid, address, course_list=None, preferences=None, personal_events=None):
        """
        Parameters:
            sid -- socket id
            course_list -- dict of User course
            preferences -- dict of User course preferences 
        """
        self.sid = sid # socket id 
        self.address = address
        self.course_list = course_list # User selected courses
        self.preferences = preferences # User chosen preferences
        self.personal_events = personal_events # User's personal events
        self.schedule = None # set by generate schedule

async def index(request):
    """
    handler for index GET requests
    """
    log('Index requested by ', request.remote)
    with open(static_path+'index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect')
async def new_connection(sid, environ):
    """
    Sets up a User object for each session. A single computer can have multiple sessions and sockets open.
    """
    new_session = 'New session'
    address = environ['aiohttp.request'].remote
    await sio.save_session(sid, {'user': User(sid=sid, address=address), 'address' : address}) # save information about the user
    
    log(new_session + " for host: " + address)

@sio.on('disconnect')
async def remove_connection(sid):
    session = await sio.get_session(sid=sid)
    log('Connection ended: ' + session['address'] ) 

@sio.on('message')
async def print_message(sid, message):
    """
    Generic message handler mostly for testing
    """
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message
    log("Socket ID: " , sid, ' message: ', str(message))


@sio.on('generate schedule')
async def receive_schedule(sid, data):
    """
    event handler for when a User attempts to generate a schedule
    """
    session = await sio.get_session(sid)
    log('Generate schedule reqeuest from: ', session['address'])
    course_list = json.loads(data)
    await generate_schedule(session['user'])
    # sio.emit('processing')
    # # prcess the schedule
    # sio.emit('schedule done', 'replace this with a schedule')
 
async def send_schedule(user: User):
    await sio.emit('schedule ready', 'replace with schedule', room=user.sid)

async def generate_schedule(user: User):
    log("generating schedule for ", user.address)
    sleep(5) # simulate processing 
    await send_schedule(user)



def main():
    """ 
    prep necessary routes then start the server. 
    """
    setup_log() # default log level is debug
    # router
    global static_path
    static_path = '/var/www/html/' # base bath to all of the static files. 
    app.router.add_get('/', index) # redirect to index on initial visit. 
    app.router.add_static('/', static_path) # automatically add routes for everything else
    # app.add_routes([web.static('/', static_path)]) # this works 
    # We kick off our server
    log('Starting ASAP socket server')
    web.run_app(app, host='asap.ucsd.edu', port=80) # this is blocking
    log('Stoppping ASAP socket server')
    # web.run_app(app) # localhost for debugging. Doesn't require root to run

if __name__ == '__main__':
    main()

