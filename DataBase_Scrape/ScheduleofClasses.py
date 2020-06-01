
"""
Module that handles all interaction with the Schedule of Classes database hosted by UCSD
"""
# from LogASAP import setup_log, log, LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR, LOG_CRITICAL

from requests import post, get
from urllib.parse import urlencode
from traceback import format_exc
from time import time
from Keys import auth_key # used to generate a new access_token
from threading import current_thread, Lock
import json
import copy

# constants that will be used repeatedly. DO NOT change.
access_token = None
end_time = 0
base_url = "https://api.ucsd.edu:8243/get_schedule_of_classes/v1/classes/" # base url for any query
lock = Lock()

def synchronized(func):
    """
    Given a method, return a new method that acquires the the lock before calling the method.
    Then release the lock after the method has returned. This blocks other threads from making a call to the object

    """
    def wrapper(*args, **kwargs):
        """Synchronized wrapper"""
        # with self.lock:
        #     return func(self, *args, **kwargs)
        try:
            if lock.acquire(0):
                # log('{thread} ACQUIRED the lock for {type} {obj}'.format(thread=current_thread().name, type=type(self), \
                # obj=self.name), level=LOG_DEBUG) # Don't need this intensive logging
                return func(*args, **kwargs)
            else:
                print("couldn't acquire lock")
                # log('{thread} couldn\'t acquire the lock for {func_name}'.format(\
                    # thread=current_thread().name, func_name=func.func_name), level=LOG_ERROR)
        except: #Exception as e:
            # log('Synchronization failure in thread: {thread} for {func_name}'.format(\
            #     thread=current_thread().name, func_name=func.func_name), level=LOG_ERROR, email=False,\
            #     err_str=format_exc()) # print a stack trace for the exception
            print("there was an exception \n\n" + format_exc())
        finally:
            if lock.locked: # if lock is acquired, release it
                # log('{thread} RELEASED the lock for {type} {obj}'.format(thread=current_thread().name, type=type(self),\
                # obj=self.name), level=LOG_DEBUG)
                lock.release() # let another thread have a turn
    return wrapper

def getSectionByID(sectionID : str):
    """
    Retrieves a section by section id
    Note: easier to just pass it in as a string because Python 3.x doesn't like leading zeros.

    Returns: JSON of the section information
    """
    return makeRequest(base_url + sectionID) # append sectionID to query

def getSection(termCode : str, subjectCode : str, courseCode : int):
    """
    Retrieves a section by term code, subject code, and course code.

    Returns: JSON of the section information
    """
    return makeRequest(base_url + termCode + ',' + subjectCode + ',' + str(courseCode))

def search(**kwargs):
# subjectCodes=None, courseCodes=None, departments=None, instructor=None, instructorPID=None, title=None,
            # days, openSection : bool, startTime,
            # endTime, limit, offset, bldgCodes, roomCodes, printFlag):
    """
    Queries for classes based on query parameter criteria. Only returns high level data that can be used to query for individual classes.
    Note: the arguments must match exactly or else unexpected responses will be returned without throwing an error.
    Valid Arguments: (all inputs should be strings)
        REQURIED--> termCode: A term code (eg: FA16) <--------------------------------
        subjectCodes: List of subject codes separated by commas no spaces
        courseCodes: List of course codes separated by commas no spaces
        departments: List of department codes separated by commas no spaces
        instructor: Name of the instructor (or part of the name). Last name only works well
        instructorPID: Instructor PID
        title: Title of the course (or part of the title)
        days: List of days of the week separated by commas (eg: "MO,WE,FR") no spaces
        openSection: Set to true if you only want sections with open seats returned
        startTime: Earliest start time (eg: 1430 for 2:30pm)
        endTime: Latest end time (eg: 1430 for 2:30pm)
        limit: Number of entries per page
        offset: Item number to start at (not page number)
        bldgCodes: List of building codes separated by commas.
        roomCodes: List of room codes separated by commas.
        printFlag: Set to false if you want to display suppressed sections

    Returns: Only high level data that can be used to query for individual classes
    """
    # raise NotImplementedError
    url = base_url + 'search?' + urlencode(kwargs)
    return makeRequest(url)["data"]



