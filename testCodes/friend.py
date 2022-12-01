import requests
import json
with open('./data/kakao_code.json', 'r') as fp:
    tokens = json.load(fp)



friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

# GET /v1/api/talk/friends HTTP/1.1
# Host: kapi.kakao.com
# Authorization: Bearer ${ACCESS_TOKEN}

headers={"Authorization" : "Bearer " + tokens["access_token"]}

print(tokens["access_token"])


result = json.loads(requests.get(friend_url, headers=headers).text)

print(type(result))
print("=============================================")
print(result)
print("=============================================")
friends_list = result.get("elements")
print("friends_list: ")
print(friends_list)
print(type(friends_list))
print("=============================================")
# friend_id = []

for i in range(len(friends_list)):
    print(friends_list[i].get("uuid"))
    friend_id = friends_list[i].get("uuid")
    print(friend_id)

    send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

    data={
        'receiver_uuids': '["{}"]'.format(friend_id),
        "template_object": json.dumps({
            "object_type":"text",
            "text":"성공입니다!",
            "link":{
                "web_url":"www.daum.net",
                "web_url":"www.naver.com"
            },
            "button_title": "바로 확인"
        })
    }

    response = requests.post(send_url, headers=headers, data=data)
    response.status_code