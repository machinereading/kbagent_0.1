import json
import pprint

def ka_by_question(kblang):
    print('##############################################')
    pprint.pprint(kblang)
    print('################################################')
    try:
        knowledge = kblang['obtained_knowledge'] 
    except:
        knowledge = []
    if kblang['dialogAct'][-1] == 'Agree':
        if kblang['keyEntity'] == '':
            t = {}
            t['e1'] = 'kbox:'+kblang['pTopic']
            t['r'] = kblang['property']
            t['e2'] = kblang['concept']
        else:
            t = {}
            t['e1'] = 'kbox:'+kblang['keyEntity']
            t['r'] = kblang['property']
            if len(kblang['allTopics']) >1:
                t['e2'] = kblang['allTopics'][-2]
            else:
                t['e2'] = kblang['allTopics'][-1]

    elif kblang['dialogAct'][-2] == 'Question' and kblang['dialogAct'][-1] == 'Answer':
        t = {}
        t['e1'] = 'kbox:'+kblang['keyEntity']
        t['r'] = kblang['property']
        t['e2'] = kblang['allTopics'][-1]
    else:
        pass
    knowledge.append(t)
    kblang['obtained_knowledge'] = knowledge
    return kblang
