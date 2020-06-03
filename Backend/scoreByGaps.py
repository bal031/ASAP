import functools
import sys
sys.path.append('/home/nate/ASAP/DataBase_Scrape/')
sys.path.append('/home/nate/ASAP/Backend/database/')
from ScheduleofClasses import getSectionByID
from Database import get_database, close_database, get_capes_by_course_and_prof, get_professor_id



"""
    comparision function for sorting meetings
    meeting 1 is less than meeting 2 if M1 occurs earlier than M2
"""
def meeting_compare(meeting1, meeting2):
    if meeting1['dayCode'] < meeting2['dayCode']:
        return -1
    elif meeting1['dayCode'] > meeting2['dayCode']:
        return 1
    elif meeting1['dayCode'] == meeting2['dayCode']:
        if meeting1['startTime'] < meeting2['startTime']:
            return -1
        if meeting1['startTime'] > meeting2['startTime']:
            return 1
    return 0

"""
    calculate the largest gap between classes
    input: list of section IDs
    return: list of 2 items, where the first item is the hour amount and second item is minute amount
    ie 2 hours and 30 mins gap will be returned as [2,30]. if there is only 1 meeting for each day of the week
    then gap is 0 hours and 0 mins 
"""
def score_by_gaps(sectionIDs):
    meetings = []

    for secID in sectionIDs:
        # get professor name and course name
        response = getSectionByID(secID)
        for section in response['sections']:
            for recurringMeetings in section['recurringMeetings']:
                day_code = recurringMeetings['dayCode']
                meeting_day = 0
                if day_code == "MO":
                    meeting_day = 1
                elif day_code == "TU":
                    meeting_day = 2
                elif day_code == "WE":
                    meeting_day  = 3
                elif day_code == "TH":
                    meeting_day   = 4
                elif day_code == "FR":
                    meeting_day   = 5
                elif day_code == "SA":
                    meeting_day   = 6
                elif day_code == "SU":
                    meeting_day   = 7
                meeting = {
                    "dayCode": meeting_day,
                    "startTime": int(recurringMeetings['startTime']),
                    "endTime": int(recurringMeetings['endTime'])
                }
                meetings.append(meeting)
    meetings = sorted(meetings, key=functools.cmp_to_key(meeting_compare))
    maxGap = 0
    prev_day_code = 0
    prev_end_time = 0
    current_start_time = 0
    max_start = 0
    max_end = 0
    for m in meetings:
        if(prev_end_time == 0):
            prev_end_time = m['endTime']
            prev_day_code = m['dayCode']
            continue
        current_start_time = m['startTime']
        gap = current_start_time - prev_end_time
        if gap > maxGap :
            if m['dayCode'] == prev_day_code:
                max_start = current_start_time
                max_end = prev_end_time
                maxGap = gap
        prev_end_time = m['endTime']
        prev_day_code = m['dayCode']
    max_start_hour = int(max_start / 100)
    max_start_min  = int(max_start % 100)
    
    max_end_hour = int(max_end / 100)
    max_end_min = int(max_end % 100)
    if max_start_min < max_end_min:
        max_start_min += 60
        max_start_hour -= 1

    gap_hour = max_start_hour - max_end_hour
    gap_min = max_start_min - max_end_min
    return [gap_hour, gap_min]
    #return(str(gap_hour) +" hour(s) and " + str(gap_min) + " minute(s)")

if __name__ == "__main__":
    # execute only if run as a script
    sectionIDs = {"019459", "019462", "019468"}
    print(score_by_gaps(sectionIDs))
    m1 = {'dayCode': 1, 'startTime': 900, 'endTime': 1150}
    m2 = {'dayCode': 2, 'startTime': 1400, 'endTime': 1520}
    m3 = {'dayCode': 2, 'startTime': 800, 'endTime': 1520}
    m4 = {'dayCode': 3, 'startTime': 900, 'endTime': 1150}
    l1 = []
    l1.append(m1)
    l1.append(m2)
    l1.append(m3)
    l1.append(m4)
    meetings = sorted(l1, key=functools.cmp_to_key(meeting_compare))