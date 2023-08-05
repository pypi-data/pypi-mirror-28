import json
import dicttoxml
from xml.dom.minidom import parseString
from jyxml.exceptions import InvalidJSON, InvalidXML
import xmltodict
from xml.parsers.expat import ExpatError


class Json2Xml:
    def __init__(self):
        pass

    def parseXML(self, rawData, root=False, root_name="root", beautify=False, diffIds=False):
        global data
        try:
            data = json.loads(rawData)
            data = dicttoxml.dicttoxml(data, root=root, custom_root=root_name, ids=diffIds).decode()
            if beautify:
                dom = parseString(data)
                data = dom.toprettyxml()
            pass
        except json.JSONDecodeError:
            raise InvalidJSON
        return data

    def parseJSON(self, rawData, indentBy=0, beautify=False):
        global data
        try:
            data = xmltodict.parse(rawData)
            if beautify:
                data = json.dumps(data, indent=indentBy)
            else:
                data = json.dumps(data)
            pass
        except ExpatError:
            raise InvalidXML
            pass
        return data
    pass

