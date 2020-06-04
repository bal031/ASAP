# ![ASAP Logo](resources/favicon.ico "Autoscheduler Assist Program") Autoscheduler Assist Program 
ASAP is a web application that intends to assit a UCSD student burdened with course planning for a looming quarter. Simply select the courses you wish to take and denote any preferences (e.g. classes with high CAPE reviews) then sit back while the algorithm does all
of the heavy lifting of finding the best possible schedule. 

## Team ASAP
* James Li - @JamesOnEarth - Senior System Analyst
* Yiyan Chen - @YiyanChen - Algorithm Specialist
* Levent Horvath - @lhorvath13 - Project Manager
* Nathan Krause - @N-T-K - Software Architect
* Dan Liu - @DanchengLiu - Business Analyst 
* Brian Lu - @bal031 - Software Development Lead
* William Simpson - @williamcsimpson - Database Specialist
* Dat Ta - @dqta21 - Algorithm Specialist
* Huan Mai - @FriendlyHM - Quality Assurance
* Hung Tong - @hungntong - User Interface Specialist


## How To Use
1. Navigate to [asap.ucsd.edu](http://asap.ucsd.edu)
2. Select the quarter you wish to plan for and add the class to the course list. Be sure to note if you must have it in the schedule.
3. Click done and choose your preferences for the algorithm to prioritize. 
4. Click generate and then view the returned schedule below. 
It's that easy!

## Supported Browsers
Note: Desktops are the intended endpoint; however, a user may get away with using a mobile device, but screen size may be an issue as this platform is not officially supported. 

Desktop Browsers:
* Firefox Version 77.x.x
* Chrome Version 83.0.xxx.xx
* Safari Version 13.x.x
* Microsoft Edge 44.xxxxx.xxx.x



## Known Bugs
* Generating a schedule for multiple classes with a lot of open sections will cause the system to return a valid schedule very slowly. 
* UCSD's Schedule of Classes database may show open seats when WebReg reports a full section. This is a university problem. 
* Classes sometimes do not have meeting times scheduled or they're denoted as "TBA" thus a schedule cannot be generated where those are included.  

## How It Works
Once the user selects there classes and clicks generate the list is sent to the server where all of the processing will occur. The server queries the Schedule of Classes Database getting the most recent class times and current enrollment then passes it over to the algorithm where the section selection takes place. 

The algorithm grabs information of each section that are offered for the courses the user selected. It then iterates over all combinations of sections of must-take user courses. If a must-take course cannot be accommodated, the schedule with those sections is marked as invalid and tossed away. Once a valid schedule of must-take sections is found, the algorithm proceeds to place sections want-to-take user courses into the existing must-take schedule. If a want-to-take course cannot be accommodated, the schedule remains valid. The valid schedule with the most want-to-takes fitted is returned. If there are multiple valid schedules with the most want-to-takes, each schedule is scored based on selected preferences, and the one with the highest score is returned.


# Building and Deploying a Server Instance
Note: This application was initially developed and deployed on a CentOS 8 virtual machine. 

Python Server and Processing
---
The server side component of this application was developed using Python 3.6.8

`$ python3 --version`

Any version of Python 3.x.x will most likey work. 
There are a few external libraries utilized througout this build:
* [python-socketio](https://python-socketio.readthedocs.io/en/latest/server.html)
* [aiohttp](https://docs.aiohttp.org/en/stable/)
* [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html)

Installation should be done in a virtual environment or with a package manager such as `pip3`:

`$ pip3 install <package-name>`

In order to start the server open port 80 on the OS firewall. For CentOS 8

`$ sudo firewall-cmd --zone=public --add-service=http`

Now to start the program execute order 66

`$ sudo python3 SocketServer.py`

To run it in the background either make it a `systemd service` or use the quick and dirty option:

`$ screen sudo python3 SocketServer.py`

MySQL Database
--- 

The project uses a MySQL database to store CAPE information. To create the database, use the `create_asap_database.sql` file. More detailed instructions are in the head of  `create_asap_database.sql`. To interface with the database, create a user that has `READ`, `WRITE`, and `DELETE` privileges for all tables in the `asap_database` on `localhost`. In `Database.py` change the `USER` constant to the user’s name, and change the `PASSWORD` field to the user’s password. To use `Database.py`, create a connection to the database by using `get_database()`. Use this for the database field in all other methods in `Database.py`. Once you have finished with the connection, close it using`close_database()`. All other methods in `Database.py` are used for inserting, querying, and deleting data from the database.

JavaScript Frameworks
---
No installation is required, the libraries can be found under [Frontend/](Frontend/). The `npm` package manager was used during development
* uikit v3
* FullCalendar.io v4
* jQuery
* tui datepicker
* socket.io