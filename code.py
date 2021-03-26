import cv2
import numpy

#################################################################################################################################################################################
l_eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_lefteye_2splits.xml')
r_eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_righteye_2splits.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_eye.xml')
cap = cv2.VideoCapture(0)

counter = 0
frame2 = ""

left_eye_found = False

right_eye_found = False

#################################################################################################################################################################################

#function to detect left and right eye
def detect(frame):
    global left_eye_found, l_eye_x, l_eye_y, right_eye_found, r_eye_x, r_eye_y, frame2
    left_eye = l_eye_cascade.detectMultiScale(frame, 2, 10)
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
        cv2.rectangle(frame2, (x,y),(x+w,y+h),(0,255,0),2)
        l_eye_x=x
        l_eye_y=y
        
    
    
    right_eye = r_eye_cascade.detectMultiScale(frame, 2, 10)
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
        cv2.rectangle(frame2, (x,y),(x+w,y+h),(0,0,255),2)
        r_eye_x=x
        r_eye_y=y
        
        
    cv2.imshow("FRAME", frame2)
    return None

#################################################################################################################################################################################


#Function to detect blinking
def detect_eyes(frame_for_detection):

    
    global l_eye_found,r_eye_found,l_eye_x,l_eye_y,r_eye_x,r_eye_y,l_eye_blink_state,r_eye_blink_state,scale,frame2
    
    l_eye_blink_state='closed'
    r_eye_blink_state='closed'
    
    eyes_rects = eye_cascade.detectMultiScale(frame_for_detection,scaleFactor=2,minNeighbors=40)
    
    counter=0
    for (x,y,w,h) in eyes_rects:
        if counter>=2:
            break
        cv2.rectangle(frame2,(x,y),(x+w,y+h),(255,255,255),3)
        
        if abs(l_eye_x-x)<frame_x*.03 and abs(l_eye_y-y)<frame_y*.03 and left_eye_found == True:
            l_eye_blink_state='open'
            print("L")
        elif abs(r_eye_x-x)<frame_x*.05 and abs(r_eye_y-y)<frame_y*.05 and right_eye_found == True:
            r_eye_blink_state='open'
            print("R")
        counter=counter+1
        
    return None
    
#################################################################################################################################################################################

def Morse_code():
    pass
def Voice():
    pass
    
#################################################################################################################################################################################

while True:
    
    _,frame = cap.read()
    if counter == 0:
        frame_x = frame.shape[1]
        frame_y = frame.shape[0]
        
    frame2 = frame.copy()
    detect(frame)
    detect_eyes(frame)
    
    k = cv2.waitKey(1)
    if k == "s":
        break
        
cap.release()
cv2.deleteAllWindows()

    
