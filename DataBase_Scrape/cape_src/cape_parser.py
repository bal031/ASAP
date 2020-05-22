from bs4 import BeautifulSoup
import os
import re
import Database

#Class to hold courses and to organize the data so it can be sent to the database
class CapeCourse:
    def __init__(self, instructor, crs, term, response, enroll_num, rec_class, rec_instr, study_hrs, avg_grade_exp, avg_grade_rec):
        self.instructor = instructor
        self.crs = crs
        self.term = term
        self.response = response
        self.enroll_num = enroll_num
        self.rec_class = rec_class
        self.rec_instr = rec_instr
        self.study_hrs = study_hrs
        self.avg_grade_exp = avg_grade_exp
        self.avg_grade_rec = avg_grade_rec

    def __str__(self):
        return self.instructor + " " + self.study_hrs



path = './Cape_HTML/'


#main
def main():
    #stores the results of the scrape for all departments
    results = []
    x=[]
    with open('Departments.txt', 'r') as f:
        lines = f.readlines()
        for department in lines:
            parse_file(os.path.join(path,department.rstrip() + '.html'), results)
    for result in results:
        Database.insert_cape(result.crs.split()[0], results.crs.split()[1], result.instructor,
            float(result.avg_grade_exp), float(result.avg_grade_rec), float(result.study_hrs),
            float(result.rec_class.split()[0]), float(result.rec_instr.split()[0]), float(result.response), result.term,
            Database.get_database())


def parse_file(file, results):
    with open(file, 'rb') as file:
        contents = file.read()
        soup = BeautifulSoup(contents, 'lxml')
        #Find all rows of classes with the class info
        courses = soup.find_all('tr', {'class': 'odd'}) + soup.find_all('tr', {'class': 'even'})

        #for each row parse the information and load it into the CapeCourse Class
        for course in courses:
            prof = course.find('td').contents[0]
            term = course.find_all('td')[2].contents[0]
            enroll_num = course.find_all('td')[3].contents[0]
            evals = course.find('span', {'id': re.compile(
                r'ctl00_ContentPlaceHolder1_gvCAPEs_ctl[0-9]{1,10}_lblCAPEsSubmitted')}).contents[0]
            crs = re.search('[A-Z]{2,4} [0-9]{1,3}', course.find('a', {'id': re.compile(
                r'ctl00_ContentPlaceHolder1_gvCAPEs_ctl[0-9]{1,10}_hlViewReport')}).contents[0]).group(0)
            rec_class = course.find('span', {'id': re.compile(
                r'ctl00_ContentPlaceHolder1_gvCAPEs_ctl[0-9]{1,10}_lblPercentRecommendCourse')}).contents[0]
            rec_instr = course.find('span', {'id': re.compile(
                r'ctl00_ContentPlaceHolder1_gvCAPEs_ctl[0-9]{1,10}_lblPercentRecommendInstructor')}).contents[0]
            study_hrs = course.find('span', {'id': re.compile(
                r'ctl00_ContentPlaceHolder1_gvCAPEs_ctl[0-9]{1,10}_lblStudyHours')}).contents[0]
            avg_grade_exp = course.find('span', {'id': re.compile(
                r'ctl00_ContentPlaceHolder1_gvCAPEs_ctl[0-9]{1,10}_lblGradeExpected')}).contents[0]
            avg_grade_rec = course.find('span', {'id': re.compile(
                r'ctl00_ContentPlaceHolder1_gvCAPEs_ctl[0-9]{1,10}_lblGradeReceived')}).contents[0]
            results.append(
                CapeCourse(prof, crs, term, float(evals, enroll_num), enroll_num, rec_class, rec_instr, study_hrs, avg_grade_exp, avg_grade_rec))
        print(file, ": ", len(results))


if __name__ == "__main__":
    main()