import json
from urllib.parse import urlencode
import urllib3
import codecs

server = 'http://kbox.kaist.ac.kr:5820/myDB/'
headers = {
    'Content-Type': 'application/x-www-form-urlencoded, application/sparql-query, text/turtle',
    'Accept': 'text/turtle, application/rdf+xml, application/n-triples, application/trig, application/n-quads, '
    'text/n3, application/trix, application/ld+json, '  # application/sparql-results+xml, '
    'application/sparql-results+json, application/x-binary-rdf-results-table, text/boolean, text/csv, '
    'text/tsv, text/tab-separated-values '
}

def KB_incomplete(inputjson):
	indic = inputjson
	dialogStatus = indic["dialogStatus"]
	pTopic = indic["pTopic"]
	area = indic["area"]

	try:
		f = open("data/area_questions/" + area, "r")
	except:
		print("No question list defined for " + area + ".")
		return None

	qlist = []
	for line in f.readlines():
		qdic = dict()
		line = line.strip().split("\t")
		qdic["concept"] = line[0]
		qdic["property"] = line[1]
		qdic["reverse"] = line[2]
		qdic["multipleTriples"] = line[3]
		qdic["questionType"] = line[4]

		qlist.append(qdic)

	print(qlist)

	outputlist = []
	for q in qlist:
		if check_question_in_KB(pTopic, q):
			pass
		else:
			qjson = q
			outputlist.append(qjson)

	return outputlist

def check_question_in_KB(uri, inputdic):
	if inputdic["multipleTriples"] == "True":
		return False
	else:
		query = "PREFIX dbo: <http://dbpedia.org/ontology/> PREFIX prop-ko: <http://ko.dbpedia.org/property/> " \
			"SELECT ?o " \
			"WHERE { <"+uri+"> "+ inputdic["property"] +" ?o .} "
		print(query)

		values = urlencode({'query': query})
		http = urllib3.PoolManager()

		url = server + 'query?' + values
		r = http.request('GET', url, headers=headers)
		label = ''
		request = json.loads(r.data.decode('UTF-8'))

		result_list = request['results']['bindings']

		print(result_list)
		if len(result_list) == 0:
			return False
		else:
			return True

def top_10_question_generator(EntityType):
	f = codecs.open("data/types_analysis/"+EntityType+".txt", "r", encoding="utf-8")
	qlist = []
	f.readline()
	for line in f.readlines():
		line = line.strip().split("\t")
		if "ko.dbpedia.org/property" in line[0]:
			qlist.append(line[0])
		if len(qlist) == 10:
			break

	return qlist


if __name__ == "__main__":
	sample0 = {"dialogStatus":"hold", "pTopic":"http://ko.dbpedia.org/resource/현진영", "area":"MusicalArtist"}
	print(KB_incomplete(sample0))
	print(top_10_question_generator("SoccerPlayer"))



	