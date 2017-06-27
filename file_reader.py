import requests
import util
import XML_parser

def read_schedule(file_name):
    print "Getting schedule from file " + file_name
    xml_content = util.readFileContentAsString(file_name)
    return XML_parser.parse_schedule(xml_content)