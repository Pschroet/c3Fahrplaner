import fahrplan_writer
import util
import file_reader
import web_file_reader

if __name__ == '__main__':
    #get the schedule from a file
    #file_name = "33c3-schedule.xml"
    #file_name = "PrivacyWeek-schedule.xml"
    #file_name = "35c3-schedule.xml"
    #context = file_reader.read_schedule(file_name)
    #get the schedule from a URL
    #url = "https://fahrplan.events.ccc.de/congress/2016/Fahrplan/schedule.xml"
    #url = "https://events.ccc.de/congress/2017/Fahrplan/schedule.xml"
    #url = "https://fahrplan.events.ccc.de/camp/2019/Fahrplan/schedule.xml"
    #url = "https://datenspuren.de/2019/fahrplan/schedule.xml"
    #url = "https://fahrplan.events.ccc.de/camp/2019/Fahrplan/schedule.xml"
    #url = "https://fahrplan.events.ccc.de/congress/2019/Fahrplan/schedule.xml"
    #url = "https://datenspuren.de/2020/fahrplan/schedule.xml"
    #url = "https://data.c3voc.de/rC3/everything.schedule.xml"
    #context = web_file_reader.read_xml_schedule(url)
    url = "http://data.c3voc.de/rC3/everything.schedule.json"
    context = web_file_reader.read_json_schedule(url)
    #print(context)
    tmpl = util.readFileContentAsString('fahrplan_template.html')
    parser = fahrplan_writer.fahrplan_writer()
    parser.set_context(context)
    parser.feed(tmpl)
    destination = "fahrplan.html"
    print("Writing to '" + destination + "'")
    util.write2File(destination, parser.get_result(), "w+")
