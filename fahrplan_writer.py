from HTMLParser import HTMLParser
import datetime
import re
import util

class fahrplan_writer(HTMLParser):
    context = {}
    fahrplan = ""
    expire_date = datetime.date(2020, 12, 31)
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.context = {}
        self.fahrplan = ""
        self.event_types = {}
        self.event_types["cccongress"] = {"title":"Chaos Communication Congress",
                                          "function_name":"cccongress"}
        self.event_types["cccongress"]["regex"] = re.compile(".*" + self.event_types["cccongress"]["title"] + ".*", re.IGNORECASE)
        self.event_types["cccamp"] = {"title":"Chaos Communication Camp",
                                      "function_name":"cccamp"}
        self.event_types["cccamp"]["regex"] = re.compile(".*" + self.event_types["cccamp"]["title"] + ".*", re.IGNORECASE)
        self.event_types["dspuren"] = {"title":"Datenspuren",
                                       "function_name":"dspuren"}
        self.event_types["dspuren"]["regex"] = re.compile(".*" + self.event_types["dspuren"]["title"] + ".*", re.IGNORECASE)
        self.event_function_name = "other_event"

    def set_context(self, context):
        self.context = context
        self.expire_date = datetime.datetime.date(datetime.datetime.strptime(context["end"], "%Y-%m-%d") + datetime.timedelta(days=365))

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
            for event_type in self.event_types:
                #print(str(event_type))
                #print(str(self.event_types[event_type]))
                #print(str(self.context["title"]))
                #print(self.event_types[event_type]["regex"].match(self.context["title"]))
                if self.event_types[event_type]["regex"].match(self.context["title"]):
                    self.event_function_name = self.event_types[event_type]["function_name"]
        elif tag == "h1":
            self.fahrplan += "<h1>" + self.context["title"]
        elif tag == "p":
            if self.event_function_name is not None:
                self.fahrplan += getattr(self, self.event_function_name)(tag)
        #add the information about the events at the days
        elif tag == "div":
            #print(str(self.event_function_name))
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
                            if self.event_function_name is not None:
                                day_events += getattr(self, self.event_function_name)(tag, events[last_event]["time_slots"], events[last_event]["id"], events[last_event]["title"])
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

    def other_event(self, tag, event_time_slots="", event_id="", event_title=""):
        if tag == "p":
            return ""
        elif tag == "div":
            event_code = "<td class='something' colspan='" + str(event_time_slots) + "'"
            event_code += " onclick='toggleClick(this, false);'"
            event_code += " id='" + event_id + "'"
            event_code += " title='unselected'>"
            event_code += event_title
            event_code += "</td>\n"
            return event_code

    def cccongress(self, tag, event_time_slots="", event_id="", event_title=""):
        if tag == "p":
            useful_links = "<p><a href='https://events.ccc.de/tag/" + self.context["acronym"]
            useful_links += "'>Event blog</a></p>"
            useful_links += "<p><a href='https://events.ccc.de/congress/" +  self.context["year"]
            useful_links += "/wiki/'>Wiki</a>"
            return useful_links
        elif tag == "div":
            event_code = "<td class='something' colspan='" + str(event_time_slots) + "'"
            event_code += " onclick='toggleClick(this, false);'"
            event_code += " id='" +  event_id + "'"
            event_code += " title='unselected'>"
            event_code += "<a href='https://media.ccc.de/tags/" + event_id + "'>"
            event_code += event_title
            event_code += "</a>"
            event_code += " (<a href='https://fahrplan.events.ccc.de/congress/" + self.context["year"]
            event_code += "/Fahrplan/events/" +  event_id + ".html'"
            event_code += " onmouseover='onLink=true;' onmouseout='onLink=false;' target='_blank'>--></a>)" + "</td>\n"
            return event_code

    def cccamp(self, tag, event_time_slots="", event_id="", event_title=""):
        if tag == "p":
            useful_links = "<p><a href='https://events.ccc.de/category/camp/camp-"
            useful_links += self.context["year"]
            useful_links += "'>Event blog</a></p>"
            useful_links += "<p><a href='https://events.ccc.de/camp/"
            useful_links += self.context["year"]
            useful_links += "/wiki/'>Wiki</a>"
            return useful_links
        elif tag == "div":
            event_code = "<td class='something' colspan='" + str(event_time_slots) + "'"
            event_code += " onclick='toggleClick(this, false);'"
            event_code += " id='" + event_id + "'"
            event_code += " title='unselected'><a href='https://media.ccc.de/tags/" + event_id + "'>"
            event_code += event_title
            event_code += "</a>"
            event_code += " (<a href='https://fahrplan.events.ccc.de/camp/" + self.context["year"]
            event_code += "/Fahrplan/events/" + event_id + ".html'"
            event_code += " onmouseover='onLink=true;' onmouseout='onLink=false;' target='_blank'>--></a>)" + "</td>\n"
            return event_code

    def dspuren(self, tag, event_time_slots="", event_id="", event_title=""):
        if tag == "p":
            useful_links = "<p><a href='https://events.ccc.de/tag/datenspuren'>Event blog</a></p>"
            useful_links += "<p><a href='https://wiki.c3d2.de/Datenspuren/" + self.context["year"] + "'>Wiki</a>"
            return useful_links
        elif tag == "div":
            event_code = "<td class='something' colspan='" + str(event_time_slots) + "'"
            event_code += " onclick='toggleClick(this, false);'"
            event_code += " id='" + event_id + "'"
            event_code += " title='unselected'><a href='https://media.ccc.de/tags/" + event_id + "'>"
            event_code += event_title
            event_code += "</a>"
            event_code += " (<a href='https://datenspuren.de/" + self.context["year"]
            event_code += "/fahrplan/events/" + event_id + ".html'"
            event_code += " onmouseover='onLink=true;' onmouseout='onLink=false;' target='_blank'>--></a>)" + "</td>\n"
            return event_code