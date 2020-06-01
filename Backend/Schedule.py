import scoreByCapes

def schedule_day(meetings):
    last_end = -1
    for end,start in sorted( (end,start) for start,end in meetings ):
        if start >= last_end:
            last_end = end
        elif start < last_end:
        	return False

    return True

def checkConflict(meetings,optional):
    last_end = -1
    joint = meetings + optional
    for end,start in sorted( (end,start) for start,end in joint ):
        if start >= last_end:
            last_end = end
        elif start < last_end:
        	return True

    return False


def schedule(must_haves, want_to_haves):
	result = False;
	schedules = []
	for section1 in must_haves[0]:
		for section2 in must_haves[1]:
			for section3 in must_haves[2]:
				for section4 in must_haves[3]:
					for section5 in must_haves[4]:
						for section6 in must_haves[5]:
							for section7 in must_haves[6]:
								for section8 in must_haves[7]:
									monday = []
									tuesday = []
									wednesday = []
									thursday = []
									friday = []
									saturday = []
									sunday = []
									finalMonday = []
									finalTuesday = []
									finalWednesday = []
									finalThursday = []
									finalFriday = []
									finalSaturday = []
									finalSunday = []
									if(section1 != None):
										for meetings in section1['meetings']:
											if(meetings[0] == 'MO'):
												monday.append(meetings[1:])
											elif(meetings[0] == 'TU'):
												tuesday.append(meetings[1:])
											elif(meetings[0] == 'WE'):
												wednesday.append(meetings[1:])
											elif(meetings[0] == 'TH'):
												thursday.append(meetings[1:])
											elif(meetings[0] == 'FR'):
												friday.append(meetings[1:])
											elif(meetings[0] == 'SA'):
												saturday.append(meetings[1:])
											elif(meetings[0] == 'SU'):
												sunday.append(meetings[1:])
										if(len(section1['finals']) == 3):
											if(section1['finals'][0] == 'MO'):
												finalMonday.append(section1['finals'][1:])
											elif(section1['finals'][0] == 'TU'):
												finalTuesday.append(section1['finals'][1:])
											elif(section1['finals'][0] == 'WE'):
												finalWednesday.append(section1['finals'][1:])
											elif(section1['finals'][0] == 'TH'):
												finalThursday.append(section1['finals'][1:])
											elif(section1['finals'][0] == 'FR'):
												finalFriday.append(section1['finals'][1:])
											elif(section1['finals'][0] == 'SA'):
												finalSaturday.append(section1['finals'][1:])
											elif(section1['finals'][0] == 'SU'):
												finalSunday.append(section1['finals'][1:])
									if(section2 != None):
										for meetings in section2['meetings']:
											if(meetings[0] == 'MO'):
												monday.append(meetings[1:])
											elif(meetings[0] == 'TU'):
												tuesday.append(meetings[1:])
											elif(meetings[0] == 'WE'):
												wednesday.append(meetings[1:])
											elif(meetings[0] == 'TH'):
												thursday.append(meetings[1:])
											elif(meetings[0] == 'FR'):
												friday.append(meetings[1:])
											elif(meetings[0] == 'SA'):
												saturday.append(meetings[1:])
											elif(meetings[0] == 'SU'):
												sunday.append(meetings[1:])
										if(len(section2['finals']) == 3):
											if(section2['finals'][0] == 'MO'):
												finalMonday.append(section2['finals'][1:])
											elif(section2['finals'][0] == 'TU'):
												finalTuesday.append(section2['finals'][1:])
											elif(section2['finals'][0] == 'WE'):
												finalWednesday.append(section2['finals'][1:])
											elif(section2['finals'][0] == 'TH'):
												finalThursday.append(section2['finals'][1:])
											elif(section2['finals'][0] == 'FR'):
												finalFriday.append(section2['finals'][1:])
											elif(section2['finals'][0] == 'SA'):
												finalSaturday.append(section2['finals'][1:])
											elif(section2['finals'][0] == 'SU'):
												finalSunday.append(section2['finals'][1:])
									if(section3 != None):
										for meetings in section3["meetings"]:
											if(meetings[0] == 'MO'):
												monday.append(meetings[1:])
											elif(meetings[0] == 'TU'):
												tuesday.append(meetings[1:])
											elif(meetings[0] == 'WE'):
												wednesday.append(meetings[1:])
											elif(meetings[0] == 'TH'):
												thursday.append(meetings[1:])
											elif(meetings[0] == 'FR'):
												friday.append(meetings[1:])
											elif(meetings[0] == 'SA'):
												saturday.append(meetings[1:])
											elif(meetings[0] == 'SU'):
												sunday.append(meetings[1:])
										if(len(section3['finals']) == 3):
											if(section3['finals'][0] == 'MO'):
												finalMonday.append(section3['finals'][1:])
											elif(section3['finals'][0] == 'TU'):
												finalTuesday.append(section3['finals'][1:])
											elif(section3['finals'][0] == 'WE'):
												finalWednesday.append(section3['finals'][1:])
											elif(section3['finals'][0] == 'TH'):
												finalThursday.append(section3['finals'][1:])
											elif(section3['finals'][0] == 'FR'):
												finalFriday.append(section3['finals'][1:])
											elif(section3['finals'][0] == 'SA'):
												finalSaturday.append(section3['finals'][1:])
											elif(section3['finals'][0] == 'SU'):
												finalSunday.append(section3['finals'][1:])
									if(section4 != None):
										for meetings in section4["meetings"]:
											if(meetings[0] == 'MO'):
												monday.append(meetings[1:])
											elif(meetings[0] == 'TU'):
												tuesday.append(meetings[1:])
											elif(meetings[0] == 'WE'):
												wednesday.append(meetings[1:])
											elif(meetings[0] == 'TH'):
												thursday.append(meetings[1:])
											elif(meetings[0] == 'FR'):
												friday.append(meetings[1:])
											elif(meetings[0] == 'SA'):
												saturday.append(meetings[1:])
											elif(meetings[0] == 'SU'):
												sunday.append(meetings[1:])
										if(len(section4['finals']) == 3):
											if(section4['finals'][0] == 'MO'):
												finalMonday.append(section4['finals'][1:])
											elif(section4['finals'][0] == 'TU'):
												finalTuesday.append(section4['finals'][1:])
											elif(section4['finals'][0] == 'WE'):
												finalWednesday.append(section4['finals'][1:])
											elif(section4['finals'][0] == 'TH'):
												finalThursday.append(section4['finals'][1:])
											elif(section4['finals'][0] == 'FR'):
												finalFriday.append(section4['finals'][1:])
											elif(section4['finals'][0] == 'SA'):
												finalSaturday.append(section4['finals'][1:])
											elif(section4['finals'][0] == 'SU'):
												finalSunday.append(section4['finals'][1:])
									if(section5 != None):
										for meetings in section5["meetings"]:
											if(meetings[0] == 'MO'):
												monday.append(meetings[1:])
											elif(meetings[0] == 'TU'):
												tuesday.append(meetings[1:])
											elif(meetings[0] == 'WE'):
												wednesday.append(meetings[1:])
											elif(meetings[0] == 'TH'):
												thursday.append(meetings[1:])
											elif(meetings[0] == 'FR'):
												friday.append(meetings[1:])
											elif(meetings[0] == 'SA'):
												saturday.append(meetings[1:])
											elif(meetings[0] == 'SU'):
												sunday.append(meetings[1:])
										if(len(section5['finals']) == 3):
											if(section5['finals'][0] == 'MO'):
												finalMonday.append(section5['finals'][1:])
											elif(section5['finals'][0] == 'TU'):
												finalTuesday.append(section5['finals'][1:])
											elif(section5['finals'][0] == 'WE'):
												finalWednesday.append(section5['finals'][1:])
											elif(section5['finals'][0] == 'TH'):
												finalThursday.append(section5['finals'][1:])
											elif(section5['finals'][0] == 'FR'):
												finalFriday.append(section5['finals'][1:])
											elif(section5['finals'][0] == 'SA'):
												finalSaturday.append(section5['finals'][1:])
											elif(section5['finals'][0] == 'SU'):
												finalSunday.append(section5['finals'][1:])
									if(section6 != None):
										for meetings in section6["meetings"]:
											if(meetings[0] == 'MO'):
												monday.append(meetings[1:])
											elif(meetings[0] == 'TU'):
												tuesday.append(meetings[1:])
											elif(meetings[0] == 'WE'):
												wednesday.append(meetings[1:])
											elif(meetings[0] == 'TH'):
												thursday.append(meetings[1:])
											elif(meetings[0] == 'FR'):
												friday.append(meetings[1:])
											elif(meetings[0] == 'SA'):
												saturday.append(meetings[1:])
											elif(meetings[0] == 'SU'):
												sunday.append(meetings[1:])
										if(len(section6['finals']) == 3):
											if(section6['finals'][0] == 'MO'):
												finalMonday.append(section6['finals'][1:])
											elif(section6['finals'][0] == 'TU'):
												finalTuesday.append(section6['finals'][1:])
											elif(section6['finals'][0] == 'WE'):
												finalWednesday.append(section6['finals'][1:])
											elif(section6['finals'][0] == 'TH'):
												finalThursday.append(section6['finals'][1:])
											elif(section6['finals'][0] == 'FR'):
												finalFriday.append(section6['finals'][1:])
											elif(section6['finals'][0] == 'SA'):
												finalSaturday.append(section6['finals'][1:])
											elif(section6['finals'][0] == 'SU'):
												finalSunday.append(section6['finals'][1:])
									if(section7 != None):
										for meetings in section7["meetings"]:
											if(meetings[0] == 'MO'):
												monday.append(meetings[1:])
											elif(meetings[0] == 'TU'):
												tuesday.append(meetings[1:])
											elif(meetings[0] == 'WE'):
												wednesday.append(meetings[1:])
											elif(meetings[0] == 'TH'):
												thursday.append(meetings[1:])
											elif(meetings[0] == 'FR'):
												friday.append(meetings[1:])
											elif(meetings[0] == 'SA'):
												saturday.append(meetings[1:])
											elif(meetings[0] == 'SU'):
												sunday.append(meetings[1:])
										if(len(section7['finals']) == 3):
											if(section7['finals'][0] == 'MO'):
												finalMonday.append(section7['finals'][1:])
											elif(section7['finals'][0] == 'TU'):
												finalTuesday.append(section7['finals'][1:])
											elif(section7['finals'][0] == 'WE'):
												finalWednesday.append(section7['finals'][1:])
											elif(section7['finals'][0] == 'TH'):
												finalThursday.append(section7['finals'][1:])
											elif(section7['finals'][0] == 'FR'):
												finalFriday.append(section7['finals'][1:])
											elif(section7['finals'][0] == 'SA'):
												finalSaturday.append(section7['finals'][1:])
											elif(section7['finals'][0] == 'SU'):
												finalSunday.append(section7['finals'][1:])
									if(section8 != None):
										for meetings in section8["meetings"]:
											if(meetings[0] == 'MO'):
												monday.append(meetings[1:])
											elif(meetings[0] == 'TU'):
												tuesday.append(meetings[1:])
											elif(meetings[0] == 'WE'):
												wednesday.append(meetings[1:])
											elif(meetings[0] == 'TH'):
												thursday.append(meetings[1:])
											elif(meetings[0] == 'FR'):
												friday.append(meetings[1:])
											elif(meetings[0] == 'SA'):
												saturday.append(meetings[1:])
											elif(meetings[0] == 'SU'):
												sunday.append(meetings[1:])
										if(len(section8['finals']) == 3):
											if(section8['finals'][0] == 'MO'):
												finalMonday.append(section8['finals'][1:])
											elif(section8['finals'][0] == 'TU'):
												finalTuesday.append(section8['finals'][1:])
											elif(section8['finals'][0] == 'WE'):
												finalWednesday.append(section8['finals'][1:])
											elif(section8['finals'][0] == 'TH'):
												finalThursday.append(section8['finals'][1:])
											elif(section8['finals'][0] == 'FR'):
												finalFriday.append(section8['finals'][1:])
											elif(section8['finals'][0] == 'SA'):
												finalSaturday.append(section8['finals'][1:])
											elif(section8['finals'][0] == 'SU'):
												finalSunday.append(section8['finals'][1:])

									if(schedule_day(monday) == True and schedule_day(tuesday) == True and schedule_day(wednesday) == True and schedule_day(thursday) == True and schedule_day(friday) == True and schedule_day(saturday) == True and schedule_day(sunday) == True and schedule_day(finalMonday) == True and schedule_day(finalTuesday) == True and schedule_day(finalWednesday) == True and schedule_day(finalThursday) == True and schedule_day(finalFriday) == True and schedule_day(finalSaturday) == True and schedule_day(finalSunday) == True):
										result = True;

										for optional1 in want_to_haves[0]:
											for optional2 in want_to_haves[1]:
												for optional3 in want_to_haves[2]:
													for optional4 in want_to_haves[3]:
														for optional5 in want_to_haves[4]:
															for optional6 in want_to_haves[5]:
																for optional7 in want_to_haves[6]:
																	optionalMonday = []
																	optionalTuesday = []
																	optionalWednesday = []
																	optionalThursday = []
																	optionalFriday = []
																	optionalSaturday = []
																	optionalSunday = []
																	optionalFinalMonday = []
																	optionalFinalTuesday = []
																	optionalFinalWednesday = []
																	optionalFinalThursday = []
																	optionalFinalFriday = []
																	optionalFinalSaturday = []
																	optionalFinalSunday = []

																	if(optional1 != None):
																		for optMeetings in optional1["meetings"]:
																			if(optMeetings[0] == 'MO'):
																				optionalMonday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TU'):
																				optionalTuesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'WE'):
																				optionalWednesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TH'):
																				optionalThursday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'FR'):
																				optionalFriday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SA'):
																				optionalSaturday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SU'):
																				optionalSaturday.append(optMeetings[1:])
																		if(len(optional1['finals']) == 3):
																			if(optional1['finals'][0] == 'MO'):
																				optionalFinalMonday.append(optional1['finals'][1:])
																			elif(optional1['finals'][0] == 'TU'):
																				optionalFinalTuesday.append(optional1['finals'][1:])
																			elif(optional1['finals'][0] == 'WE'):
																				optionalFinalWednesday.append(optional1['finals'][1:])
																			elif(optional1['finals'][0] == 'TH'):
																				optionalFinalThursday.append(optional1['finals'][1:])
																			elif(optional1['finals'][0] == 'FR'):
																				optionalFinalFriday.append(optional1['finals'][1:])
																			elif(optional1['finals'][0] == 'SA'):
																				optionalFinalSaturday.append(optional1['finals'][1:])
																			elif(optional1['finals'][0] == 'SU'):
																				optionalFinalSunday.append(optional1['finals'][1:])
																	
																	if(optional2 != None):
																		for optMeetings in optional2["meetings"]:
																			if(optMeetings[0] == 'MO'):
																				optionalMonday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TU'):
																				optionalTuesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'WE'):
																				optionalWednesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TH'):
																				optionalThursday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'FR'):
																				optionalFriday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SA'):
																				optionalSaturday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SU'):
																				optionalSaturday.append(optMeetings[1:])
																		if(len(optional2['finals']) == 3):
																			if(optional2['finals'][0] == 'MO'):
																				optionalFinalMonday.append(optional2['finals'][1:])
																			elif(optional2['finals'][0] == 'TU'):
																				optionalFinalTuesday.append(optional2['finals'][1:])
																			elif(optional2['finals'][0] == 'WE'):
																				optionalFinalWednesday.append(optional2['finals'][1:])
																			elif(optional2['finals'][0] == 'TH'):
																				optionalFinalThursday.append(optional2['finals'][1:])
																			elif(optional2['finals'][0] == 'FR'):
																				optionalFinalFriday.append(optional2['finals'][1:])
																			elif(optional2['finals'][0] == 'SA'):
																				optionalFinalSaturday.append(optional2['finals'][1:])
																			elif(optional2['finals'][0] == 'SU'):
																				optionalFinalSunday.append(optional2['finals'][1:])

																	if(optional3 != None):
																		for optMeetings in optional3["meetings"]:
																			if(optMeetings[0] == 'MO'):
																				optionalMonday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TU'):
																				optionalTuesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'WE'):
																				optionalWednesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TH'):
																				optionalThursday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'FR'):
																				optionalFriday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SA'):
																				optionalSaturday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SU'):
																				optionalSaturday.append(optMeetings[1:])
																		if(len(optional3['finals']) == 3):
																			if(optional3['finals'][0] == 'MO'):
																				optionalFinalMonday.append(optional3['finals'][1:])
																			elif(optional3['finals'][0] == 'TU'):
																				optionalFinalTuesday.append(optional3['finals'][1:])
																			elif(optional3['finals'][0] == 'WE'):
																				optionalFinalWednesday.append(optional3['finals'][1:])
																			elif(optional3['finals'][0] == 'TH'):
																				optionalFinalThursday.append(optional3['finals'][1:])
																			elif(optional3['finals'][0] == 'FR'):
																				optionalFinalFriday.append(optional3['finals'][1:])
																			elif(optional3['finals'][0] == 'SA'):
																				optionalFinalSaturday.append(optional3['finals'][1:])
																			elif(optional3['finals'][0] == 'SU'):
																				optionalFinalSunday.append(optional3['finals'][1:])

																	if(optional4 != None):
																		for optMeetings in optional4["meetings"]:
																			if(optMeetings[0] == 'MO'):
																				optionalMonday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TU'):
																				optionalTuesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'WE'):
																				optionalWednesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TH'):
																				optionalThursday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'FR'):
																				optionalFriday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SA'):
																				optionalSaturday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SU'):
																				optionalSaturday.append(optMeetings[1:])
																		if(len(optional4['finals']) == 3):
																			if(optional4['finals'][0] == 'MO'):
																				optionalFinalMonday.append(optional4['finals'][1:])
																			elif(optional4['finals'][0] == 'TU'):
																				optionalFinalTuesday.append(optional4['finals'][1:])
																			elif(optional4['finals'][0] == 'WE'):
																				optionalFinalWednesday.append(optional4['finals'][1:])
																			elif(optional4['finals'][0] == 'TH'):
																				optionalFinalThursday.append(optional4['finals'][1:])
																			elif(optional4['finals'][0] == 'FR'):
																				optionalFinalFriday.append(optional4['finals'][1:])
																			elif(optional4['finals'][0] == 'SA'):
																				optionalFinalSaturday.append(optional4['finals'][1:])
																			elif(optional4['finals'][0] == 'SU'):
																				optionalFinalSunday.append(optional4['finals'][1:])

																	if(optional5 != None):
																		for optMeetings in optional5["meetings"]:
																			if(optMeetings[0] == 'MO'):
																				optionalMonday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TU'):
																				optionalTuesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'WE'):
																				optionalWednesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TH'):
																				optionalThursday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'FR'):
																				optionalFriday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SA'):
																				optionalSaturday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SU'):
																				optionalSaturday.append(optMeetings[1:])
																		if(len(optional5['finals']) == 3):
																			if(optional5['finals'][0] == 'MO'):
																				optionalFinalMonday.append(optional5['finals'][1:])
																			elif(optional5['finals'][0] == 'TU'):
																				optionalFinalTuesday.append(optional5['finals'][1:])
																			elif(optional5['finals'][0] == 'WE'):
																				optionalFinalWednesday.append(optional5['finals'][1:])
																			elif(optional5['finals'][0] == 'TH'):
																				optionalFinalThursday.append(optional5['finals'][1:])
																			elif(optional5['finals'][0] == 'FR'):
																				optionalFinalFriday.append(optional5['finals'][1:])
																			elif(optional5['finals'][0] == 'SA'):
																				optionalFinalSaturday.append(optional5['finals'][1:])
																			elif(optional5['finals'][0] == 'SU'):
																				optionalFinalSunday.append(optional5['finals'][1:])

																	if(optional6 != None):
																		for optMeetings in optional6["meetings"]:
																			if(optMeetings[0] == 'MO'):
																				optionalMonday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TU'):
																				optionalTuesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'WE'):
																				optionalWednesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TH'):
																				optionalThursday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'FR'):
																				optionalFriday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SA'):
																				optionalSaturday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'SU'):
																				optionalSaturday.append(optMeetings[1:])
																		if(len(optional6['finals']) == 3):
																			if(optional6['finals'][0] == 'MO'):
																				optionalFinalMonday.append(optional6['finals'][1:])
																			elif(optional6['finals'][0] == 'TU'):
																				optionalFinalTuesday.append(optional6['finals'][1:])
																			elif(optional6['finals'][0] == 'WE'):
																				optionalFinalWednesday.append(optional6['finals'][1:])
																			elif(optional6['finals'][0] == 'TH'):
																				optionalFinalThursday.append(optional6['finals'][1:])
																			elif(optional6['finals'][0] == 'FR'):
																				optionalFinalFriday.append(optional6['finals'][1:])
																			elif(optional6['finals'][0] == 'SA'):
																				optionalFinalSaturday.append(optional6['finals'][1:])
																			elif(optional6['finals'][0] == 'SU'):
																				optionalFinalSunday.append(optional6['finals'][1:])

																	if(optional7 != None):
																		for optMeetings in optional7["meetings"]:
																			if(optMeetings[0] == 'MO'):
																				optionalMonday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TU'):
																				optionalTuesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'WE'):
																				optionalWednesday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'TH'):
																				optionalThursday.append(optMeetings[1:])
																			elif(optMeetings[0] == 'FR'):
																				optionalFriday.append(optMeetings[1:])
																			elif(meetings1[0] == 'SA'):
																				optionalSaturday.append(optMeetings[1:])
																			elif(meetings1[0] == 'SU'):
																				optionalSaturday.append(optMeetings[1:])
																		if(len(optional7['finals']) == 3):
																			if(optional7['finals'][0] == 'MO'):
																				optionalFinalMonday.append(optional7['finals'][1:])
																			elif(optional7['finals'][0] == 'TU'):
																				optionalFinalTuesday.append(optional7['finals'][1:])
																			elif(optional7['finals'][0] == 'WE'):
																				optionalFinalWednesday.append(optional7['finals'][1:])
																			elif(optional7['finals'][0] == 'TH'):
																				optionalFinalThursday.append(optional7['finals'][1:])
																			elif(optional7['finals'][0] == 'FR'):
																				optionalFinalFriday.append(optional7['finals'][1:])
																			elif(optional7['finals'][0] == 'SA'):
																				optionalFinalSaturday.append(optional7['finals'][1:])
																			elif(optional7['finals'][0] == 'SU'):
																				optionalFinalSunday.append(optional7['finals'][1:])

																	if(checkConflict(monday,optionalMonday) == False and checkConflict(tuesday,optionalTuesday) == False and checkConflict(wednesday,optionalWednesday) == False and checkConflict(thursday,optionalThursday) == False and checkConflict(friday,optionalFriday) == False and checkConflict(saturday,optionalSaturday) == False and checkConflict(sunday,optionalSunday) == False and checkConflict(monday,optionalFinalMonday) == False and checkConflict(tuesday,optionalFinalTuesday) == False and checkConflict(wednesday,optionalFinalWednesday) == False and checkConflict(thursday,optionalFinalThursday) == False and checkConflict(friday,optionalFinalFriday) == False and checkConflict(saturday,optionalFinalSaturday) == False and checkConflict(sunday,optionalFinalSunday) == False):
																		schedule = []
																		if(section1 != None):
																			schedule.append(section1)
																		if(section2 != None):
																			schedule.append(section2)
																		if(section3 != None):
																			schedule.append(section3)
																		if(section4 != None):
																			schedule.append(section4)
																		if(section5 != None):
																			schedule.append(section5)
																		if(section6 != None):
																			schedule.append(section6)
																		if(section7 != None):
																			schedule.append(section7)
																		if(section8 != None):
																			schedule.append(section8)
																		if(optional1 != None):
																			schedule.append(optional1)
																		if(optional2 != None):
																			schedule.append(optional2)
																		if(optional3 != None):
																			schedule.append(optional3)
																		if(optional4 != None):
																			schedule.append(optional4)
																		if(optional5 != None):
																			schedule.append(optional5)
																		if(optional6 != None):
																			schedule.append(optional6)
																		if(optional7 != None):
																			schedule.append(optional7)
																		schedules.append(schedule)

	
	if(result == True):
		return(schedules)
	else:
		return(schedules)

