import os
import XML_parser
import util
from genshi.template import MarkupTemplate
from genshi.template import TemplateLoader

if __name__ == '__main__':
    url = "https://fahrplan.events.ccc.de/congress/2016/Fahrplan/schedule.xml"
    #speaker info: https://fahrplan.events.ccc.de/congress/2016/Fahrplan/speakers.json
    print "Getting schedule from " + url
    context = XML_parser.read_schedule(url)
    print context
    loader = TemplateLoader(".")
    tmpl = loader.load('fahrplan_template.html')
    stream = tmpl.generate(context=context)
    util.write2File("fahrplan.html", stream.render('html', doctype='html'), "w")