def getMeetings(sectionID : str):
    """
    Retrieves all meeting entries for a section.

    Returns:
    """
    return makeRequest(base_url + str(sectionID) + '/meetings')

def getAdditionalMeetings(sectionID : str):
    """
    Retrieves all additional meeting entries for a section.
    Returns:
    """
    return makeRequest(base_url + str(sectionID) + '/additional_meetings')

def getInstructors(sectionID : str):
    """
    Retrieves all instructors for a section.

    Returns: a JSON formatted output of the instructors for a section
    """
    return makeRequest(base_url + str(sectionID) + '/instructors')


def makeRequest(url : str):
    """actually makes the get request

    Arguments:
        url: string of the url

    Returns: The requested information in a json format

    """
    headers = {
        "authorization" : "Bearer " + getAccessToken() # do this everytime tokens expire
        }
    try:
        response = get(url, headers=headers).json()
    except:
        response = None
        print('something went wrong: \n\n' + format_exc()) # TODO error handling/logging module
    return response

@synchronized
def getAccessToken():
    """
    Description: Handles requesting Access Tokens for the Schedule of Classes API
    Note: this is a synchronized method and is therefore thread safe.
    Returns: access token as a str or None if the request fails.
    """
    global access_token, end_time # writing to these global variables
    url = "https://api.ucsd.edu:8243/token"
    header = {
        "authorization" : "Basic " + auth_key # found in Keys.py should be on the .gitignore
    }
    payload = {
        "grant_type" : "client_credentials"
    }
    if time() >= end_time or access_token is None: # do we need a new access token?
        try:
            response = post(url=url, data=payload, headers=header)
            end_time = time() + response.json()['expires_in'] # current time + seconds until token expiration
            access_token = response.json()['access_token']
        except:
            print('something went wrong: \n' + format_exc()) # TODO need a defined error handling module
            access_token = None
    return access_token    # return access_token

def get_section_pairings(user_courses, termCode='FA20', personalEvents=None):
    """
    Prepares a list of sections for algorithm to use in making its selection. Similar to how its viewd on webreg
    NOTE: I am pairing lectures and discussions with the same prefix together. i.e. LE A00 and DI A01, LE A00 and DI A02, ... etc.
    Paramters:
        user_courses : list of list of dictionaries describing courses selected by the user from the UI. The JSON format is managed by Hung
            Example:
                [
                    {
                        "must_have" : "true",
                        "name" : "CSE 100"
                    },
                    ...
                ]
    """
    must_haves = []
    could_haves = []

    must_haves += (get_personalEvents(personalEvents)) # personal events are required events

    for section in user_courses:
        if section['must_have'] == 'true': # append to must_haves
            append_list = must_haves
        else: # append to could haves
            append_list = could_haves
        subjectCode, courseCode = [section['name'].split(' ')[i] for i in (0, 1)]  # get subjectCode and courseCode
        response = getSection(termCode=termCode, subjectCode=subjectCode, courseCode=courseCode) # query schedule of classes

        classes = []
        curr_le = dict()
        for section in response['sections']:
            if section['instructionType'] == 'LE': # new lecture A00, B00, ..., etc.
                curr_le['meetings'] = get_recurringMeetings(section) # recurring weekly
                curr_le['finals'], curr_le['midterms'] = get_additionalMeetings(section) # returns [finals, midterms]
                curr_le['LE id'] = section['sectionId'] # saves time later on getting the lecture times
            else: # it's a DI or LA, create new LE to DI/LA pairing
                if section['enrolledQuantity'] != section['capacityQuantity']: # only want classes with open seats
                    new_pair = copy.deepcopy(curr_le) # get baseline characteristics for the new pairing
                    new_pair['id'] = section['sectionId'] # LE to DI/LA pairings are identified by there DI/LA sectionId
                    new_pair['meetings'] += (get_recurringMeetings(section))
                    classes.append(new_pair)
                # else skip this section, capacity is determined by DI/LA and not lecture
        append_list.append(classes)
    return [must_haves, could_haves]

