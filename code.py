#issue-1 closing factor to determine time
#issue -2 not picking one eye
#issue -3 not joining words
import cv2
import numpy
from gtts import gTTS
import os
import time

l_eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_lefteye_2splits.xml')
r_eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_righteye_2splits.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
cap = cv2.VideoCapture(0)

counter = 0
frame2 = ""
scale = 1.2
minSize = (2,2)
padding = (10,10)
minNeighbours = 5
left_eye_found = False
right_eye_found = False
sequence = list()
cmd_end = False
cmd_count = 0
Speak = False
joint_seq = ""
time = 0

def detect(frame):
    global left_eye_found, l_eye_x, l_eye_y, right_eye_found, r_eye_x, r_eye_y, frame2
    left_eye = l_eye_cascade.detectMultiScale(frame, scale, minNeighbours)
    left_most_eye = ()
    biggestArea = 0
    counter = 0
    left_eye_found = False 
    
    
    for (x,y,w,h) in left_eye:
        left_eye_found=True
        tempArea=w*h
        
        if counter==0:
            left_most_eye=(x,y,w,h)
            biggestArea=tempArea
            
        elif x>left_most_eye[0]:
            left_most_eye=(x,y,w,h)
            biggestArea=tempArea
            
        counter=counter+1
    
    if left_eye_found == True:
        x,y,w,h=left_most_eye
        cv2.rectangle(frame_eye, (x,y),(x+w,y+h),(0,255,0),1)
        l_eye_x=x
        l_eye_y=y
        
        
    right_eye = r_eye_cascade.detectMultiScale(frame, scale, minNeighbours)
    right_most_eye = ()
    biggestArea = 0
    counter = 0
    right_eye_found = False
    
    
    for (x,y,w,h) in right_eye:
        right_eye_found=True
        tempArea=w*h
        
        if counter==0:
            right_most_eye=(x,y,w,h)
            biggestArea=tempArea
            
        elif x>right_most_eye[0]:
            right_most_eye=(x,y,w,h)
            biggestArea=tempArea
            
        counter=counter+1
    
    if right_eye_found == True:
        x,y,w,h=right_most_eye
        cv2.rectangle(frame_eye, (x,y),(x+w,y+h),(0,0,255),1)
        r_eye_x=x
        r_eye_y=y

    return None


#Function to detect blinking
def detect_individual_eye(frame_for_detection):

    
    global l_eye_found,r_eye_found,l_eye_x,l_eye_y,r_eye_x,r_eye_y,l_eye_blink_state,r_eye_blink_state,scale,frame2
    
    l_eye_blink_state='closed'
    r_eye_blink_state='closed'
    
    eyes_rects = eye_cascade.detectMultiScale(frame_for_detection,scale,minNeighbours)
    
    counter=0
    for (x,y,w,h) in eyes_rects:
        if counter>=2:
            break
        cv2.rectangle(frame_eye,(x,y),(x+w,y+h),(255,255,255),1)
        
        if left_eye_found == True and abs(l_eye_x-x)<frame_x*.05 and abs(l_eye_y-y)<frame_y*.05:
            l_eye_blink_state='open'
        elif right_eye_found == True and abs(r_eye_x-x)<frame_x*.05 and abs(r_eye_y-y)<frame_y*.05 :
            r_eye_blink_state='open'
        counter=counter+1
        
    return None

def Morse_code():
    if l_eye_blink_state == "closed" and r_eye_blink_state == "open":
        return "."
    elif r_eye_blink_state == "closed" and l_eye_blink_state == "open":
        return "_"
    elif r_eye_blink_state == "closed" and l_eye_blink_state == "closed":
        return "*"
    
    
def Voice(joint) :

        list = [".", "_", "..", "._", "_.", "__", "...", "___"]
        mytext = ""
        if joint == list[0]:
            mytext = "yes "
    
        elif joint == list[1]:
             mytext = "no "
        
        elif joint == list[2]:
            mytext = "Its urgent, please walk me through the toilet "
    
        elif joint == list[3]:
            mytext = "Help, Emergency, Help"

        elif joint == list[4]:
            mytext = "I am hungry, please bring something to eat"
    
        elif joint == list[5]:
            mytext = "Feeling pretty thirsty, please bring a glass of water"
    
        elif joint == list[6]:
            mytext = "Random command 3"
    
        elif joint == list[7]:
            mytext = "random command 4"
            
         elif joint == "*":
            mytext = "Initializing"
        if time > 10 sec:
            cmd_count = 0
            return
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save("voices.mp3")
        os.system("voices.mp3")
            
    

   
while True:
    temp_state = ""
    _,frame = cap.read()
    frame = cv2.resize(frame,(320,240))
    if counter == 0:
        frame_x = frame.shape[1]
        frame_y = frame.shape[0]
        
    frame_eye = frame.copy()
    detect(frame)
    detect_individual_eye(frame)
    cv2.imshow("Blinks",frame_eye)
    
    temp = Morse_code()
    if cmd_count == 0:
            joint_seq = ""
            cmd_count += 1
            Voice("*")
    elif cmd_count > 0:
        if temp == "*":
            Voice(joint_seq)
            joint_seq = ""
        elif temp == "." or temp == "_":
           #Joining all the appended elements together 
            joint_seq = ("".join(temp))   
    
   
    
    k = cv2.waitKey(1)
    if k == "s":
        break
        
cap.release()
cv2.deleteAllWindows()

    
