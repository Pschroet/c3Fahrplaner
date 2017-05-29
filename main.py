import fahrplan_writer
import util
import XML_parser

if __name__ == '__main__':
    url = "https://fahrplan.events.ccc.de/congress/2016/Fahrplan/schedule.xml"
    #speaker info: https://fahrplan.events.ccc.de/congress/2016/Fahrplan/speakers.json
    print "Getting schedule from " + url
    context = XML_parser.read_schedule(url)
    #print context
    tmpl = util.readFileContentAsString('fahrplan_template.html')
    parser = fahrplan_writer.fahrplan_writer()
    parser.set_context(context)
    parser.feed(tmpl)
    destination = "fahrplan.html"
    print "Writing to '" + destination + "'"
    util.write2File(destination, parser.get_result(), "w")