def get_personalEvents(personalEvents):
    """
    Personal events are treated like an other must have class.
    """
    must_haves = []
    if personalEvents is not None:
        for event in personalEvents:
            meetings = list()
            startTime = int(event['startTime'])
            endTime = int(event['endTime'])
            # eventName = event['courseName']  # Can a user name an event?
            for day in event['instructionDay']:
                meetings.append([day, startTime, endTime])
            must_haves.append([{'id' : 'personal event', 'meetings' : meetings, 'finals': [], 'midterms' : [], 'LE id': 'personal event'}])
    return must_haves


def get_recurringMeetings(section : dict):
    """
    helper function for get section pairings. Gets all recurring meetings for a section and formats it how
    James has requested.
    Parameters:
        section: single dict corresponding to a section, could be LE, LA, or DI.
    Returns: array of meetings for the provided section
    """
    meetings = list()
    for meeting in section['recurringMeetings']:
        dayCode = meeting['dayCode']
        startTime = int(meeting['startTime'])
        endTime = int(meeting['endTime'])
        # buildingCode = meeting['buildingCode'] # in case anyone wants this information later
        # roomCode = meetings['roomCode']
        meetings.append([dayCode, startTime, endTime])

    return meetings

def get_additionalMeetings(section : dict):
    """
    Helper function for get_section_pairings. Gets all of the additional meetings for a section and formats it how James
    has requested. Additionally meetings refer to midterms and finals and are only found inside of a lecture section.
    Paraemeters:
        section: single dict coresponding to a section (LE, LA, DI).
    Returns: [final, midterms] where a final is an array of meeningful info and midterms is an array of meetings
    """
    midterms = []
    final = None
    for meeting in section['additionalMeetings']:
        dayCode = meeting['dayCode']
        startTime = int(meeting['startTime'])
        endTime = int(meeting['endTime'])
        meetingDate = meeting['meetingDate']
        if meeting['meetingType'] == 'MI': # midterm
            midterms.append([dayCode, startTime, endTime, meetingDate]) # might want date for later conflict checking
        else: #NOTE assuming a class can only have one final.
            final = [dayCode, startTime, endTime] # don't really need a meeting date because of exclusivity of finals week
    return [final, midterms]



# [{"id":6,"meetings":[["TU",140000,152000],["TH",140000,152000],["W",90000,115000]],"finals":["M",150000,180000]},{"id":7,"meetings":[["TU",140000,152000],["TH",140000,152000],["W",90000,115000]],"finals":["M",150000,180000]},{"id":8,"meetings":[["TU",140000,152000],["TH",140000,152000],["W",90000,115000]],"finals":["M",150000,180000]},{"id":9,"meetings":[["TU",140000,152000],["TH",140000,152000],["W",120000,145000]],"finals":["M",150000,180000]},{"id":10,"meetings":[["TU",140000,152000],["TH",140000,152000],["W",120000,145000]],"finals":["M",150000,180000]}]


"""
if __name__ == "__main__": # for testing purposes
#     print("attempting to make a request...\n\n")
#     # print(json.dumps((getSection(termCode='SP20', subjectCode='CSE',courseCode='110'))))
#     # print(search(termCode='SP20', subjectCodes="CSE", courseCode="110", limit=1))
#     # testURL = "https://api.ucsd.edu:8243/get_schedule_of_classes/v1/classes/search?termCode=SP20&subjectCodes=CSE&courseCodes=110&openSection=false"
#     # response = makeRequest(testURL)

#     response = getSectionByID(sectionID="021116")

#     course = response['subjectCode'] +  ' ' + response['courseCode']
#     instructors = list()
#     for section in response['sections']:
#         for instructor in section['instructors']:
#             instructors.append(instructor['instructorName'])

#     print('Course: ' + course + '\n\t' + str(instructors))

#    user_courses = [{'must_have' : 'true', 'name' : 'ECE 102'},{'must_have':'true','name':'CHEM 6A'}]
    #personal_events = [{'courseName' : 'my_time', 'startTime': 900, 'endTime': 1000, 'instructionDay' : ['TU', 'TH']}]
#    must_haves, could_haves = get_section_pairings(user_courses)
#    print(must_haves[0])
#    print(must_haves[1])
#    print(could_haves)
#    result = generateSchedule(must_haves, could_haves,[])
#    print(result)
"""