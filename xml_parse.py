import muzzle
import xml.etree.ElementTree as ET
import json
import os

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
with open("fedlex.xml") as f:
    xml_content = f.read().encode()


namespaces = {
    "akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
    "xsd": "http://www.w3.org/2001/XMLSchema",
}
xmlparser = muzzle.XMLParser(namespaces)
xml = xmlparser.parse(xml_content)


frbr_nr = xmlparser.find(xml, './/akn:FRBRnumber').attrib['value']
uri_base = xmlparser.find(xml, './/akn:FRBRuri').attrib['value']
print(f"URI: {uri_base}")

# Attribute Name
attribute_name = "eId"

# Extrahiere Elemente mit dem Attribut "eID"
elements = extract_elements_with_attribute(xml, attribute_name)


# Ausgabe der extrahierten Elemente
json_content = {}
for element in elements:
    for par in xmlparser.findall(element, './akn:content/akn:p'):
        uri = f"{uri_base}/{element.attrib['eId']}"
        print(f"{uri}")
        print(par.text)
        print('')
        json_content[uri] = {
            "text": par.text.strip(),
            "comment": "",
        }

json_path = os.path.join('fedlex', f"{frbr_nr}.json")
with open(json_path, "w") as fw:
    fw.write(json.dumps(json_content, indent=4))





#print(xml.find('./FRBRuri'))
