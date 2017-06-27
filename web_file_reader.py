import requests
import XML_parser

def read_schedule(url):
    print "Getting schedule from " + url
    xml_content = requests.get(url)
    #print xml_content.headers
    return XML_parser.parse_schedule(xml_content.text.encode('utf8'))