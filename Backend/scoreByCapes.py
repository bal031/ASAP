import sys
sys.path.append('/home/dat/ASAP/DataBase_Scrape/')
sys.path.append('/home/dat/ASAP/Backend/database/')
from ScheduleofClasses import getSectionByID
from Database import get_database, close_database, get_capes_by_course_and_prof, get_professor_id

"""
    score by capes scores each section using cape data
    input: list of section IDs
    return: list of cape rating for each associated section IDs
"""
def score_by_capes(sectionIDs):
    scores = {'gpa':'-1', 'prof':'-1', 'timeSpent':'-1'}
    database = get_database()
    capes = get_capes_by_course_and_prof("CSE", "110", "Gillespie, Gary N", database)

    sections_ratings = []

    for secID in sectionIDs:
        # get professor name and course name
        response = getSectionByID(secID)

        subject_code = response['subjectCode'] 
        course_code = response['courseCode']
        course_name = subject_code + ' ' + course_code
        instructors = list()
        for section in response['sections']:
            for instructor in section['instructors']:
                instructors.append(instructor['instructorName'])
        instructor_name = str(instructors).replace('[', '')
        instructor_name = instructor_name.replace('\'', '')
        instructor_name = instructor_name.replace(']', '')

        capes = get_capes_by_course_and_prof(subject_code, course_code, instructor_name , database)
        
        grade_sum = 0
        grade_count = 0
        rating_sum = 0
        rating_count = 0
        time_spent_sum = 0
        time_spent_count = 0
        for i in range(len(capes)):
            for key in capes[i]:
                if key == "received_grade":
                    grade_sum += capes[i][key]
                    grade_count += 1
                if key == "recommend_professor":
                    rating_sum += capes[i][key]
                    rating_count += 1
                if key == "hours_per_week":
                    time_spent_sum += capes[i][key]
                    time_spent_count += 1

        grade_avg = grade_sum / grade_count
        rating_avg = rating_sum / rating_count
        time_spent_avg = time_spent_sum / time_spent_count
        cape_dict = {
            "section ID": secID,
            "grade": grade_avg,
            "rating": rating_avg,
            "time spent": time_spent_avg
        }
        sections_ratings.append(cape_dict)
    close_database(database)
    return sections_ratings

if __name__ == "__main__":
    # execute only if run as a script
    sectionIDs = {"021682", "021686", "022097", "016644"}	
    section_rating_list = score_by_capes(sectionIDs)
    for dictionary in section_rating_list:
        for key in dictionary:
            print(key + ": " + str(dictionary[key]))