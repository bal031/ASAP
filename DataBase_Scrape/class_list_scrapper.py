import requests
from bs4 import BeautifulSoup

f = open("search.json", "w")
f.write('[\n');

page=requests.get("http://m.ucsd.edu/scheduleofclasses/term/FA20/")

soup=BeautifulSoup(page.text,'html.parser')
department_list=soup.find('ol')
departments=department_list.find_all('a')

for department in departments:
    subpage=requests.get("http://m.ucsd.edu/scheduleofclasses/term/FA20/"+department.get('href'))
    soup2=BeautifulSoup(subpage.text,'html.parser')
    subject_list=soup2.find('ol')
    subjects=subject_list.find_all('a')
    for subject in subjects:
        subsubpage=requests.get("http://m.ucsd.edu/scheduleofclasses/term/FA20/"+department.get('href')+subject.get('href'))
        soup3=BeautifulSoup(subsubpage.text,'html.parser')
        course_list=soup3.find('ol')
        try:
            courses=course_list.find_all('a')
        except:
            continue;
        for course in courses:
                f.write('\t{"name":"'+course.contents[0]+'"},\n')

f.write(']');
f.close();
