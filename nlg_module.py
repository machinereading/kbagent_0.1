import json
import state

class NLG:
	def __init__(self):
		self.states = state.FSM("states", "dict")


	def nlg(self, inputJson):
		return self.states.generate(inputJson)

	# def convertTagToText(self, tagCandidate):
	# 	tags = tagCandidate.split(":")
	# 	if len(tags) < 2: return tagCandidate
	# 	tag = tags[1].lower()
	# 	if tag in self.dict:
	# 		return self.dict[tag]
	# 	return tagCandidate

	# def generateQuestion(self, dialogAct, pTopic, prop, concept, questionType):
	# 	if dialogAct[-1] == "CheckQuestion":
	# 		return "%s %s인가요?" % (self.eun(pTopic), concept)
	# 	if pTopic == None or len(pTopic) == 0:
	# 		return "어느 %s의 %s 좋아하시나요?" % (prop, self.eul(concept))
	# 	if questionType == "opinion":
	# 		if prop == "kbox:evaluation" :
	# 			return "%s 어떻게 생각하세요?" % self.eul(pTopic)
	# 	return "%s 관련된 어느 %s 좋아하시나요?" % (self.gwa(pTopic), self.eul(concept))
		
	# def generateCheckQuestion(self, pTopic, concept):
	# 	return "%s %s인가요?" % (self.eun(pTopic), concept)

	# def hasJongsung(self, character):
	# 	x = ord(character)
	# 	if(x < 0xAC00 and x > 0xD7A3): return False
	# 	return (x - 0xAC00) % 28 != 0

	def test(self):
		f = open("test", encoding="UTF8")
		for line in f.readlines():
			print(line.strip())
			print(json.dumps(self.nlg(json.loads(line.strip())), ensure_ascii=False))
		


if __name__ == '__main__':
	nlg = NLG()
	nlg.test()