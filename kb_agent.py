import json
from urllib.parse import urlencode
import urllib3

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

	outputlist = []
	for q in qlist:
		if check_question_in_KB(pTopic, q):
			if q["multipleTriples"] == "True":
				qjson = q
				outputlist.append(qjson)
		else:
			qjson = q
			outputlist.append(qjson)

	return outputlist


# 추후 개발
def check_question_in_KB(uri, inputdic):
	return False


if __name__ == "__main__":
	sample0 = json.dumps({"dialogStatus":"hold", "pTopic":"ko.dbpedia.org/resource/현진영", "area":"MusicalArtist"})
	print(KB_incomplete(sample0))


	