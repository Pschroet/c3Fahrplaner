import fahrplan_writer
import util
import file_reader
#import web_file_reader

if __name__ == '__main__':
    #get the schedule from a file
    file_name = "schedule.xml"
    context = file_reader.read_schedule(file_name)
    #get the schedule from a URL
    #url = "https://fahrplan.events.ccc.de/congress/2016/Fahrplan/schedule.xml"
    #context = web_file_reader.read_schedule(url)
    #print context
    tmpl = util.readFileContentAsString('fahrplan_template.html')
    parser = fahrplan_writer.fahrplan_writer()
    parser.set_context(context)
    parser.feed(tmpl)
    destination = "fahrplan.html"
    print "Writing to '" + destination + "'"
    util.write2File(destination, parser.get_result(), "w")