import json
from urllib.parse import urlencode
import urllib3

server = 'http://kbox.kaist.ac.kr:5820/myDB/'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded, application/sparql-query, text/turtle',
    'Accept': 'text/turtle, application/rdf+xml, application/n-triples, application/trig, application/n-quads, '
    'text/n3, application/trix, application/ld+json, '  # application/sparql-results+xml, '
    'application/sparql-results+json, application/x-binary-rdf-results-table, text/boolean, text/csv, '
    'text/tsv, text/tab-separated-values '
}


def error_handler(inputjson):
	indic = inputjson
	cTopics = indic["cTopics"]
	intent = indic["intent"]
	concept = indic["concept"]


	outdic = dict()

	outputlist = []
	if intent == "Agree":
		outdic["inContext"] = True
		outdic["label"] = None
		outdic["uri"] = None
		outjson = outdic
		outputlist.append(outjson)

	elif intent == "Disagree":
		outdic["inContext"] = False
		outdic["label"] = None
		outdic["uri"] = None
		outjson = outdic
		outputlist.append(outjson)
	else:
		if isinstance(cTopics, str):
			cTopics = [cTopics]
		for cTopic in cTopics:
			entity_list = kb_checker(cTopic)
			if len(entity_list) > 0:
				uri = entity_list[0]
				if len(type_checker(uri, concept)) > 0:
					outdic["inContext"] = True
					outdic["label"] = cTopic
					outdic["uri"] = uri
#					print("type checker")
				elif concept == "dbo:Genre":
					if len(genre_checker(uri)) > 0:
						outdic["inContext"] = True
						outdic["label"] = cTopic
						outdic["uri"] = uri
#					print("genre checker")
				else:
					outdic["inContext"] = "Uncertain"
					outdic["label"] = cTopic
					outdic["uri"] = None
			else:
				outdic["inContext"] = "Uncertain"
				outdic["label"] = cTopic
				outdic["uri"] = None

			outjson = outdic
			outputlist.append(outjson)

	return outputlist



def kb_checker(cTopics):
	#print(cTopics)
	query = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> SELECT ?entity ?label " \
			"WHERE { ?entity rdfs:label ?label . filter(?label='" + cTopics + "'@ko) . } "
	values = urlencode({'query': query})
	http = urllib3.PoolManager()

	url = server + 'query?' + values
	r = http.request('GET', url, headers=headers)
	label = ''
	request = json.loads(r.data.decode('UTF-8'))
	result_list = request['results']['bindings']
	output_list = []
	
	for result in result_list:
		uri = result["entity"]["value"]
		if "ko.dbpedia.org/resource" in uri and "틀" not in uri and "분류" not in uri:
			output_list.append(uri)

	return output_list

def type_checker(uri, concept):
	query = "PREFIX dbo: <http://dbpedia.org/ontology/> " \
			"SELECT ( <" + uri + "> as ?entity) ?concept " \
			"WHERE { <"+uri+"> rdf:type ?concept . filter(?concept="+concept+")} "
	#print(query)

	values = urlencode({'query': query})
	http = urllib3.PoolManager()

	url = server + 'query?' + values
	r = http.request('GET', url, headers=headers)
	label = ''
	request = json.loads(r.data.decode('UTF-8'))
#	print(request)
	result_list = request['results']['bindings']


	return result_list

#genre만을 위한 임시 함수
def genre_checker(uri):
	query = "PREFIX dbo: <http://dbpedia.org/ontology/> " \
			"SELECT ?s ( <" + uri + "> as ?o) " \
			"WHERE { ?s dbo:genre <"+uri+"> . } "
	#print(query)

	values = urlencode({'query': query})
	http = urllib3.PoolManager()

	url = server + 'query?' + values
	r = http.request('GET', url, headers=headers)
	label = ''
	request = json.loads(r.data.decode('UTF-8'))
	#print(request)
	result_list = request['results']['bindings']

	return result_list

if __name__ == "__main__":

	sample0 = json.dumps({"intent":"Answer", "cTopics":"재즈", "concept":"dbo:Genre"})
	sample1 = json.dumps({"intent":"Agree", "cTopics":None, "concept":"dbo:Genre"})
	sample2 = json.dumps({"intent":"Disagree", "cTopics":None, "concept":"dbo:Genre"})
	sample3 = json.dumps({"intent":"Answer", "cTopics":"뉴잭스윙이아닐수도있습니다", "concept":"dbo:Genre"})
	sample4 = json.dumps({"intent":"Answer", "cTopics":"클래식", "concept":"dbo:Genre"})
	sample5 = json.dumps({"intent":"Answer", "cTopics":"팝", "concept":"dbo:Genre"})
	sample6 = json.dumps({"intent":"Answer", "cTopics":"록", "concept":"dbo:Genre"})
	sample7 = json.dumps({"intent":"Answer", "cTopics":"힙합", "concept":"dbo:Genre"})
	
	print(error_handler(sample0))
	print(error_handler(sample1))
	print(error_handler(sample2))
	print(error_handler(sample3))
	print(error_handler(sample4))
	print(error_handler(sample5))
	print(error_handler(sample6))
	print(error_handler(sample7))
	
	#sampleuri = "http://ko.dbpedia.org/resource/\\uc7ac\\uc988"
	#sampleconcept = "dbo:Genre"
	#type_checker(sampleuri, sampleconcept)
	#genre_checker(sampleuri)



