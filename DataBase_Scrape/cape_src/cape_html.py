"""
Downloads HTML files using an active cookie
"""
from bs4 import BeautifulSoup
import requests, pickle
import os
import threading

def main():
    url = "http://cape.ucsd.edu/responses/Results.aspx?"
    name = "Name="
    crsNum = "CourseNumber="
    path = "./Cape_HTML(Updated)/"

    headers = {"User-Agent":
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    #requests session that loads in cookies provided by a Selenium login, cookie only lasts an hour or so
    s = requests.Session()
    s.headers.update(headers)
    #loads in cookie from previous Selenium session dump
    with open('CapeCookies.txt', 'rb') as f:
        s.cookies.update(pickle.load(f))
    #Opens up Departments.txt and downloads the html pages for each departmentd
    x = []
    with open("Departments.txt") as f:
        lines = f.readlines()
        for department in lines:
            x.append(threading.Thread(target=download_page, args=(path + department.rstrip() + '.html', url + name + "&" + crsNum + department, s)))
            x[-1].start()


def download_page(path, url, s):
    """
    Downlaods the HTML file at the given url
    :param path: Where to download the file to
    :param url: URL to download from
    :param s: The session to use
    :return:
    """
    page = s.get(url)
    with open(path, 'wb') as f:
        pickle.dump(page.text, f)
    print(page.status_code)


if __name__ == "__main__":
    main()
