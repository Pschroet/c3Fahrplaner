from HTMLParser import HTMLParser
import datetime
import util

class fahrplan_writer(HTMLParser):
    context = {}
    fahrplan = ""
    expire_date = datetime.date(2020, 12, 31)
    
    def fahrplan_writer(self):
        self.context = {}
        self.fahrplan = ""
        
    def set_context(self, context):
        self.context = context
        self.expire_date = datetime.datetime.date(datetime.datetime.strptime(context["end"], "%Y-%m-%d") + datetime.timedelta(days=1))
    
    def get_result(self):
        return self.fahrplan
    
    def handle_starttag(self, tag, attrs):
        #print "Encountered a start tag: " + tag
        #add the title
        if tag == "title":
            self.fahrplan += "<" + tag
            for attr in attrs:
                self.fahrplan += " " + attr[0] + "='" + attr[1] + "'"
            self.fahrplan += ">" + self.context["title"]
        #add the information about the events at the days
        elif tag == "div":
            day_events = "<div class='day'>"
            for day in self.context["days"]:
                day_events += "<h3>" + day["date"]  + "</h3>\n"
                day_events += "<table id='" + day["date"] + "'>\n<thead><tr>\n<th class='something'>Room</th>\n"
                #add the time slots
                for time_slot in day["time_slots"]:
                    day_events += "<th class='something'>" + time_slot + "</th>\n"
                #add the room for this day
                day_events += "</tr></thead>\n<tbody>\n"
                for room in day["rooms"]:
                    #print room
                    day_events += "<tr>"
                    day_events += "<td class='something'>" + room["name"] + "</td>"
                    #add the events for this room
                    last_event = 0
                    colspan = 0
                    events = room["events"]
                    #look for the starting time for each event in the time slots
                    for time_slot in day["time_slots"]:
                        #if there are no more events stop for this room
                        if len(events) is last_event:
                            break
                        #print time_slot + " == " + events[last_event]["start"]
                        #if not, go on
                        if time_slot == events[last_event]["start"] or "0" + time_slot == events[last_event]["start"]:
                            day_events += "<td class='something' colspan='" + str(events[last_event]["time_slots"]) + "' onclick='toggleClick(this, false);' " + "id='" + events[last_event]["id"] + "' title='unselected'>" + events[last_event]["title"] + " (<a href='https://fahrplan.events.ccc.de/congress/" + self.context["year"] + "/Fahrplan/events/" + events[last_event]["id"] + ".html' onmouseover='onLink=true;' onmouseout='onLink=false;' target='_blank'>--></a>)" + "</td>\n"
                            #calculate the columns used, subtract the current table field
                            colspan = events[last_event]["time_slots"] - 1
                            #print "-> " + str(events[last_event])
                            #print "-> " + str(colspan)
                            last_event += 1
                        elif last_event is 0:
                            day_events += "<td class='nothing'></td>"
                        elif colspan is 0:
                            day_events += "<td class='nothing'></td>"
                        else:
                            colspan -= 1
                            #print "--> " + str(colspan)
                    day_events += "</tr>"
                day_events += "</table>"
            self.fahrplan += day_events
        elif tag == "script":
            #add the expire date and the script
            self.fahrplan += "<script>\nvar dayAfter = '" + self.expire_date.strftime("%a, %d %b %Y 23:59:00 UTC") + "';\n" + util.readFileContentAsString("script.js")
        #if no 'special' tag is found, just copy it
        else:
            self.fahrplan += "<" + tag
            #print attrs
            for attr in attrs:
                self.fahrplan += " " + attr[0] + "='" + attr[1] + "'"
            self.fahrplan += ">"

    def handle_endtag(self, tag):
        #print "Encountered an end tag :" + tag
        self.fahrplan += "</" + tag + ">"

    def handle_data(self, data):
        #print "Encountered some data"
        self.fahrplan += data

    def handle_decl(self, decl):
        self.fahrplan += "<!" + decl + ">"

    def handle_comment(self, data):
        self.fahrplan += "<!-- " + data + " -->"
