import json
import yaml
from jyxml.exceptions import InvalidYAML, InvalidJSON


class Json2Yaml:
    def __init__(self):
        pass

    def parseJSON(self, rawData, indentBy=0, beautify=False):
        global data
        try:
            yam = yaml.load(rawData)
            if beautify:
                data = json.dumps(yam, indent=indentBy)
            else:
                data = json.dumps(yam)
            pass
        except (yaml.MarkedYAMLError, yaml.YAMLError):
            raise InvalidYAML
        return data

    def parseYAML(self, rawData, beautify=False):
        global data
        try:
            data = json.loads(rawData)
            if beautify:
                data = yaml.dump(data, default_flow_style=False)
                pass
            else:
                data = yaml.dump(data, default_flow_style=True)
            pass
        except json.JSONDecodeError:
            raise InvalidJSON
        return data
    pass

