import muzzle
import xml.etree.ElementTree as ET
import json

def extract_elements_with_attribute(root, attribute_name):
    # Initialize list to store elements
    elements_with_attribute = []
    
    # Traverse XML and extract elements with the specified attribute
    def traverse(element):
        if attribute_name in element.attrib:
            elements_with_attribute.append(element)
        for child in element:
            traverse(child)
    
    traverse(root)
    
    return elements_with_attribute

# Beispiel XML
xml_string = """
<root>
    <element1 eID="1">
        <subelement1>eID 1</subelement1>
    </element1>
    <element2>
        <subelement2>eID 2</subelement2>
    </element2>
    <element3 eID="3">
        <subelement3>eID 3</subelement3>
    </element3>
</root>
"""

with open("fedlex.xml") as f:
    xml_content = f.read().encode()


namespaces = {
    "akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
    "xsd": "http://www.w3.org/2001/XMLSchema",
}
xmlparser = muzzle.XMLParser(namespaces)
xml = xmlparser.parse(xml_content)


uri_base = xmlparser.find(xml, './/akn:FRBRuri')
uri_value = uri_base.attrib['value']
print(f"URI: {uri_value}")

# Attribute Name
attribute_name = "eId"

# Extrahiere Elemente mit dem Attribut "eID"
elements = extract_elements_with_attribute(xml, attribute_name)


# Ausgabe der extrahierten Elemente
json_content = {}
for element in elements:
    for par in xmlparser.findall(element, './akn:content/akn:p'):
        content_id = f"{uri_value}/{element.attrib['eId']}"
        print(f"{content_id}")
        print(par.text)
        print('')
        json_content[content_id] = par.text

with open("content.json", "w") as fw:
    fw.write(json.dumps(json_content, indent=4))





#print(xml.find('./FRBRuri'))
