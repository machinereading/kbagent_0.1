import json
import aiml

eun = lambda x: "" if len(x) == 0 else ("은" if hasJongsung(x[-1]) else "는")
eul = lambda x: "" if len(x) == 0 else ("을" if hasJongsung(x[-1]) else "를")
ee = lambda x: "" if len(x) == 0 else ("이" if hasJongsung(x[-1]) else "가")
gwa = lambda x: "" if len(x) == 0 else ("과" if hasJongsung(x[-1]) else "와")
eomi_ee = lambda x: "" if len(x) == 0 or not hasJongsung(x[-1]) else "이"
redirection = {"은": eun, "을": eul, "이": ee, "과": gwa, "어미_이": eomi_ee}
def hasJongsung(character):
	x = ord(character)
	if(x < 0xAC00 and x > 0xD7A3): return False
	return (x - 0xAC00) % 28 != 0

class NLG:
	def __init__(self):

		# self.states = state.FSM("states", "dict")
		self.loadAIML()
		self.loadDict()


	# main function. generate utterance from input json
	def nlg(self, inputJson):
		return {"utterance": self.postprocess(self.aimlKernel.respond(self.preprocess(inputJson)), inputJson)}
		

	# load AIML file and train kernel
	def loadAIML(self, f="nlgAIML.xml"):
		self.aimlKernel = aiml.Kernel()
		self.aimlKernel.learn(f)

	# load tag dictionary
	def loadDict(self, dictFileName="dict"):

		self.tagDict = {}
		f = open("nlgdict", encoding="UTF8")
		for line in f.readlines():
			sp = line.strip().split(",")
			self.tagDict[sp[0]] = sp[1]
		f.close()
	
	# convert English tags/colon tags into Korean tags
	def convertTagToText(self, tagCandidate):
	
		tags = tagCandidate.split(":")
		tag = tags[-1].lower()
		if tag in self.tagDict:
			return self.tagDict[tag]
		return tags[-1]

	# process raw json to aiml-understandable string
	# python-aiml module recognizes no punctuation and order-sensitive, so we need to convert json into fixed form
	# PROPERTY1 VALUE1 E | PROPERTY2 VALUE2 ...
	# if value is list, 
	# properties must be in alphabet-order
	def preprocess(self, inputJson):
		# print(inputJson)
		ignoreKey = ["dialog"]
		items = []
		result = []
		# sort key in alphabetical order
		for k, v in inputJson.items():
			items.append((k, v))
		items.sort(key=lambda x: x[0])
		result.append("DIV") # always start with * in AIML
		for item in items:
			k, v = item[0], item[1]
			if k in ignoreKey:
				continue
			result.append(k)
			if type(v) == list:
				result.append("LISTBEGIN") # list start notation
				for i in v:
					result.append(i)
				result.append("LISTEND") # list end notation
			else: 
				if type(v) is not str:
					result.append(str(v))
					continue
				for tagFragment in v.split(":"):
					result.append(tagFragment.replace("-", ""))
			result.append("DIV") # always put * between tags
		return " ".join(result)

	# from aiml response, put proper tag value into slots, noted as [tag]
	# also make response more natural like putting right josa like [을]
	# area that needs postprocessing will be enclosed by []
	def postprocess(self, utterance, inputJson):
		
		last = ""
		flag = False
		result = []
		sysval = ""
		for c in utterance:
			if c == '[':
				flag = True
				continue
			if c == ']':
				flag = False
				if sysval in redirection:
					result.append(redirection[sysval](last))
				else:
					try:
						result.append(self.convertTagToText(inputJson[sysval]))
					except KeyError:
						print("Keyerror: %s is not in json" % sysval)
						result.append(sysval)
				sysval = ""
				last = result[-1]
				continue
			if flag:
				sysval += c
				continue
			last = c
			result.append(c)
		return "".join(result)


	def test(self):
		f = open("nlgtest", encoding="UTF8")
		for line in f.readlines():
			print(line.strip())
			print(json.dumps(self.nlg(json.loads(line.strip())), ensure_ascii=False))

	def aimltest(self, teststr):
		print(self.aimlKernel.respond(teststr))

if __name__ == '__main__':
	nlg = NLG()
	# nlg.aimltest("hello hello w,")
	nlg.test()
