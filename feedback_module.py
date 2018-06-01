import json

class Feedback:
	def __init__(self):
		pass

	def checker(kblang):
		triple = kblang['obtained_triple']
		check = 0
		for i in range(len(triple)):
			if triple[i].count('\t') == 2:
				data = triple[i].split('\t')
				if kblang['dialogAct'][-3] != 'CheckQuestion' or  check == 1:
					dialogAct = kblang['dialogAct']
					dialogAct.append('CheckQuestion')
					response = {}
					response['speaker'] = 'system_kbagent'
					response['dialogAct'] = 'CheckQuestion'
					response['utterance'] = data[0] + '의 ' + data[1] + '는 ' + data[2] + '인가요?'
					dialog = kblang['dialog']
					dialog.append(response)
					kblang['dialog'] = dialog
					kblang['dialogAct'] = dialogAct
					i = i - 1
					break
				else:
					if kblang['dialogAct'][-2] == 'Agree':
						triple[i] = triple[i] + '\tY'
					else:
						triple[i] = triple[i] + '\tN'
					kblang['obtained_triple'][i] = triple[i]
					check = 1
		if i == len(triple) - 1:
			dialogAct = kblang['dialogAct']
			dialogAct = dialogAct[:-2]
			dialogAct.append('end')
			kblang['dialogAct'] = dialogAct
			kblang['dialogStatus'] = 'end'

		return kblang
			
