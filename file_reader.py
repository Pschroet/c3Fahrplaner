import requests
import util
import XML_parser

def read_xml_schedule(file_name):
    print("Getting XML schedule from file " + file_name)
    xml_content = util.readFileContentAsString(file_name)
    return XML_parser.parse_schedule(xml_content)


def read_json_schedule(file_name):
    print("Getting JSON schedule from file " + str(file_name))
    json_content = util.readFileContentAsString(file_name)
    return json_parser.parse_schedule(json_content)