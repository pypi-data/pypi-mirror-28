class InvalidJSON(Exception):
    def __str__(self):
        return "Can't Parse Invalid JSON Data"
    pass


class InvalidXML(Exception):
    def __str__(self):
        return "Can't Parse Invalid XML Data"


class InvalidYAML(Exception):
    def __str__(self):
        return "Can't Parse Invalid YAML Data"
