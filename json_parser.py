import json

def parse_schedule(json_content):
    print("Parsing schedule")
    #print(json_content)
    conference_json = json.loads(json_content)["schedule"]["conference"]
    context = {}
    context["title"] = conference_json["title"]
    context["acronym"] = conference_json["acronym"]
    context["year"] = conference_json["start"].split("-"[0])
    context["timeslot"] = conference_json["timeslot_duration"]
    time_slot_mins = int(context["timeslot"].split(":")[1])
    time_slot_hours = int(context["timeslot"].split(":")[0])
    #get the year, so it can be used in the URLs
    context["year"] = conference_json["start"].split("-")[0]
    #get the last day, to determine the expiration date of the cookie
    context["end"] = conference_json["end"]
    #get the days
    #define the temporary variables for collect all information
    temp_days = []
    counter = 0
    for day in conference_json["days"]:
        #print("Events for " + day["date"] + ":")
        #check if the the event is spread over more than one day, e.g. from 10am to 4am the next day
        start_day = int(day["day_start"].split("T")[0].split("-")[2])
        end_day = int(day["day_end"].split("T")[0].split("-")[2])
        diff_days = 0
        if start_day < end_day:
            diff_days = end_day - start_day
        start_time = day["day_start"].split("T")[1].split("+")[0].split(":")
        end_time = day["day_end"].split("T")[1].split("+")[0].split(":")
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
        temp_days.append({"date":day["date"], "rooms":[], "start":start_time, "end":end_time, "time_slots": time_slots, "total_time_slots":total_time_slots})
        #get the rooms
        rooms = day["rooms"]
        for room in rooms:
            #print(room)
            temp_room = {}
            temp_room["name"] = room
            temp_room["events"] = []
            #get the events for this room
            for event in rooms[room]:
                temp_event = {}
                #get the basic information about the event
                temp_event["title"] = str(event["title"])
                #print(temp_event["title"])
                temp_event["id"] = event["id"]
                persons = event["persons"]
                temp_event["persons"] = []
                for person in persons:
                    temp_event["persons"].append(person)
                #get the number of time slots this event/talk
                durations = event["duration"].split(":")
                #calculate the amount of timeslots this event uses
                if time_slot_hours != 0:
                    temp_event["time_slots"] = (int(durations[0]) * time_slot_hours) + (int(durations[1]) / time_slot_mins)
                else:
                    temp_event["time_slots"] = (int(durations[0]) * 60 + int(durations[1])) / time_slot_mins
                #if there is an URL, use it, it should be the link to the info
                if "url" in event:
                    temp_event["info_link"] = event["url"]
                else:
                    temp_event["info_link"] = None
                temp_event["start"] = event["start"]
                temp_room["events"].append(temp_event)
            temp_days[counter]["rooms"].append(temp_room)
        #increase the counter
        counter += 1
    #print(temp_days)
    context["days"] = temp_days
    return context