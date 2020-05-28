from aiohttp import web
import socketio
import sys
sys.path.append('../DataBase_Scrape/soc/')
import ScheduleofClasses

static_path = None
# creates a new Async Socket IO Server
sio = socketio.AsyncServer()
# Creates a new Aiohttp Web Application
app = web.Application()
# Binds our Socket.IO server to our Web App
# instance
sio.attach(app)

async def index(request):
    # with open('/var/www/html/test.html') as f:
    #     return web.Response(text=f.read(), content_type='text/html')
    print('Index requested')
    return web.FileResponse(static_path + 'main.html')

# If we wanted to create a new websocket endpoint,
# use this decorator, passing in the name of the
# event we wish to listen out for
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

@sio.on('search')
async def search(sid, message):
    # TODO still working on this 
    response = ScheduleofClasses.search(termCode='SP20', subjectCodes="CSE", openSection="false", offset=50)
    for section in response:
        print(section["courseCode"])



def main():
    """ 
    prep needed routes then start the server. 
    """
    # We bind our aiohttp endpoint to our app
    # router
    # app.add_routes([web.static('/index.html', static_path)])
    global static_path
    static_path = '/home/nate/ASAP/Frontend/'
    route = app.router.add_static('/', static_path, show_index=True)
    print(route.get_info())
    # app.router.add_get('/index.html', index)
    # app.add_routes([web.static('/', static_path)]) # this works 
    # We kick off our server
    web.run_app(app, host='asap.ucsd.edu', port=80)
    # web.run_app(app) # localhost for debugging

if __name__ == '__main__':
    main()
