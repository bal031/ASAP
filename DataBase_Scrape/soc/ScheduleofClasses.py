
"""
Module that handles all interaction with the Schedule of Classes database hosted by UCSD
"""
# from LogASAP import setup_log, log, LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR, LOG_CRITICAL

from requests import post, get
from traceback import format_exc
from time import time
from Keys import auth_key # used to generate a new access_token 

# constants that will be used repeatedly. DO NOT change. 
access_token = None
end_time = 0
base_url = "https://api.ucsd.edu:8243/get_schedule_of_classes/v1/classes/" # base url for any query 

def getSectionByID(sectionID : int):
    """ 
    Retrieves a section by section id
    
    Returns: #TODO add details
    """
    return makeRequest(base_url+ sectionID) # append sectionID to query

def getSection(termCode : str, subjectCode : str, courseCode : int):
    """
    Retrieves a section by term code, subject code, and course code.

    Returns: #TODO add details 
    """
    return makeRequest(base_url + termCode + ',' + subjectCode + ',' + str(courseCode))

def search(termCode : str, **kwargs):
# subjectCodes=None, courseCodes=None, departments=None, instructor=None, instructorPID=None, title=None, 
            # days, openSection : bool, startTime,
            # endTime, limit, offset, bldgCodes, roomCodes, printFlag):
    """
    Queries for classes based on query parameter criteria. Only returns high level data that can be used to query for individual classes.

    Valid Arguments: (all inputs should be strings)
        termCode: A term code (eg: FA16)
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
    pass # TODO DOES NOT WORK 
    url = base_url + '/search?'
    return makeRequest(url, data=kwargs)



def getMeetings(sectionID : int):
    """
    Retrieves all meeting entries for a section.

    Returns: 
    """
    return makeRequest(base_url + str(sectionID) + '/meetings')

def getAdditionalMeetings(sectionID : int):
    """
    Retrieves all additional meeting entries for a section.
    Returns: 
    """
    return makeRequest(base_url + str(sectionID) + '/additional_meetings')

def getInstructors(sectionID : int):
    """
    Retrieves all instructors for a section.

    Returns: 
    """
    return makeRequest(base_url + str(sectionID) + '/instructors')


def makeRequest(url, data=None):
    """actually makes the get request

    Returns: 

    """
    headers = {
        "authorization" : "Bearer " + getAccessToken() # do this everytime tokens expire
        }
    try:
        response = get(url, data=data, headers=headers).json()
    except:
        response = None
        print('somoething went wrong: \n\n' + format_exc()) # TODO error handling/logging module
    return response

def getAccessToken():
    """
    Description: Handles requesting Access Tokens for the Schedule of Classes API

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
            end_time = time() + response.json()['expires_in'] # current time - seconds until token expiration
            access_token = response.json()['access_token']
        except:
            print('something went wrong: \n' + format_exc()) # TODO need a defined error handling module
            access_token = None
    return access_token    # return access_token 




if __name__ == "__main__":
    print("attempting to make a request...\n\n")
    print(getSection(termCode='SP20', subjectCode='CSE',courseCode='110'))


