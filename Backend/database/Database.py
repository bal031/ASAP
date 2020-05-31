# This module is used for communicating with the asap_database. Use the 
# get_database() method to open a connection and the close_database() method
# to close it once finished.
#
# This file uses the mysql-connector-python library.
# To install for python3 use: `pip3 install mysql-connector-python`
#
# NOTE: The following methods should not be vulnerable to SQL injection, but 
#   they have not been tested. Proceed with caution.  

import mysql.connector
USER = 'python'
PASSWORD = 'password'
DATABASE = 'asap_database'
HOST = 'localhost'

CAPE_KEYS = ("expected_grade", "received_grade", "hours_per_week", 
             "recommend_course", "recommend_professor", "response_rate", 
             "term_code", "name", "subject_code", "course_code")

def get_database():
    '''
    Returns a connection to the asap_database. Use close_database() once finished.
    Returns None if error is encountered.
    '''
    try:
        return mysql.connector.connect(
            host=HOST,
            user=USER,
            passwd=PASSWORD,
            database=DATABASE
        )
    except mysql.connector.Error as err:
        print('ERROR: Failed to connect to the asap_database:')
        print(err)
        return None

def close_database(database):
    database.close()

def get_user_email(user_id, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Returns the email of the user.

    Parameters:
    user_id (String): the unique id of the user, use get_user_id() for this value
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: the email of the user
    '''
    user = (user_id, )
    cursor = database.cursor()
    sql = "SELECT email FROM user WHERE userID = %s"
    cursor.execute(sql, user)
    id_list = cursor.fetchall()
    cursor.close()

    return id_list[0][0]

def get_user_create_date(user_id, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Returns the date the user's account was created on.

    Parameters:
    user_id (String): the unique id of the user, use get_user_id() for this value
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: the date the user's account was created on
    '''
    user = (user_id, )
    cursor = database.cursor()
    sql = "SELECT create_date FROM user WHERE userID = %s"
    cursor.execute(sql, user)
    id_list = cursor.fetchall()
    cursor.close()

    return id_list[0][0]
    
def get_user_id(google_id, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Returns the userID that corresponds to the given google_id. Returns
    None if the google_id is not in the database

    Parameters:
    google_id (String): the unique google_id of the user
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: the userID if found, None otherwise
    '''
    user = (google_id, )
    cursor = database.cursor()
    sql = "SELECT userID FROM user WHERE google_id = %s"
    cursor.execute(sql, user)
    id_list = cursor.fetchall()
    cursor.close()

    if len(id_list) != 1:
        return None

    return id_list[0][0]

def insert_user(google_id, email, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Inserts the indicated user into the database. Will fail if the 
    google_id is already regestered.

    Parameters:
    google_id (String): the unique google_id of the user
    email (String): the email of the user
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: true if the user is successfully added, false otherwise
    '''
    if get_user_id(google_id, database) is not None:
        return False

    cursor = database.cursor()
    user = (google_id, email)
    sql = "INSERT INTO user (google_id, email) VALUES (%s, %s)"
    cursor.execute(sql, user)
    database.commit()
    cursor.close()
    return True

def get_user_schedule(user_id, name, term_code, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Returns the id of the specified schedule, and inserts the schedule
    into the database if it is not present

    Parameters:
    user_id (String): the unique id of the user, use get_user_id() for this value
    name (String): the name of the schedule
    term_code (String): The term this schedule is associated with e.g. ("SP20")
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: void
    '''
    cursor = database.cursor()
    user = (user_id, name, term_code.upper())

    sql = "SELECT scheduleID FROM schedule WHERE userID = %s AND name = %s AND term_code = %s"
    cursor.execute(sql, user)
    id_list = cursor.fetchall()

    if len(id_list) != 0:
        cursor.close()
        return id_list[0][0]

    sql = "INSERT INTO schedule (userID, name, term_code) VALUES (%s, %s, %s)"
    cursor.execute(sql, user)
    database.commit()

    sql = "SELECT scheduleID FROM schedule WHERE userID = %s AND name = %s AND term_code = %s"
    cursor.execute(sql, user)
    id_list = cursor.fetchall()

    cursor.close()
    return id_list[0][0]

def get_capes_by_course(subject_code, course_code, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Returns all capes for the indicated course.

    Parameters:
    subject_code (String): the subject of the course, (e.g. 'CSE')
        will be converted to UPPERCASE (e.g. 'cSe' becomes 'CSE')
    course_code (String): the code for the course, (e.g. '15L')
        will be converted to UPPERCASE (e.g. '15l' becomes '15L')
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: An array of all capes for the indicated course. Each CAPE 
             is represented as a dictionary. Use the CAPE_KEYS tuple
             to access the values you need. expected_grade and 
             received_grade have a value of -1 if there was no value for
             them.
    '''
    cursor = database.cursor()
    course = (get_course_id(subject_code, course_code, database),)
    sql = "SELECT cape_review.expected_grade, cape_review.received_grade, " \
        + "cape_review.hours_per_week, cape_review.recommend_course, " \
        + "cape_review.recommend_professor, cape_review.response_rate, " \
        + "cape_review.term_code, professor.name, course.subject_code, " \
        + "course.course_code FROM cape_review LEFT JOIN professor " \
        + "ON professor.professorID = cape_review.professorID LEFT JOIN course " \
        + "ON course.courseID=cape_review.courseID WHERE " \
        + "cape_review.courseID= %s"

    cursor.execute(sql, course)
    cape_list_raw = cursor.fetchall()

    cursor.close()

    cape_list = []
    for i in range(len(cape_list_raw)):
        cape_list.append({})
        for j in range(len(CAPE_KEYS)):
            cape_list[i][CAPE_KEYS[j]]=cape_list_raw[i][j]

    return cape_list

def get_course_id(subject_code, course_code, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Returns the unique id of the course. Will add the course to the database
    if the course does not exist.

    Parameters:
    subject_code (String): the subject of the course, (e.g. 'CSE')
        will be converted to UPPERCASE (e.g. 'cSe' becomes 'CSE')
    course_code (String): the code for the course, (e.g. '15L')
        will be converted to UPPERCASE (e.g. '15l' becomes '15L')
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: the unique id of the class
    '''
    course = (subject_code.upper(), course_code.upper())
    cursor = database.cursor()
    sql = "SELECT courseID FROM course WHERE subject_code = %s AND course_code = %s"
    cursor.execute(sql, course)
    id_list = cursor.fetchall()

    if len(id_list) != 0:
        cursor.close()
        return id_list[0][0]

    sql = "INSERT INTO course (subject_code, course_code) VALUES (%s, %s)"
    cursor.execute(sql, course)
    database.commit()

    sql = "SELECT courseID FROM course WHERE subject_code = %s AND course_code = %s"
    cursor.execute(sql, course)
    id_list = cursor.fetchall()

    cursor.close()
    return id_list[0][0]

def get_room_id(building_code, room_code, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Returns the unique id of the room. Will add the room to the database
    if the room does not exist.

    Parameters:
    building_code (String): the building where the room is located, (e.g. 'WLH')
        will be converted to UPPERCASE (e.g. 'Wlh' becomes 'WLH')
    room_code (String): the room, (e.g. '201A')
        will be converted to UPPERCASE (e.g. '201a' becomes '201A')
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: the unique id of the class
    '''
    room = (building_code.upper(), room_code.upper())
    cursor = database.cursor()
    sql = "SELECT roomID FROM room WHERE building_code = %s AND room_code = %s"
    cursor.execute(sql, room)
    id_list = cursor.fetchall()

    if len(id_list) != 0:
        cursor.close()
        return id_list[0][0]

    sql = "INSERT INTO room (building_code, room_code) VALUES (%s, %s)"
    cursor.execute(sql, room)
    database.commit()

    sql = "SELECT roomID FROM room WHERE building_code = %s AND room_code = %s"
    cursor.execute(sql, room)
    id_list = cursor.fetchall()

    cursor.close()
    return id_list[0][0]

def get_professor_id(name, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Returns the unique id of the professor. Will add the course to the database
    if the course does not exist.

    Parameters:
    name (String): The name of the professor, case and comma sensitive 
        (e.g. "Gillespie, Gary")
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: the unique id of the professor
    '''
    professor = (name, )

    cursor = database.cursor()
    sql = "SELECT professorID FROM professor WHERE name = %s"
    cursor.execute(sql, professor)
    id_list = cursor.fetchall()

    if len(id_list) != 0:
        cursor.close()
        return id_list[0][0]

    sql = "INSERT INTO professor (name) VALUES (%s)"
    cursor.execute(sql, professor)
    database.commit()

    sql = "SELECT professorID FROM professor WHERE name = %s"
    cursor.execute(sql, professor)
    id_list = cursor.fetchall()

    cursor.close()
    return id_list[0][0]

def insert_cape(subject_code, course_code, name, 
        expected_grade, received_grade, hours_per_week, recommend_course, 
        recommend_professor, response_rate, term_code, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Inserts the cape into the database. Will duplicate capes if 
    same inputs given multiple times.

    Parameters:
    subject_code (String): the subject of the course, (e.g. 'CSE')
        will be converted to UPPERCASE (e.g. 'cSe' becomes 'CSE')
    course_code (String): the code for the course, (e.g. '15L')
        will be converted to UPPERCASE (e.g. '15l' becomes '15L')
    name (String): The name of the professor, case and comma sensitive 
        (e.g. "Gillespie, Gary")
    expected_grade (Float): From 0.0 to 4.0 or -1 if not present
    hours_per_week (Float): Minimum 0.0
    received_grade (Float): From 0.0 to 4.0 or -1 if not present
    recommend_course (Float): From 0.0 to 100.0
    recommend_professor (Float): From 0.0 to 100.0
    response_rate (Float): From 0.0 to 100.0. Equal to
        (number of  respondants)/(number of students in class)
    term_code (String): e.g. ("SP20")
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: void
    '''
    courseID = get_course_id(subject_code, course_code, database)
    professorID = get_professor_id(name, database)

    cape = (courseID, professorID, expected_grade, hours_per_week, received_grade, 
            recommend_course, recommend_professor, response_rate, term_code.upper())

    
    cursor = database.cursor()
    sql = "INSERT INTO cape_review (courseID, professorID, expected_grade, " \
        + "hours_per_week, received_grade, recommend_course, recommend_professor, " \
        + "response_rate, term_code) VALUES "\
        + "(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, cape)
    database.commit()
    cursor.close()

def get_section_id(subject_code, course_code, name, 
        instruction_type, section_code, term_code, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Gets the id of the specified section, and inserts it into the database
    if it doesn't exist

    Parameters:
    subject_code (String): the subject of the course, (e.g. 'CSE')
        will be converted to UPPERCASE (e.g. 'cSe' becomes 'CSE')
    course_code (String): the code for the course, (e.g. '15L')
        will be converted to UPPERCASE (e.g. '15l' becomes '15L')
    name (String): The name of the professor, case and comma sensitive 
        (e.g. "Gillespie, Gary")
    instruction_type (String): what type of instruction is this (e.g. 'LE', 'DI')
    section_code (String): code for the section (e.g. 'A01')
    term_code (String): e.g. ("SP20")
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: the id of the specified section
    '''
    courseID = get_course_id(subject_code, course_code, database)
    professorID = get_professor_id(name, database)

    section = (instruction_type, section_code.upper(), term_code.upper(), courseID, professorID)

    cursor = database.cursor()
    sql = "SELECT sectionID FROM current_class_section WHERE instruction_type = %s AND " \
        + "section_code = %s AND term_code = %s AND courseID = %s AND professorID = %s"
    cursor.execute(sql, section)
    id_list = cursor.fetchall()

    if len(id_list) != 0:
        cursor.close()
        return id_list[0][0]

    sql = "INSERT INTO current_class_section (instruction_type, section_code, " \
        + "term_code, courseID, professorID) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, section)
    database.commit()

    sql = "SELECT sectionID FROM current_class_section WHERE instruction_type = %s AND " \
        + "section_code = %s AND term_code = %s AND courseID = %s AND professorID = %s"
    cursor.execute(sql, section)
    id_list = cursor.fetchall()

    cursor.close()
    return id_list[0][0]
    
def insert_recurring_meeting( day_code, start_time, end_time, roomID, sectionID, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Inserts the specified meeting into the database if not already present. Used
    for meetings that happen on a weekly basis, like lectures.

    Parameters:
    day_code (String): The day the meeting is on (e.g. 'TU')
    start_time (String): The starting time of the meeting in 24-hour time. String must 
        be in the format 'HHMMSS' (e.g. '110000' is 11:00:00). Be careful, as '1100' 
        is interpeted as 00:11:00, or 0 hours and 11 minutes. 
    end_time (String): The ending time of the meeting in 24-hour time. String must
        be in the format 'HHMMSS' (e.g. '110000' is 11:00:00). Be careful, as '1100' 
        is interpeted as 00:11:00, or 0 hours and 11 minutes. 
    roomID (Integer): the id of a room in the database. Use get_room_id() for this. Use 
        None if there is no room for the meeting.
    sectionID (Integer): the id of a section in the database. Use get_section_id() for this. 
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: void
    '''
    meeting = (day_code.upper(), start_time, end_time, roomID, sectionID)

    cursor = database.cursor()
    sql = "SELECT * FROM current_section_meeting WHERE day_code = %s AND " \
        + "start_time = %s AND end_time = %s AND roomID = %s AND sectionID = %s"
    cursor.execute(sql, meeting)
    meeting_list = cursor.fetchall()

    if len(meeting_list) != 0:
        cursor.close()
        return

    sql = "INSERT INTO current_section_meeting (day_code, start_time, " \
        + "end_time, roomID, sectionID) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, meeting)
    database.commit()
    cursor.close()


def insert_one_time_meeting( meeting_type, meeting_date, start_time, end_time, roomID, sectionID, database):
    '''
    NOTE: should not be vulnerable to SQL injection, but untested 

    Inserts the specified meeting into the database if not already present. Used
    for meetings that happen only once, like midterms or finals.

    Parameters:
    meeting_type (String): The type of meeting this is (e.g. 'FI' for final)
    meeting_date (String): The date of the meeting in the format 'YYYY-MM-DD' 
        (e.g. '2020-05-19' is May 19th, 2020)
    start_time (String): The starting time of the meeting in 24-hour time. String must 
        be in the format 'HH:MM:SS' (e.g. '11:00:00' is 11:00:00). Be careful, as '11:00' 
        is interpeted as 00:11:00, or 0 hours and 11 minutes. 
    end_time (String): The ending time of the meeting in 24-hour time. String must
        be in the format 'HH:MM:SS' (e.g. '11:00:00' is 11:00:00). Be careful, as '11:00' 
        is interpeted as 00:11:00, or 0 hours and 11 minutes. 
    roomID (Integer): the id of a room in the database. Use get_room_id() for this. Use 
        None if there is no room for the meeting.
    sectionID (Integer): the id of a section in the database. Use get_section_id() for this. 
    database (mysql database): The connection to the asap_database. Use 
        get_database() to get this value.

    Returns: void
    '''
    meeting = (meeting_type.upper(), meeting_date, start_time, end_time, roomID, sectionID)

    cursor = database.cursor()
    sql = "SELECT * FROM current_additional_meeting WHERE meeting_type = %s AND " \
        + "meeting_date = %s AND start_time = %s AND end_time = %s AND roomID = %s" \
        + " AND sectionID = %s"
    cursor.execute(sql, meeting)
    meeting_list = cursor.fetchall()

    if len(meeting_list) != 0:
        cursor.close()
        return

    sql = "INSERT INTO current_additional_meeting (meeting_type, meeting_date, start_time, " \
        + "end_time, roomID, sectionID) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, meeting)
    database.commit()
    cursor.close()