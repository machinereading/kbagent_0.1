import json
import error_handler
import csv
import kb_agent
import pprint

class DM:
    def __init__(self):
        pass

    def pTopicIdentifier(self, kblang):
        #longest entity
        pTopic = kblang['pTopic']
        cTopics = kblang['cTopics']
        oldTopics = kblang['allTopics']
        oldTopics = oldTopics + cTopics
        kblang['allTopics'] = oldTopics
        if len(cTopics) > 0:
            pTopic = max(kblang['cTopics'],key=len)
            kblang['pTopic'] = pTopic
        if kblang['N_of_Q'] == 0:
            kblang['keyEntity'] = pTopic
        if kblang['N_of_Q'] > 0:
            kblang['pTopic'] = kblang['keyEntity']
        else:
            pass

        return kblang

    def initiate(self,kblang):
        dialogAct = kblang['dialogAct']
        dialogAct.append('Question')
        kblang['dialogAct'] = dialogAct
        kblang['dialogStatus'] = 'start'
        kblang['pTopic'] = ''
        kblang['keyEntity'] = ''
        kblang['property'] = 'dbo:genre'
        kblang['concept'] = 'dbo:MusicalArtist'
#        kblang['area'] = 'MusicalArtist'
        kblang['questionType'] = 'opinion'
        kblang['N_of_Q'] = 0
        kblang['allTopics'] = []

        return kblang

    def call_error_handler(self,kblang):
        error_handler_input = {}
        error_handler_input['cTopics'] = kblang['cTopics']
        error_handler_input['intent'] = kblang['dialogAct'][-1]
        error_handler_input['concept'] = kblang['concept']
        error_handler_output = error_handler.error_handler(error_handler_input)

        unCertain = False
        for i in error_handler_output:
            if i['inContext'] == 'Uncertain':
                kblang['pTopic'] = i['label']
                dialogAct = kblang['dialogAct']
                dialogAct.append('CheckQuestion')
                kblang['dialogAct'] = dialogAct
                concept = False
                with open('./dict.errorhandler','r') as f:
                    reader = csv.reader(f)
                    for line in reader:
                        if line[0] == kblang['property']:
                            concept = line[1]
                            prop = line[2]
                            break
                if concept:
                    kblang['concept'] = concept
                    kblang['property'] = prop
                else:
                    pass
                unCertain = True
                break
            else:
                pass

        return kblang, unCertain

    def get_next_concept(self,kblang):
        concept = False
        rel = False
        with open('./dict.dm','r') as f:
            reader = csv.reader(f)
            for line in reader:
                if line[0] == kblang['concept']:
                    concept = line[1]
                    rel = line[2]
                    break
#        if rel:
#            kblang['property'] = rel
        return concept,kblang

    def get_incomplete_list(self,kblang):
        incomplete_list = kb_agent.KB_incomplete(kblang)

        if kblang['N_of_Q'] < len(incomplete_list) :
            kblang['concept'] = incomplete_list[kblang['N_of_Q']]['concept']
            kblang['property'] = incomplete_list[kblang['N_of_Q']]['property']
            kblang['questionType'] = incomplete_list[kblang['N_of_Q']]['questionType']
            kblang['N_of_Q'] = kblang['N_of_Q'] +1

        else:
            dialogAct = kblang['dialogAct']
            dialogAct = dialogAct[:-1]
            dialogAct.append('feedback')
            kblang['dialogAct'] = dialogAct
            kblang['dialogStatus'] = 'feedback'



        return kblang


    def dm(self,kblang):
        if kblang['dialogAct'][-1] == 'start':
            kblang = DM.initiate(self,kblang)

        else:
            kblang['dialogStatus'] = 'hold'
            kblang['questionType'] = 'factual'
#        kblang = DM.pTopicIdentifier(self,kblang)

#        print('===inDM')
#        pprint.pprint(kblang)
#        print('===inDM')
        if kblang['dialogStatus'] == 'hold':
            kblang = DM.pTopicIdentifier(self,kblang)
            #1) call error handler
            if kblang['N_of_Q'] == 0:
                kblang, unCertain = DM.call_error_handler(self, kblang)
            else:
                unCertain = False
#            kblang = DM.pTopicIdentifier(self,kblang)

            if unCertain == False:
                #error 가 없는 경우
                kblang = DM.pTopicIdentifier(self,kblang)

                #triple 추가
#                kblang = ka.ka_by_question(kblang)
                if kblang['dialogAct'][-1] == 'Answer' and kblang['dialogAct'][-3] != 'feedback':
                    incomplete_list = kb_agent.KB_incomplete(kblang)
                    if kblang['N_of_Q'] <= len(incomplete_list) and kblang['N_of_Q'] != 0:
                        obtained_triple = []
                        if 'obtained_triple' in kblang:
                            obtained_triple = kblang['obtained_triple']
                        obtained_triple.append(kblang['pTopic'] + '	' + kblang['property'] + '	' +kblang['cTopics'][-1])
                        kblang['obtained_triple'] = obtained_triple

                #2) dialogAct 가 agree 인 경우
                if kblang['dialogAct'][-1] == 'Agree' and kblang['dialogAct'][-3] != 'feedback':
                #triple 추가
                    obtained_triple = []
                    if 'obtained_triple' in kblang:
                        obtained_triple = kblang['obtained_triple']
                    obtained_triple.append(kblang['pTopic'] + '	' + kblang['property'] + '	' + kblang['concept'])
                    kblang['obtained_triple'] = obtained_triple

                    dialogAct = kblang['dialogAct']
                    dialogAct.append('Question')
                    kblang['dialogAct'] = dialogAct
                    concept,kblang = DM.get_next_concept(self,kblang)
                    if concept != False:
                        kblang['concept'] = concept
                    else:
                        kblang = DM.get_incomplete_list(self,kblang)

                elif kblang['dialogAct'][-1] == 'Disagree' and kblang['dialogAct'][-3] != 'feedback':
                    dialogAct = kblang['dialogAct']
                    dialogAct.append('Question')
                    kblang['dialogAct'] = dialogAct
                    if len(kblang['allTopics']) > 1:
                        kblang['cTopic'] = kblang['allTopics'][-2]
                        kblang['keyEntity'] = kblang['allTopics'][-2]
                        kblang['pTopic'] = kblang['allTopics'][-2]
                    else:
                        kblang['cTopic'] = kblang['allTopics'][-1]
                        kblang['keyEntity'] = kblang['allTopics'][-1]
                        kblang['pTopic'] = kblang['allTopics'][-1]
                else:
                    dialogAct = kblang['dialogAct']
                    dialogAct.append('Question')
                    kblang['dialogAct'] = dialogAct
                    concept,kblang = DM.get_next_concept(self,kblang)
                    if concept != False:
                        kblang['concept'] = concept
                    else:
                        kblang = DM.get_incomplete_list(self,kblang)
            else:
                pass

        return kblang



