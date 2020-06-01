from aiohttp import web
import socketio
import sys
sys.path.append('/home/nate/ASAP/Log')
sys.path.append('/home/nate/ASAP/DataBase_Scrape/')
from LogASAP import log, setup_log, LogASAP, LOG_ERROR, LOG_INFO
import json
from time import sleep, time
import schedule 
import ScheduleofClasses

# Global assignments, plus they need to run first. 
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
        self.schedule = {} # set by generate schedule

async def index(request):
    """
    handler for index GET requests
    """
    log('Index requested by {client_address}'.format(client_address=request.remote) )
    with open(static_path+'index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.on('connect')
async def new_connection(sid, environ):
    """
    Sets up a User object for each session. A single computer can have multiple sessions and sockets open.
    """
    address = environ['aiohttp.request'].remote
    await sio.save_session(sid, {'user': User(sid=sid, address=address), 'address' : address}) # save information about the user
    
    log("New session for host: " + address)

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
    log("Socket ID: "  + sid + ' message: ' + str(message))


@sio.on('generate')
async def receive_schedule(sid, data):
    """
    event handler for when a User attempts to generate a schedule
    """
    session = await sio.get_session(sid)
    log('Generate schedule reqeuest from: ' + session['address'])
    await sio.emit('comfirmation', 'Data Received. Optimizing Schedule...', room=sid) # NOTE typo on the UI for comfirmation, should be confirmation
    
    input_dict = json.loads(data) 
    user = session['user']
    user_courses = input_dict['course']
    currentTerm = input_dict['currentTerm']
    personalEvents = input_dict['personalEvent']

    must_haves, could_haves = ScheduleofClasses.get_section_pairings(user_courses=user_courses, termCode=currentTerm, \
        personalEvents=personalEvents)

    print('must_haves:\n', must_haves)
    user.schedule = schedule.generateSchedule(must_haves=must_haves, want_to_haves=could_haves, \
        preferences=input_dict['preference'])
    print('Schedule: \n', user.schedule) # save raw output of schedule

    new_display, new_schedule = convert_schedule(user)

    # test_schedule = json.dumps(test)
    print("Converted Schedule:\n", new_schedule)
    test_schedule = json.dumps({'display': new_display, 'schedule': new_schedule})

    await sio.emit('schedule_ready', test_schedule, room=user.sid)
    log('Sent schedule to: ' + str(user.address))

def convert_schedule(user: User):
    """
    converts a generated schedule into the correct format needed to display it on the UI calendar and table
    """
    dayCodeDict = { 'SU' : 0, 'MO' : 1, 'TU' : 2, 'WE' : 3, 'TH' : 4, 'FR' : 5, 'SA' : 6} # days of the week constants
    new_display = [] 
    new_schedule = []
    for course in user.schedule:
        ids = [course['LE id'], course['id']]
        # get meetings for both
        if ids[1] != 'personal event':
            for ID in ids: 
                response = ScheduleofClasses.getSectionByID(sectionID=ID)
                section = response['sections'][0] # only returns a single section
                title = response['subjectCode'] + ' ' + response['courseCode'] + ' ' + section['instructionType']
                daysOfWeek = []
                for meeting in section['recurringMeetings']:
                    dayCode = dayCodeDict[meeting['dayCode']] # convert dayCode to a number e.g. SU to 0
                    daysOfWeek.append(dayCode) # separate for debugging
                    startTime = convertTime(meeting['startTime'])
                    endTime = convertTime(meeting['endTime'])
                new_schedule.append({'title': title, 'startTime': startTime, 'endTime': endTime, 'daysOfWeek': daysOfWeek})
        else:
            pass
    
    return [new_display, new_schedule]

def convertTime(time: str):
    """
    Converts from Schedule of Classes format e.g. 1200 to 12:00:00
    """
    if len(time) < 4:
        time = time[:1] + ':' + time[1:] + ':00'
    else:
        time = time[:2] + ':' + time[2:] + ':00'
    return time

test = """
    'display': [{name: 'CSE 100',
            'professor': 'Paul Cao',
            'days': 'MWF',
            'start': '9:00 AM',
            'end': '9:50 AM'}],
    'schedule': [{ 'title': 'CSE 110',
                'startTime': '9:00:00',
                'endTime': '9:50:00',
                'daysOfWeek': [1,3,5]}
                ]
}
"""
test = {'display': [{'name' : 'CSE 100', 'professor': 'Paul Cao', 'days' : 'MWF', 'start':'9:00 AM', 'end': '9:50 AM'}],\
        'schedule' : [{'title': 'CSE 110', 'startTime': '9:00:00', 'endTime': '9:50:00', 'daysOfWeek': [1,3, 5]}] }


def main():
    """ 
    prep necessary routes then start the server. 
    """
    setup_log() # default log level is debug
    # router
    global static_path
    static_path = '/var/www/html/src/' # base bath to all of the static files. 
    # static_path = '/home/nate/ASAP/Frontend/'
    app.router.add_get('/', index) # redirect to index on initial visit. 
    app.router.add_static('/', static_path) # automatically add routes for everything else
    # app.add_routes([web.static('/', static_path)]) # this works 
    # We kick off our server
    log('Starting ASAP socket server')
    try:
        web.run_app(app, host='asap.ucsd.edu', port=80) # this is blocking
        # web.run_app(app) # localhost for debugging. Doesn't require root to run
        log('Stoppping ASAP socket server')
    except Exception as e:
        log('The server messed up', level=LOG_ERROR, email=False, err_str=str(e))

if __name__ == '__main__':
    main()



