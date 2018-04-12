import json

class NLU:
	def __init__(self):
		pass

	def topicIdentifier(self, utterance):
		topic_list = []

		# --

		import re

		match = re.findall(r'\[(.+?)\]', utterance)

		topic_list = list(match)

		return topic_list		

	def sentimentAnalysis(self, utterance):
		positive_words = ['응', '그래', '맞아', '그거야', '좋아해']
		negative_words = ['아니', '아닌데', '아니야', '노노', '싫어해']

		# --

		sentiment = 0

		# --

		for p in positive_words:
			if p in utterance:
				sentiment += 1

		# --

		for n in negative_words:
			if n in utterance:
				sentiment -= 1

		# --

		if sentiment > 0:
			return 'positive'

		elif sentiment < 0:
			return 'negative'

		else:
			return 'neutral'

	def nlu(self, i_json):
		o_json = {}

		# --

		utterance = i_json['utterance']
		dialogAct = i_json['dialogAct']

		# -- topic analysis

		cTopics = self.topicIdentifier(utterance)

		# --

		o_json['cTopics'] = cTopics

		# -- intent analysis

		positive_words = ['응', '그래', '맞아', '그거야', '좋아', '조아']
		negative_words = ['아니', '아닌데', '싫어', '시러']

		if dialogAct[-1] == 'Question' or dialogAct[-1] == 'Thanking':
			intent = 'Answer'

		elif dialogAct[-1] == 'CheckQuestion':
			if self.sentimentAnalysis(utterance) == 'positive':
				intent = 'Agree'

			elif self.sentimentAnalysis(utterance) == 'negative':
				intent = 'Disagree'

			elif self.sentimentAnalysis(utterance) == 'neutral':
				intent = 'Neutral'

		# --

		o_json['intent'] = intent

		# --

		return o_json

	def test(self):
		# -- test case 1

		i_json = {'utterance': '[뉴잭스윙]을 좋아해', 'dialogAct':['Question']}

		print('test case 1')

		import json

		print(json.dumps(self.nlu(i_json), indent=4, separators=(',', ':'), ensure_ascii=False))

		# -- test case 3
		
		i_json = {'utterance': '응 어떻게 알았지? [소녀시대]랑 [태연]이 제일 좋아', 'dialogAct':['CheckQuestion']}

		print('test case 2')

		import json

		print(json.dumps(self.nlu(i_json), indent=4, separators=(',', ':'), ensure_ascii=False))

		# -- test case 1
		
		i_json = {'utterance': '아닌데 잘좀 맞춰봐', 'dialogAct':['CheckQuestion']}

		print('test case 3')
		
		import json

		print(json.dumps(self.nlu(i_json), indent=4, separators=(',', ':'), ensure_ascii=False))

# --




