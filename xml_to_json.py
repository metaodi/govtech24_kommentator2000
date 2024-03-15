import muzzle
import json
import os
from SPARQLWrapper import SPARQLWrapper, JSON
import argparse
import requests

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("--sr", help="SR-ID to save", type=str)
args = parser.parse_args()


def querySparql(query):
    sparql = SPARQLWrapper("https://fedlex.data.admin.ch/sparqlendpoint")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()
    return results['results']['bindings']

def load_xml_url(sr_id):
    query = """
    PREFIX jolux: <http://data.legilux.public.lu/resource/ontology/jolux#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    select distinct ?title (str(?dateDocumentNode) as ?dateDocument) ?fileUri {
    values (?srString) {("%SR_ID%")}

    ?consoAbstract a jolux:ConsolidationAbstract .
    ?consoAbstract jolux:classifiedByTaxonomyEntry/skos:notation ?rsNotation .
    filter(str(?rsNotation) = ?srString)
    ?consoAbstract jolux:dateDocument ?dateDocumentNode .
    ?consoAbstract jolux:isRealizedBy ?consoAbstractExpression .
    ?consoAbstractExpression jolux:language <http://publications.europa.eu/resource/authority/language/DEU> .
    ?consoAbstractExpression jolux:title ?title .
    optional {?consoAbstractExpression jolux:titleShort ?abbreviation . }
    optional {?consoAbstractExpression jolux:titleAlternative ?titleAlternative . }

    ?conso a jolux:Consolidation .
    ?conso jolux:isMemberOf ?consoAbstract .
    ?conso jolux:dateApplicability ?dateApplicabilityNode .

    ?conso jolux:isRealizedBy ?consoExpression .
    ?consoExpression jolux:isEmbodiedBy ?manifestation .
    ?consoExpression jolux:language <http://publications.europa.eu/resource/authority/language/DEU> .
    ?manifestation jolux:isExemplifiedBy ?fileUri .
    ?manifestation jolux:userFormat/skos:notation "xml"^^<https://fedlex.data.admin.ch/vocabulary/notation-type/uri-suffix>.
    }
    order by desc(?fileUri)
    """.replace('%SR_ID%', sr_id)
    results = querySparql(query)
    xml_url = results[0]['fileUri']['value']
    return xml_url


xml_url = load_xml_url(args.sr)
print(f"Load XML form URL {xml_url}...")

session = requests.Session()
r = session.get(xml_url)
xml_content = r.text

# parse xml
namespaces = {
    "akn": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xml": "http://www.w3.org/XML/1998/namespace",
}
xmlparser = muzzle.XMLParser(namespaces)
xml = xmlparser.parse(xml_content)

frbr_nr = xmlparser.find(xml, './/akn:FRBRnumber').attrib['value']
uri_base = xmlparser.find(xml, './/akn:FRBRuri').attrib['value']
title = xmlparser.find(xml, ".//akn:FRBRname[@xml:lang='de']").attrib['value']
short = xmlparser.find(xml, ".//akn:FRBRname[@xml:lang='de']").attrib['shortForm']
print(f"URI: {uri_base}")

# Ausgabe der extrahierten Elemente
lines = {}
for article in xmlparser.findall(xml, './/akn:article'):
    article_num = xmlparser.find(article, './akn:num/akn:b').text
    for par in xmlparser.findall(article, './akn:paragraph'):
        par_num = xmlparser.find(par, './akn:num').text or '' 
        par_text = xmlparser.find(par, './akn:content/akn:p').text or ''
        uri = f"{uri_base}/{par.attrib['eId']}"
        print(f"{uri}")
        print('')
        lines[uri] = {
            "article_num": article_num.strip(),
            "par_num": par_num.strip(),
            "text": par_text.strip(),
            "comment": "",
        }

content = {
    "_metadata": {
        "title": title,
        "short": short,
        "frbr_nr": frbr_nr,
        "uri": uri_base,
    },
    "lines": lines
}

json_path = os.path.join('fedlex', f"{frbr_nr}.json")
with open(json_path, "w") as fw:
    fw.write(json.dumps(content, indent=4))





#print(xml.find('./FRBRuri'))
