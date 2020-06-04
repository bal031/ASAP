# ![ASAP Logo](resources/favicon.ico "Autoscheduler Assist Program") Autoscheduler Assist Program 
ASAP is a web application that intends to ease the burden of a UCSD student amidst course planning for a looming quarter. Simply select the courses you wish to take and denote any preferences (e.g. classes with high CAPE reviews) then sit back while the algorithm does all
of the heavy lifting of finding the best possible schedule. 

## Team ASAP
* James Li - @JamesOnEarth - Senior System Analyst
* Yiyan Chen - @YiyanChen - Algorithm Specialist
* Levent Horvath - Project Manager
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
Note: It is safe to assume most desktop browsers will be able to use the site. 
* Firefox Version 77.x.x
* Chrome Version 83.0.xxx.xx
* Safari Version 13.x.x
* Internet Explorer 11
* Microsoft Edge 44.xxxxx.xxx.x


## Known Bugs
* Generating a schedule for multiple classes with a lot of open sections will cause the system to return a valid schedule very slowly. 
* 

## How It Works
ASAP takes in the class list from the client
`testing `
The algorithm grabs information of each section that are offered for the courses the user selected. It then iterates over all combinations of sections of must-take user courses. If a must-take course cannot be accommodated, the schedule with those sections is marked as invalid and tossed away. Once a valid schedule of must-take sections is found, the algorithm proceeds to place sections want-to-take user courses into the existing must-take schedule. If a want-to-take course cannot be accommodated, the schedule remains valid. The valid schedule with the most want-to-takes fitted is returned. If there are multiple valid schedules with the most want-to-takes, each schedule is scored based on selected preferences, and the one with the highest score is returned.


---

## Building and Deploying
