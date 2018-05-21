import lxml.etree as etree

raw = etree.parse("game.xsd")
schema_root = raw.getroot()
# This will actually check that the schema is sound:
schema = etree.XMLSchema(schema_root)
parser = etree.XMLParser(schema=schema)
tree = etree.parse('example1.xml', parser)
