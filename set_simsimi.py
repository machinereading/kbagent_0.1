import requests
import json

TEST_KEY = "32494ce8-bedb-4f31-9475-027f8b660ed1"
input_lang = 'ko'

def set_simsimi():
    slangs = []
    with open('./slang','r') as f:
        for line in f:
            line = line.strip()
            slangs.append(line)

    for word in slangs:
        print(word)
        data={}
        data['key'] = TEST_KEY
        data['lc'] ='ko'
        data['word']=word

        r = requests.post("http://api.simsimi.com/filter",data=data)

        

        response = r.content.decode('utf-8')

        print(response,type(response))
set_simsimi()
