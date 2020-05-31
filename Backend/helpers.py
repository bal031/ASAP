# from Nate
#    given a section ID i need courseName and professor name
# getSectionByID. use section key then instructor key.
# from Will
#    get_capes_by_course_and_prof()
#    get_database();
#   close_database();
#    given a professor name and a course name i need
#       rating
#       average GPA
#       timeSpent
import sys
sys.path.append('/home/dat/ASAP/DataBase_Scrape/')
sys.path.append('/home/dat/ASAP/Backend/database/')
from ScheduleofClasses import getSectionByID
from Database import get_database

def score_by_capes(sectionIDs):
    scores = {'gpa':'-1', 'prof':'-1', 'timeSpent':'-1'}
    db = get_database()
    for secID in sectionIDs:
        # get professor name and course name
        response = getSectionByID(secID)

        course = response['subjectCode'] +  ' ' + response['courseCode']
        instructors = list()
        for section in response['sections']:
            for instructor in section['instructors']:
                instructors.append(instructor['instructorName'])
        courseName = course
        instructorName = str(instructors)

        






# given a list of section id get, professor rating for each section and calculate average rating
def scoreProf(prof_ratings):
    sum = 0
    for position in range(len(prof_ratings)):
        sum += prof_ratings[position]
    sum = sum / len(prof_ratings)
    return sum;

# given a list of section id get expected GPA of that class with that professor,
# and calculate the expected GPA for the quarter
def scoreGPA(GPAList):
    sum = 0;
    for position in range(len(GPAList)):
        sum += GPAList[position]
    sum = sum / len(GPAList)
    return sum;

# given a list of section id get the time spent for each class with that professor, 
# and calculate the average time spent per class.
def scoreTimeSpent(timeSpent):
    sum = 0 
    for position in range(len(timeSpent)):
        sum += timeSpent[position]
    sum = sum / len(timeSpent)
    return sum

#given a list of section id, get the class days and return the number of days the user have class
def scoreClassDay(days):
    return len(set(days))

# given a list of section id, get the start time and end time
# sort time by day
# calculate average gap between classes
"""
def scoreGaps(startTime, endTime):
    for position in range(len(endTime) - 1):
        if 
"""

if __name__ == "__main__":
    # execute only if run as a script
    sectionIDs = ["021116"]
    score_by_capes(sectionIDs)





    """
    rating_input = [90, 80, 95, 89]
    print(scoreProf( rating_input ))
    gpa_input = [3, 3.5, 3.8, 3.9]
    print(scoreProf( gpa_input ))
    timeSpent_input = [7, 5, 6, 8, 12]
    print(scoreTimeSpent(timeSpent_input))
    classDay_input = [ "Mo", "Mo", "Tu", "We", "Fr", "Fr"]
    print(scoreClassDay(classDay_input))
    """