def generateSchedule(must_haves,want_to_haves,preferences):
	tempMustHaves = must_haves
	tempWantHaves = want_to_haves
	while(len(tempMustHaves) < 8):
		tempMustHaves.append([None])
	for i in want_to_haves:
		i.append(None)
	while(len(tempWantHaves) < 7):
		tempWantHaves.append([None])
	schedules = schedule(tempMustHaves, tempWantHaves)
	totalWeights = 0
	if(len(schedules) == 0):
		return []
	else:
		sectionIDs = parseSchedule(schedules[0])
                #sectionRatings = scoreByCapes.score_by_capes(sectionIDs)
                #print(sectionIDs)
		return schedules[0]


def parseSchedule(schedule):
	sectionIDs = []
	for i in schedule:
		sectionIDs.append(i['id'])
	return sectionIDs

def main():
	# Must-takes/Personal Events
	# 1.CSE 120 TUTH 8:00-9:20 TH 10:00-10:50 @@@
	# 2.CSE 141 MWF 10:00-10:50 W 11:00-11:50 @@@
	# 3.CSE 141 TUTH 3:30-4:50 TU 2:00-2:50
	# 4.CSE 141L M 3:00-3:50 W 3:00-3:50 @@@
	# 5.CSE 141L M 4:00-4:50 W 4:00-4:50 @@@
	# 6.CSE 110 TUTH 2:00-3:20 W 9:00-11:50
	# 7.CSE 110 TUTH 2:00-3:20 W 9:00-11:50
	# 8.CSE 110 TUTH 2:00-3:20 W 9:00-11:50
	# 9.CSE 110 TUTH 2:00-3:20 W 12:00-2:50 @@@
	# 10.CSE 110 TUTH 2:00-3:20 W 12:00-2:50 @@

	# Want-to-takes
	# 11. ECE 107 TUTH 8:00-9:20 F 11:00-11:50
	# 12. CSE 130 MWF 4:00-4:50 TH 5:00-5:50 @@@
	# 13. CSE 111 MWF 4:00-4:50 TH 5:00-5:50


	#Start time, end time, index
	must_takes=[]
	#must_takes.append([{"id":1,"meetings":[["TU",80000,92000],["TH",80000,92000],["TH",100000,105000]]}])
	#must_takes.append([{"id":2,"meetings":[["M",100000,105000],["W",100000,105000],["W",110000,115000],["F",100000,105000]]},{"id":3,"meetings":[["TU",153000,165000],["TU",140000,145000],["TH",153000,165000]]}])
	#must_takes.append([{"id":4,"meetings":[["M",150000,155000],["W",150000,155000]]},{"id":5,"meetings":[["M",160000,165000],["W",160000,165000]]}])
	#must_takes.append([{"id":6,"meetings":[["TU",140000,152000],["TH",140000,152000],["W",90000,115000]],"finals":["M",150000,180000]},{"id":7,"meetings":[["TU",140000,152000],["TH",140000,152000],["W",90000,115000]],"finals":["M",150000,180000]},{"id":8,"meetings":[["TU",140000,152000],["TH",140000,152000],["W",90000,115000]],"finals":["M",150000,180000]},{"id":9,"meetings":[["TU",140000,152000],["TH",140000,152000],["W",120000,145000]],"finals":["M",150000,180000]},{"id":10,"meetings":[["TU",140000,152000],["TH",140000,152000],["W",120000,145000]],"finals":["M",150000,180000]}])
	must_takes.append([{'id': 'personal event', 'meetings': [['TU', 900, 1000], ['TH', 900, 1000]], 'finals': '', 'midterms': ''}])
	must_takes.append([{'meetings': [['TU', 1100, 1220], ['TH',1100, 1220], ['M', 1100, 1150]], 'finals': ['W', 1130, 1429], 'midterms': [], 'LE id': '016900', 'id': '016901'}]);
	must_takes.append([None]);
	must_takes.append([None]);
	must_takes.append([None]);
	must_takes.append([None]);
	must_takes.append([None]);
	must_takes.append([None]);

	want_to_takes=[]
	#want_to_takes.append([{"id":11,"meetings":[["TU",80000,92000],["TH",80000,92000],["F",110000,115000]]},None])
	#want_to_takes.append([{"id":12,"meetings":[["M",160000,165000],["W",160000,165000],["F",160000,165000],["TH",170000,175000]]},None])
	#want_to_takes.append([{"id":13,"meetings":[["M",160000,165000],["W",160000,165000],["F",160000,165000],["TH",170000,175000]]},None]);
	want_to_takes.append([None]);
	want_to_takes.append([None]);
	want_to_takes.append([None]);
	want_to_takes.append([None]);
	want_to_takes.append([None]);
	want_to_takes.append([None]);
	want_to_takes.append([None]);


	schedules = generateSchedule(must_takes,want_to_takes,[])
	print(schedules)
	#max = 0
	#for i in schedules:
#		if len(i) > max:
#			max = len(i)
#
#	final_schedules = []
#	for i in schedules:
#		if len(i) == max:
#			final_schedules.append(i)

#	print(final_schedules)

if __name__ == '__main__':
	main()
