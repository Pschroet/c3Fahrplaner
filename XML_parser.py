import defusedxml.ElementTree
import requests

def read_schedule(url):
    print "Parsing schedule " + url
    ontology_content = requests.get(url)
    #print ontology_content
    #print ontology_content.headers
    tree = defusedxml.ElementTree.fromstring(ontology_content.text.encode('utf8'), forbid_entities=False)
    if hasattr(tree, "getroot") and isfunction(tree.getroot):
        root = tree.getroot()
    else:
        root = tree
    #print root
    context = {}
    #get the info about the event first
    con_info = root.find("conference")
    #print con_info
    context["title"] = con_info.find("title").text
    context["timeslot"] = con_info.find("timeslot_duration").text
    time_slot_mins = int(context["timeslot"].split(":")[1])
    time_slot_hours = 60 / int(context["timeslot"].split(":")[1])
    #get the days
    days = root.findall("day")
    #define the temporary variables for collect all information
    temp_days = []
    counter = 0
    for day in days:
        #print "Events for " + day.attrib["date"] + ":"
        #check if the the event is spread over more than one day, e.g. from 10am to 4am the next day
        start_day = int(day.attrib["start"].split("T")[0].split("-")[2])
        end_day = int(day.attrib["end"].split("T")[0].split("-")[2])
        diff_days = 0
        if start_day < end_day:
            diff_days = end_day - start_day
        start_times = day.attrib["start"].split("T")[1].split("+")[0].split(":")
        end_times = day.attrib["end"].split("T")[1].split("+")[0].split(":")
        total_time_hours = (diff_days*24) + int(end_times[0]) - int(start_times[1])
        total_time_mins = (total_time_hours*60) + int(end_times[1]) - int(start_times[1])
        total_time_slots = total_time_mins/time_slot_mins
        #put all information into a dictionary to use later
        temp_days.append({"date":day.attrib["date"], "rooms":[], "start":start_times, "end":end_times, "total_time_slots":total_time_slots})
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
                persons = event.find("persons").findall("person")
                temp_event["persons"] = []
                for person in persons:
                    temp_event["persons"].append(person.text)
                #get the number of time slots this event/talk
                durations = event.find("duration").text.split(":")
                #calculate the amount of timeslots this event uses
                temp_event["time_slots"] = (int(durations[0]) * time_slot_hours) + (int(durations[1]) / time_slot_mins)
                temp_room["events"].append(temp_event)
            temp_days[counter]["rooms"].append(temp_room)
        #increase the counter
        counter += 1
    #print temp_days
    context["days"] = temp_days
    return context