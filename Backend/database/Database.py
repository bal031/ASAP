# This module is used for communicating with the asap_database. Use the 
# to close it once finished.
#
#   they have not been tested. Proceed with caution.  

import mysql.connector

USER = 'python'
PASSWORD = 'password'
DATABASE = 'asap_database'
HOST = 'localhost'

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
    expected_grade (Float): From 0.0 to 4.0
    hours_per_week (Float): Minimum 0.0
    received_grade (Float): From 0.0 to 4.0
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


# The following is used to test the methods. TODO: Delete in production build.
asap_database = get_database()
insert_cape("cse", "100", "Ord, Rick", 2.7, 2.3, 14.7, 80.4, 99.7, 77.43, "WI17", asap_database)
print(get_course_id("notDep", "doesntExist", asap_database))
print(get_professor_id("Gillespie, Test", asap_database))
cse100a00 = get_section_id("cse", "100", "Gillespie, Test", "LE", "A00", "SP20", asap_database)
wlh200a = get_room_id("wlh","200a", asap_database)
print(cse100a00)
print(wlh200a)
insert_one_time_meeting("Fi", "2020-05-19", "12:00:00", "14:59:00", wlh200a, cse100a00, asap_database)
insert_recurring_meeting("mwF", "12:00:00", "14:59:00", wlh200a, cse100a00, asap_database)
close_database(asap_database)