import json
from watson_developer_cloud import ConversationV1 as cv1

def get_classified_tag(text, is_student):
	if is_student:
		tag_var = cv1(username = 'dacea7af-7f3f-4a4f-9851-187d8c4f3be7', password='QrckQsNnayWe', version = '2017-10-06')
		wid = '4f9ff7a1-5f2e-49dd-ac75-0fb128b682f5'
		response = tag_var.message(workspace_id = wid, message_input = {})
		response = tag_var.message(workspace_id = wid, message_input = {'text' : text})
		if response['output']['text'] != []:
			# print response['output']['text'][0]
			return response['output']['text'][0]
	else :
		tag_var = cv1(username = 'dacea7af-7f3f-4a4f-9851-187d8c4f3be7', password='QrckQsNnayWe', version = '2017-10-06')
		wid = 'd3a1946a-ce70-44fd-a147-c12de15bc6a7'
		response = tag_var.message(workspace_id = wid, message_input = {})
		response = tag_var.message(workspace_id = wid, message_input = {'text' : text})
		if response['output']['text'] != []:
			# print response['output']['text'][0]
			return response['output']['text'][0]
	return None

def main():
	get_classified_tag("Food is not good", True)
	get_classified_tag("done", False)
	get_classified_tag("spam", False)

if __name__ == '__main__':
	main()