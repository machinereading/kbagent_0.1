import nlu_module
import nlg_module
import kb_agent
import dm_module
import json
import error_handler
import pprint
import simsimi
import random
from time import strftime
from ka import ka_by_question
from feedback_module import Feedback

#dialogAct = ['START']

dm = dm_module.DM()
nlu = nlu_module.NLU()
nlg = nlg_module.NLG()

def ioAdapter(utterance):
    result = {}
    result['utterance'] = utterance
    return result

#def controller(lang):

def chat_classifier(kblang):
    utterance = kblang['dialog'][-1]['utterance']
    with open('./chat.class','r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            lines = line.split('\t')
            for i in lines:
                i = i.strip()
            candi_class = lines[0]
            key_words = lines[1].split(',')

    chat_class = False
    for i in key_words:
        if i in utterance:
            chat_class = candi_class
            break
    if chat_class:
        pass
    else:
        chat_class = 'chitchat'

    if utterance == '시작':
        chat_class = 'MusicalArtist'
    return chat_class

def get_chitchats(kblang):
    chitchats = []
    input_json = {}
    input_json['text'] = kblang['dialog'][-1]['utterance']
    input_json['lang'] = 'ko'

    #simsimi
    sim_result = simsimi.simsimi_interface(input_json)
    chitchats.append(sim_result)
    result = {}
    result['speaker'] = 'system_'+select_best_chitchats(chitchats)['bot']
    result['utterance'] = select_best_chitchats(chitchats)['text']
    result['dialogAct'] = 'chitchat'

#    print(result)
    return result

def select_best_chitchats(chitchats):
    # random
    d = random.choice(chitchats)
    return d



def olivia(kblang):
    chat_class = chat_classifier(kblang)
    if chat_class == 'chitchat' and kblang['area'] == 'chitchat':
        response = get_chitchats(kblang)
        dialog = dialog = kblang['dialog']
        dialog.append(response)
        kblang['dialog'] = dialog


    else:
        if kblang['dialogAct'][-1] == 'Opening' or kblang['dialogAct'][-1] == 'Thanking':
            dialog = kblang['dialog']
            dialog[-1]['dialogAct'] = 'Opening'
            kblang['dialog'] = dialog
            dialogAct = kblang['dialogAct']
            dialogAct.append('start')
            kblang['dialogAct'] = dialogAct
            kblang['area'] = chat_class
            kblang = dm.dm(kblang)
            response = nlg.nlg(kblang)
            response['speaker'] = 'system_kbagent'
            response['dialogAct'] = kblang['dialogAct'][-1]
            dialog = kblang['dialog']
            dialog.append(response)
            kblang['dialog'] = dialog
        else:
            nlu_input = {}
            nlu_input['utterance'] = kblang['dialog'][-1]['utterance']
            nlu_input['dialogAct'] = kblang['dialogAct']
            nlu_output = nlu.nlu(nlu_input)

            dialog = kblang['dialog'][-1]
            dialog['dialogAct'] = nlu_output['intent']

            kblang['cTopics'] = nlu_output['cTopics']
            dialogAct = kblang['dialogAct']
            dialogAct.append(nlu_output['intent'])
            kblang['dialogAct'] = dialogAct

            kblang = dm.dm(kblang)
            #kblang = ka_by_question(kblang)

            if kblang['dialogStatus'] == 'feedback':
                kblang = Feedback.checker(kblang)

            if kblang['dialogStatus'] == 'end':
                response = {}
                response['speaker'] = 'system_kbagent'
                dialogAct = kblang['dialogAct']
                dialogAct = dialogAct[:-1]
                dialogAct.append('Thanking')
                kblang['dialogAct'] = dialogAct
                response['dialogAct'] = dialogAct[-1]
                response['utterance'] = '정말 감사합니다. 혹시 다른 관심있는 주제가 있으세요?'
                dialog = kblang['dialog']
                dialog.append(response)
                kblang['dialog'] = dialog

                #로그 저장
                now = strftime("%y%m%d_%H%M%S")
                logid = str(now)+'_'+str(random.randint(1,1000))
                dialog_logging(kblang)

                kblang['area'] = 'chitchat'

            elif kblang['dialogStatus'] == 'feedback':
                pass

            else:
                response = nlg.nlg(kblang)
                response['speaker'] = 'system_kbagent'
                response['dialogAct'] = kblang['dialogAct'][-1]
                dialog = kblang['dialog']
                dialog.append(response)
                kblang['dialog'] = dialog

    return kblang



def dialog_logging(kblang):
    now = strftime("%y%m%d_%H%M%S")
    logid = str(now)+'_'+str(random.randint(1,1000))
    filename = './logs/'+logid
    with open(filename,'w', encoding='utf-8') as f:
        json.dump(kblang['dialog'],f,indent=4,ensure_ascii=False)
    print(filename, '이 저장되었습니다')



def olivia_old(kblang):
    if kblang['dialog'][-1]['utterance'] == '시작':
        kblang = dm.dm(kblang)
        response = nlg.nlg(kblang)
        response['speaker'] = 'system'
        dialog = kblang['dialog']
        dialog.append(response)
        kblang['dialog'] = dialog
    else:
        nlu_input = {}
        nlu_input['utterance'] = kblang['dialog'][-1]['utterance']
        nlu_input['dialogAct'] = kblang['dialogAct']
        nlu_output = nlu.nlu(nlu_input)
        kblang['cTopics'] = nlu_output['cTopics']
        dialogAct = kblang['dialogAct']
        dialogAct.append(nlu_output['intent'])
        kblang['dialogAct'] = dialogAct
        #print(nlu_output)

        kblang = dm.dm(kblang)
        response = nlg.nlg(kblang)
        response['speaker'] = 'system'
        dialog = kblang['dialog']
        dialog.append(response)
        kblang['dialog'] = dialog

    return kblang    

def terminal():
    #SETTING
    kblang = {}
    kblang['dialogAct'] = ['Opening']
    kblang['dialog'] = []
    kblang['area'] = 'chitchat'
    conti = True
    while conti == True:
        utterance = input("USER>> ")
        utterance = ioAdapter(utterance)
        utterance['speaker'] = "user"
        dialog = kblang['dialog']
        dialog.append(utterance)
        kblang['dialog'] = dialog

        kblang = olivia(kblang)
        response = kblang['dialog'][-1]['utterance']
        print("SYSTEM>>",response)


