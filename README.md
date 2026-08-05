# The-Quintessential-Quintuplets-Pose-Tracker
For The Quintessential Quintuplets fans, by The Quintessential Quintuplet fan. This project analyzes your body posture and can state whoever you're posing (based from the picture)

This was created via python, Google's MediaPipe framework to track movements, OpenCV for the camera and idk but ye just check the file lil bro

Currently not yet finished

[hand_tracker.py](https://github.com/user-attachments/files/30744325/hand_tracker.py)
import cv2 
import mediapipe as mp
import math
import pygame
import time

camera = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh

hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence= 0.7)
face = mp_face.FaceMesh(max_num_faces=2, refine_landmarks=True, min_detection_confidence=0.7)
draw = mp.solutions.drawing_utils
drawstyle = mp.solutions.drawing_styles

RefreshRate = pygame.time.Clock()

while camera.isOpened():
    RefreshRate.tick(15)
    success, frame = camera.read()
    if not success:
        print("whadahell")
        continue
    frame = cv2.flip(frame,1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    hand_results = hands.process(rgb_frame)
    face_results = face.process(rgb_frame)

    if hand_results.multi_hand_landmarks and face_results.multi_face_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:

                draw.draw_landmarks(frame,hand_landmarks, mp_hands.HAND_CONNECTIONS, drawstyle.get_default_hand_landmarks_style(), drawstyle.get_default_hand_connections_style())
                draw.draw_landmarks(image=frame,landmark_list=face_landmarks, connections=mp_face.FACEMESH_TESSELATION, landmark_drawing_spec=None, connection_drawing_spec=drawstyle.get_default_face_mesh_tesselation_style())
                            
                mouth_left = face_landmarks.landmark[61]
                mouth_right = face_landmarks.landmark[291]
                mouth_top = face_landmarks.landmark[13]
                mouth_down = face_landmarks.landmark[14]
                lowerright_jaw = face_landmarks.landmark[379]
                cheek_left = face_landmarks.landmark[234]
                cheek_right = face_landmarks.landmark[425]
                forehead = face_landmarks.landmark[10]
                chin = face_landmarks.landmark[152]

                #print(f"{cheek_left.x - cheek_right.x} {cheek_right.x:.2f}  {mouth_down.y:.2f}")
                #print(f"Upper Lip{mouth_top.x:.2f} {mouth_top.y:.2f} Lower Lip {mouth_down.x:.2f} {mouth_down.y:.2f}")
                #print(f"Right Corner {mouth_right.x:.2f} {mouth_right.y:.2f} Left Corner {mouth_left.x:.2f} {mouth_left.y:.2f}")
                #print()
                index = hand_landmarks.landmark[8]
                middle = hand_landmarks.landmark[12]
                thumb = hand_landmarks.landmark[4]
                wrist = hand_landmarks.landmark[0]
                ring = hand_landmarks.landmark[16]
    
                distance1 = math.sqrt(((thumb.x - index.x)**2)+(thumb.y-index.y)**2)

                #Miku's
                sidea1 = ((wrist.x - 0.5)**2)+(wrist.y-0)**2
                sidec1 = ((index.x - wrist.x)**2)+(index.y - wrist.y)**2
                sideb1 = ((index.x - 0.5)**2)+(index.y - 0)**2

                #Nino's
                sidea2 = ((forehead.x - chin.x)**2)+(forehead.y-0)**2
                sideb2 = (chin.y)**2
                sidec2 = ((chin.x - forehead.x)**2)+(chin.y - forehead.y)**2


                #angle index wrist line
                angleiwl = (sidea1 + sidec1 - sideb1)/(2*sidea1*sidec1)
                #print(f"{angleiwl}")
                #angle forehead chin line
                anglefcl = (sidea2 + sidec2 - sideb2)/(2*sidea2*sidec2)
                #print(f"{round(ring.x) - round(mouth_right.x)}")

                print("I'm detecting...")

                if (((mouth_top.y - mouth_down.y))<=(0.10)) and (0.10 <= distance1 <= 0.20) and (2.30 <= angleiwl <= 2.50):
                    print("MIKU NAKANO", end='', flush=True)
                
                elif ((0.10<= distance1<=0.25) or ((0.45<=mouth_top.y<=0.55) and (0.55<=mouth_down.y<=0.65))) and (2.30 <= angleiwl <= 2.65):
                    print("Trying to do a Miku Pose?", end='', flush=True)
                
               

                elif (abs(round(ring.x, 3) - round(mouth_right.x,3)) <= 0.03 and ((abs((mouth_top.y - mouth_down.y))>=0.02))):
                    print("YOTSUBA", end='', flush=True)
                
                elif (0 <= abs(round(ring.x, 3) - round(mouth_right.x,3)) <= 0.09) and not(-8 <= anglefcl <= -5) :
                    print("Trying to do a Yotsuba Pose?", end='', flush=True)

                elif (-8 <= anglefcl <= -6) and (0 <= abs(round(index.x, 3) - round(lowerright_jaw.x, 3)) <= 0.05):
                    print("NINO", end='', flush=True)
                    

                elif (-9 <= anglefcl <= -5):
                    print("Trying to do a Nino Pose?", end='', flush=True)
                #print(f"{abs(round(ring.x, 3) - round(mouth_right.x,3))}")

                #print(f"{abs(round(index.x, 3) - round(lowerright_jaw.x, 3))}")
                print(2*"")
    

                
    cv2.imshow("The Quintessential Quintuplets Pose Project", frame)

    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
