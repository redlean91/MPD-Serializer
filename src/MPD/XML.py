# https://github.com/redlean91/MPD-Serializer
# MPD Serializer for Just Dance
# Serializer for Media Presentation Description files to Just Dance-like format

import json
import xml.etree.ElementTree as ET

class XML:
    def __init__(self, xml_file):
        self.XMLFile = xml_file
        self.XMLString = open(xml_file).read()

    def Cook(self):
        def parse_element(element):
            parsed = {}
            # Add attributes
            if element.attrib:
                parsed["@attributes"] = element.attrib
            # Add children or text
            for child in element:
                child_parsed = parse_element(child)
                if child.tag not in parsed:
                    parsed[child.tag] = child_parsed
                else:
                    # handle multiple children with same tag
                    if not isinstance(parsed[child.tag], list):
                        parsed[child.tag] = [parsed[child.tag]]
                    parsed[child.tag].append(child_parsed)
            if element.text and element.text.strip():
                text = element.text.strip()
                if parsed:
                    parsed["#text"] = text
                else:
                    parsed = text
            return parsed

        root = ET.fromstring(self.XMLString)
        return {root.tag: parse_element(root)}