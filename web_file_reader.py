import json_parser
import requests
import XML_parser

def read_xml_schedule(url):
    print("Getting XML schedule from " + str(url))
    xml_content = requests.get(url)
    #print(xml_content.headers)
    return XML_parser.parse_schedule(xml_content.text.encode('utf8'))

def read_json_schedule(url):
    print("Getting JSON schedule from " + str(url))
    json_content = requests.get(url)
    #print(json_content.headers)
    return json_parser.parse_schedule(json_content.content)