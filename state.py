eun = lambda x: "" if len(x) == 0 else ("은" if hasJongsung(x[-1]) else "는")
eul = lambda x: "" if len(x) == 0 else ("을" if hasJongsung(x[-1]) else "를")
ee = lambda x: "" if len(x) == 0 else ("이" if hasJongsung(x[-1]) else "가")
gwa = lambda x: "" if len(x) == 0 else ("과" if hasJongsung(x[-1]) else "와")

def hasJongsung(character):
		x = ord(character)
		if(x < 0xAC00 and x > 0xD7A3): return False
		return (x - 0xAC00) % 28 != 0
class FSM:
	def __init__(self, stateFile, dictFile):
		self.tagDict = self.loadDict(dictFile)
		self.states = self.loadStates(stateFile)
		self.initialState = self.findState("init")

		

	def loadDict(self, dictFileName):
		result = {}
		f = open("dict", encoding="UTF8")
		for line in f.readlines():
			sp = line.strip().split(",")
			result[sp[0]] = sp[1]
		f.close()
		return result

	def loadStates(self, stateFileName):
		import json
		f = open(stateFileName, 'r', encoding="UTF8")
		jd = json.load(f)
		result = []
		for name, val in jd["states"].items():
			result.append(State(name, val))
		f.close()
		return result

	

	def convertTagToText(self, tagCandidate):
		tags = tagCandidate.split(":")
		tag = tags[-1].lower()
		if tag in self.tagDict:
			return self.tagDict[tag]
		return tags[-1]

	def findState(self, stateName):
		for item in self.states:
			if item.name == stateName:
				return item

	def generate(self, js):
		current = self.initialState
		while True:
			t = list(filter(lambda x: x is not None, current.transit(js)))
			if len(t) > 0:
				#rule은 순서대로 적용 - 먼저 나온 rule이 무조건 우선순위를 가진다.
				current = self.findState(t[0])
				continue
			count = 0
			result = ""
			keys = []
			for item in current.generationKeys:
				if type(item) is str:
					keys.append(self.convertTagToText(js[item]))
				else:
					keys.append(item(keys[-1]))
			for c in current.generation:
				if c == '\\':
					result += keys[count]
					count += 1
				else:
					result += c

			return {"utterance": result}

class State:
	def __init__(self, name, jsonDict):
		josa = {"eun": eun, "eul": eul, "ee": ee, "gwa": gwa}
		self.name = name
		self.transition = []
		if "rules" in jsonDict:
			for item in jsonDict["rules"]:
				self.transition.append(TransitionRule(item["condition"], item["transition"]))
		if "generation" in jsonDict:
			a = 0
			self.generation = ""
			self.generationKeys = []
			temp = ""
			for c in jsonDict["generation"]:
				if c == '[':
					a+=1
					continue
				if c == ']':
					a -= 1
					self.generation += "\\"
					if temp in josa: self.generationKeys.append(josa[temp])
					else: self.generationKeys.append(temp)
					temp = ""
					continue
				if a == 1:
					temp += c
				else: self.generation += c
	

	def transit(self, js):
		return list(map(lambda x: x.transition if x.transit(js) else None, self.transition))

class TransitionRule:
	def __init__(self, conditionDict, transition):
		self.condition = conditionDict
		self.transition = transition
		self.transitionfilter = {"last": self.lastis}

	def transit(self, js):
		for key, val in self.condition.items():
			keys = key.split(":")
			filterfunction = None
			if len(keys) > 1:
				filterfunction = self.transitionfilter[keys[1]]
				return filterfunction(js, keys[0], val)
			if key not in js:
				return False
			elif val not in js[key]:
				return False
		return True

	def lastis(self, js, key, val):
		if key not in js:
			return False
		return js[key][-1] == val

	def not_in(self, js, key, val):
		if key not in js:
			return True
		return js[key] not in val
