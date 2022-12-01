import cv2
import dlib
import numpy as np
from functools import wraps
from scipy.spatial import distance
import RPi.GPIO as GPIO
import time
import telegram
import requests
import json

TOKEN = "5727339733:AAGrTLcd74yedbEid42fCBacLiRk4FZz0Dk"

stop_time = 0
count = 0
right_distance = 10
left_distance = 0
count_bool = False

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)

bot = telegram.Bot(token=TOKEN)

with open('./data/kakao_code.json', 'r') as fp:
    tokens = json.load(fp)
    
friend_url = "https://kapi.kakao.com/v1/api/talk/friends"

# GET /v1/api/talk/friends HTTP/1.1
# Host: kapi.kakao.com
# Authorization: Bearer ${ACCESS_TOKEN}

headers={"Authorization" : "Bearer " + tokens["access_token"]}
result = json.loads(requests.get(friend_url, headers=headers).text)
friends_list = result.get("elements")

def kakao() :
    for i in range(len(friends_list)):
        print(friends_list[i].get("uuid"))
        friend_id = friends_list[i].get("uuid")
        print(friend_id)

        send_url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

        data={
            'receiver_uuids': '["{}"]'.format(friend_id),
            "template_object": json.dumps({
                "object_type":"text",
                "text":"WARNING!!!!!!!!!! HE IS SLEEPING NOW IN HIS CAR !",
                "link":{
                    "web_url":"www.daum.net",
                    "web_url":"www.naver.com"
                },
                "button_title": "바로 확인"
            })
        }

        response = requests.post(send_url, headers=headers, data=data)
        response.status_code



# dlib model
faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')

# camera setting
video_capture = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

RIGHT_EYE_POINTS = list(range(36, 42))
LEFT_EYE_POINTS = list(range(42, 48))

def calculate_EAR(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear_aspect_ratio = (A+B)/(2.0*C)
    return ear_aspect_ratio

def detect(gray, frame):
    global stop_time, count, left_distance, right_distance, count_bool
    
    if stop_time >= 200:
        stop_time = 0
        count = 0
        count_bool = False
    
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.05,
                                         minNeighbors=5,
                                         minSize = (100, 100),
                                         flags = cv2.CASCADE_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        dlib_rect = dlib.rectangle(int(x), int(y), int(x+w), int(y+h))
        landmarks = np.matrix([[p.x, p.y] for p in predictor(frame, dlib_rect).parts()])
        
        landmarks_display = landmarks[37:42]
        for index, point in enumerate(landmarks_display):
            # right
            # 37 - 41
            # 38 - 40
            
            # left
            # 43 - 47
            # 44 - 46
            
            if index == 0:
                eye_top = point[0, 1]

            if index == 2:
                eye_bottom = point[0, 1]
                right_distance = eye_bottom - eye_top
            
            pos = (point[0, 0], point[0, 1])
            cv2.circle(frame, pos, 2, color=(0, 255, 255), thickness =- 1)
            
        left_landmarks_display = landmarks[43:48]
        for index, point in enumerate(left_landmarks_display):
            # 38 - 40 right
            # 43 - 47 left
            
            if index == 0:
                eye_top = point[0, 1]
                
            if index == 4:
                eye_bottom = point[0, 1]
                left_distance = eye_bottom - eye_top
            
            pos = (point[0, 0], point[0, 1])
            cv2.circle(frame, pos, 2, color=(0, 255, 255), thickness =- 1)
            
    print('rightDistance: ', right_distance)
    print('leftDistance: ', left_distance)
    
    if ((right_distance + left_distance) / 2) <= 2:
        count += 1
        print('close')
        count_bool = True
        
    if count_bool:
        stop_time += 1
    print('time: ', stop_time)
    print('count: ', count)
    
    if count >= 10:
        print('Sleep!!!!!')
        # sound baam
        try:
            pwm = GPIO.PWM(3, 2000)
            GPIO.output(4, True)
            
            for i in range(0, 20):
                pwm.start(100.0)
                time.sleep(0.05)
                pwm.stop()
                time.sleep(0.05)    
            
            
            GPIO.output(4, False)

            kakao()
            bot.sendMessage(chat_id='-1001789099529', text="WARNING!!!!!!!!!! HE IS SLEEPING NOW IN HIS CAR ")
            
        except Exception as e:
            print("error : ", e)
        
        # motor
        
        stop_time = 0
        count = 0
        count_bool = False
        
        
        
    right_distance = 10
    left_distance = 0
    return frame

while True:
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    
    canvas = detect(gray, frame)
    
    cv2.imshow("haha", canvas)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video_capture.release()
cv2.destroyAllWindows()
