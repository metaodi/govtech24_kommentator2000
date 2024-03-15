import muzzle
import xml.etree.ElementTree as ET
import json
import os

# open xml
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

# Ausgabe der extrahierten Elemente
json_content = {}
for article in xmlparser.findall(xml, './/akn:article'):
    article_num = xmlparser.find(article, './akn:num/akn:b').text
    for par in xmlparser.findall(article, './akn:paragraph'):
        par_num = xmlparser.find(par, './akn:num').text or '' 
        par_text = xmlparser.find(par, './akn:content/akn:p').text or ''
        uri = f"{uri_base}/{par.attrib['eId']}"
        print(f"{uri}")
        print('')
        json_content[uri] = {
            "article_num": article_num.strip(),
            "par_num": par_num.strip(),
            "text": par_text.strip(),
            "comment": "",
        }

json_path = os.path.join('fedlex', f"{frbr_nr}.json")
with open(json_path, "w") as fw:
    fw.write(json.dumps(json_content, indent=4))





#print(xml.find('./FRBRuri'))
