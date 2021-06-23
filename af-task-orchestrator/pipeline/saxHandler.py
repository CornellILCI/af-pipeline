import xml.etree.ElementTree
from xml.sax.handler import ContentHandler

class SaxHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        self._charBuffer = []
        self._result = []

    def _getCharacterData(self):
        data = ''.join(self._charBuffer).strip()
        self._charBuffer = []
        return data.strip() #remove strip() if whitespace is important

    def parse(self, f):
        xml.sax.parse(f, self)
        return self._result

    def characters(self, data):
        self._charBuffer.append(data)

    def startElement(self, name, attrs):
        if name == 'ASReport': self._result.append({})

    def endElement(self, name):
        if not name == 'ASReport': self._result[-1][name] = self._getCharacterData()


# jobs = MyHandler().parse("job-file.xml")
jobs = SaxHandler().parse("/home/vince/dev/work/rando/xmlPedro/67ac5d6f-5cdc-45fd-a2fa-2bc17a2c58bg_SA_1001.xml") #a list of all jobs
print(jobs)
