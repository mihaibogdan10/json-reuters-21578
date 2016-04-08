from BeautifulSoup import BeautifulStoneSoup
import os
import json
from os.path import join, isfile, dirname

sgmDataDirPath = join(dirname(__file__), 'sgm-data')
jsonDataDirPath = join(dirname(__file__), 'json-data')


def xml_node_to_json(node):
    textNode = node.find('text')

    return {
        'attrs': {
            'topics': node.get('topics'),
            'lewissplit': node.get('lewissplit'),
            'cgisplit': node.get('cgisplit'),
            'oldid': node.get('oldid'),
            'newid': node.get('newid'),
        },

        'date': node.find('date').text,
        'unknown': node.find('unknown').text if node.find('unknown') else '',
        'title': textNode.find('title').text if textNode.find('title') else '',
        'dateline': textNode.find('dateline').text if textNode.find('dateline') else '',
        'body': textNode.find('body').text if textNode.find('body') else '',

        'topics': [elem.text for elem in node.find('topics').findAll('d')],
        'places': [elem.text for elem in node.find('places').findAll('d')],
        'orgs': [elem.text for elem in node.find('orgs').findAll('d')],
        'exchanges': [elem.text for elem in node.find('exchanges').findAll('d')],
        'companies': [elem.text for elem in node.find('companies').findAll('d')]
    }


files = [f for f in os.listdir(sgmDataDirPath) if isfile(join(sgmDataDirPath, f))]

for sgmName in files:
    jsonName = sgmName.replace('.sgm', '.json')
    with open(join(sgmDataDirPath, sgmName)) as rf:
        with open(join(jsonDataDirPath, jsonName), mode='w') as wf:
            content = BeautifulStoneSoup(rf)

            jsonDocs = []
            for entry in content.findAll('reuters'):
                data = xml_node_to_json(entry)
                jsonDocs.append(data)

            json.dump(jsonDocs, wf, indent=4, sort_keys=True)
            print "Done with", sgmName