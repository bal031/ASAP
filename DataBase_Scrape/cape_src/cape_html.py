from bs4 import BeautifulSoup
import requests, pickle
import os


url = "http://cape.ucsd.edu/responses/Results.aspx?"
name = "Name="
crsNum = "CourseNumber="
path = "/Cape_HTML"

headers = {"User-Agent":
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
}
#requests session that loads in cookies provided by a Selenium login, cookie only lasts an hour or so
s = requests.Session()
s.headers.update(headers)
with open('CapeCookies.txt', 'rb') as f:
    s.cookies.update(pickle.load(f))
#print(s.cookies)
#Opens up Departments.txt and downloads the html pages for each departmentd
with open("Departments.txt") as f:
    lines = f.readlines()
    for department in lines:
        page = s.get(url + name + "&" + crsNum + department)
        with open(path + department.rstrip() + '.html', 'wb') as f:
            pickle.dump(page.text, f)
        print(page.status_code)

#with open('Cape_Cse.txt', 'wb') as f:
    #pickle.dump(page.text, f)
