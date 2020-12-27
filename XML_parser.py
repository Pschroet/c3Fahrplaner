import defusedxml.ElementTree

def parse_schedule(xml_content):
    print("Parsing schedule")
    #print xml_content
    tree = defusedxml.ElementTree.fromstring(xml_content, forbid_entities=False)
    if hasattr(tree, "getroot") and callable(tree.getroot):
        root = tree.getroot()
    else:
        root = tree
    #print(root)
    context = {}
    #get the info about the event first
    con_info = root.find("conference")
    #print(con_info)
    context["title"] = con_info.find("title").text
    context["acronym"] = con_info.find("acronym").text
    context["year"] = con_info.find("start").text.split("-"[0])
    context["timeslot"] = con_info.find("timeslot_duration").text
    time_slot_mins = int(context["timeslot"].split(":")[1])
    time_slot_hours = int(context["timeslot"].split(":")[0])
    #get the year, so it can be used in the URLs
    context["year"] = con_info.find("start").text.split("-")[0]
    #get the last day, to determine the expiration date of the cookie
    context["end"] = con_info.find("end").text
    #get the days
    days = root.findall("day")
    #define the temporary variables for collect all information
    temp_days = []
    counter = 0
    for day in days:
        #print("Events for " + day.attrib["date"] + ":")
        #check if the the event is spread over more than one day, e.g. from 10am to 4am the next day
        start_day = int(day.attrib["start"].split("T")[0].split("-")[2])
        end_day = int(day.attrib["end"].split("T")[0].split("-")[2])
        diff_days = 0
        if start_day < end_day:
            diff_days = end_day - start_day
        start_time = day.attrib["start"].split("T")[1].split("+")[0].split(":")
        end_time = day.attrib["end"].split("T")[1].split("+")[0].split(":")
        #calculate the hours and minutes of the time slots and use this to get total number of time slots
        total_time_hours = (diff_days*24) + int(end_time[0]) - int(start_time[1])
        total_time_mins = (total_time_hours*60) + int(end_time[1]) - int(start_time[1])
        total_time_slots = total_time_mins/time_slot_mins
        #get the start time
        time_slots = [start_time[0] + ":" + start_time[1]]
        #calculate the time of the time slots
        temp_time_slot = [int(start_time[0]), int(start_time[1])]
        while temp_time_slot[0] is not int(end_time[0]) or temp_time_slot[1] is not int(end_time[1]):
            #check if the next hour is reached when the next slot in minutes is added
            # if so, add another hour and remove this hour from the minutes
            if not ((int(temp_time_slot[1]) + int(time_slot_mins)) - 60) < 0:
                temp_time_slot[0] += 1
                temp_time_slot[1] -= 60
            #check if another day begins
            # if so, remove 24 hours
            if not ((int(temp_time_slot[0]) + int(time_slot_hours)) - 24) < 0:
                temp_time_slot[0] -= 24
            #add a time slot
            temp_time_slot[0] += int(time_slot_hours)
            temp_time_slot[1] += int(time_slot_mins)
            #if the minutes are zero, still use two digits
            if temp_time_slot[1] == 0:
                temp_time_slot[1] = "00"
            else:
                temp_time_slot[1] = str(temp_time_slot[1])
            #save the new time slot
            time_slots.append(str(temp_time_slot[0]) + ":" + temp_time_slot[1])
            #turn the minutes back into a number
            temp_time_slot[1] = int(temp_time_slot[1])
        #put all information into a dictionary to use later
        temp_days.append({"date":day.attrib["date"], "rooms":[], "start":start_time, "end":end_time, "time_slots": time_slots, "total_time_slots":total_time_slots})
        #get the rooms
        rooms = day.findall("room")
        for room in rooms:
            temp_room = {}
            temp_room["name"] = room.attrib["name"]
            temp_room["events"] = []
            #get the events for this room
            events = room.findall("event")
            for event in events:
                temp_event = {}
                #get the basic information about the event
                temp_event["title"] = event.find("title").text
                temp_event["id"] = event.attrib["id"]
                persons = event.find("persons").findall("person")
                temp_event["persons"] = []
                for person in persons:
                    temp_event["persons"].append(person.text)
                #get the number of time slots this event/talk
                durations = event.find("duration").text.split(":")
                #calculate the amount of timeslots this event uses
                if time_slot_hours is not 0:
                    temp_event["time_slots"] = (int(durations[0]) * time_slot_hours) + (int(durations[1]) / time_slot_mins)
                else:
                    temp_event["time_slots"] = (int(durations[0]) * 60 + int(durations[1])) / time_slot_mins
                #if there is an URL, use it, it should be the link to the info
                event_url = event.find("url")
                if event_url is not None and hasattr(event_url, "text"):
                    temp_event["info_link"] = event_url.text
                else:
                    temp_event["info_link"] = None
                temp_event["start"] = event.find("start").text
                temp_room["events"].append(temp_event)
            temp_days[counter]["rooms"].append(temp_room)
        #increase the counter
        counter += 1
    #print(temp_days)
    context["days"] = temp_days
    return context
