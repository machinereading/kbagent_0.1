import requests
import json

TEST_KEY = "32494ce8-bedb-4f31-9475-027f8b660ed1"

def simsimi_interface(input_json):

	# test용도
	if input_json == None:
		input_dict = dict()
		input_dict["text"] = "난 [태연]을 좋아해"
		input_dict["lang"] = "ko"
	else:
		input_dict = input_json

	input_text = input_dict["text"]
#	print(input_text)
	input_lang = input_dict["lang"]

	# key : 현재 가지고 있는 key.
	# lc : language
	# ft : 0.0 ~ 1.0까지의 값이 있으며 1.0이면 비속어가 섞인 대답은 하지 않음
	# text : input text
	r = requests.get("http://api.simsimi.com/request.p?key="+TEST_KEY+"&lc="+input_lang+"&ft=1.0&text="+input_text)
	response_str = r.content.decode("utf-8")
	response_dict = json.loads(response_str)

	return_dict = dict()
	
	return_dict["lang"] = input_lang


	if response_dict["result"] == 100:
		return_dict["text"] = response_dict["response"].replace('\n',' ')
	else:
		error_str = "Error code : " + str(response_dict["result"]) + " Error message : " + response_dict["msg"]
		return_dict["text"] = error_str

	return_dict["bot"] = "simsimi"

	response_json = return_dict

#	print(response_json)
#	print(return_dict["text"])
	
	return response_json


def test():
	r = requests.get("http://sandbox.api.simsimi.com/request.p?key=" + TEST_KEY + "&lc=ko&ft=1.0&text=너 영어는 할줄아냐?amumal")
	response_str = r.content.decode("utf-8")
	response_dict = json.loads(response_str)
	response_json = json.dumps(response_dict, indent=4, sort_keys=True)

	print(response_json)

	print(response_dict["response"])

	return response_json



if __name__ == '__main__':	

	simsimi_interface(None)

	"""

	r = requests.get("http://sandbox.api.simsimi.com/request.p?key=" + TEST_KEY + "&lc=ko&ft=0.0&text=안녕")

	print(r.status_code)
	print(r.headers)
	print(r.content)
	print(r.content["response"])
	"""
