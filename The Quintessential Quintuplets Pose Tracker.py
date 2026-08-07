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


def distance(p1, p2, p3, p4):

    ax = p1.x
    ay = p1.y
    az = p1.z
    bx = p2.x
    by = p2.y
    bz = p2.z


    #reference points
    cx = p3.x
    cy = p3.y
    cz = p3.z
    dx = p4.x
    dy = p4.y
    dz = p4.z

    return round(math.sqrt((ax - bx)**2+(ay - by)**2+(az-bz)**2) / math.sqrt((cx-dx)**2 + (cy-dy)**2 + (cz-dz)**2), 2)

def angle_finger(p1, p2):

    ax = p1.x
    ay = p1.y

    bx = p2.x
    by = p2.y
    frameH, frameW, _ = frame.shape
    dx = ax - bx
    dy = by - ay

    finger_angle = math.degrees(math.atan2(dy, dx))
    wrist_angle = abs(finger_angle - 90)

    if wrist_angle>180:
        wrist_angle=360-wrist_angle

    return wrist_angle







pygame.init()
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

                #draw.draw_landmarks(frame,hand_landmarks, mp_hands.HAND_CONNECTIONS, drawstyle.get_default_hand_landmarks_style(), drawstyle.get_default_hand_connections_style())
                #draw.draw_landmarks(image=frame,landmark_list=face_landmarks, connections=mp_face.FACEMESH_TESSELATION, landmark_drawing_spec=None, connection_drawing_spec=drawstyle.get_default_face_mesh_tesselation_style())
                            

                mouth_left = face_landmarks.landmark[61]
                left_y_cheek = face_landmarks.landmark[212]
                mouth_top_right = face_landmarks.landmark[267]
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
                index_base = hand_landmarks.landmark[5]

                

              

               
                

                #print(f"{angle_finger(forehead.x, forehead.y, chin.x, chin.y,chin.x, 0)}")
                #print(f"{distance(index.x, lowerright_jaw.x, index.y, lowerright_jaw.y)}")
                #print(f"{angle_finger(index.x, index.y, wrist.x, wrist.y, wrist.x, 0)}")
                #print(f"{angle_finger(index.x, index.y, index_base.x, index_base.y, thumb.x, thumb.y)}")
            

            

                print(f"{angle_finger(index, wrist)}")

                print("I'm detecting...")

                
                if 7 <= angle_finger(forehead, chin) and 0 <= distance(index, lowerright_jaw, forehead, chin) <= 0.2 and 5 <=angle_finger(index, wrist) <= 15 and  angle_finger(index, index_base) < 10:
                    print("NINO")
                                    
                elif 3 <= angle_finger(forehead, chin) :
                        print("Trying to do a Nino Pose?")

                
                elif 0.13 <= distance(mouth_down, mouth_top, forehead, chin) and (0.35 <= distance(thumb, index, index, wrist) <= 0.45) and (0 <= angle_finger(index, wrist) <= 10):
                    print("MIKU NAKANO")
                
                elif (0.35 <= distance(thumb, index, index, wrist) ) and angle_finger(index, wrist) <= 20:
                    print("Trying to do a Miku Pose?")
                               

                elif distance(ring.x ,mouth_right.x, ring.y, mouth_right.y) <= 0.03 and 0.015 <= distance(mouth_top.x, mouth_down.x, mouth_top.y, mouth_down.y) <= 0.03 and 0.1 <= distance(mouth_top_right.x, left_y_cheek.x, mouth_top_right.y, left_y_cheek.y) <= 0.15 and 60 <= angle_finger(ring.x, ring.y, wrist.x, wrist.y,wrist.x, 0) <= 65:
                    print("YOTSUBA")
                
                elif distance(ring.x ,mouth_right.x, ring.y, mouth_right.y) <= 0.1 :
                    print("Trying to do a Yotsuba Pose?")



                
                #print(f"{abs(ring.x, 3) - mouth_right.x,3))}")

                #print(f"{abs(index.x, 3) - lowerright_jaw.x, 3))}")
                print(2*"")
               
    

                
    cv2.imshow("The Quintessential Quintuplets Pose Project", frame)
    
    #pygame.draw.line(screen, (255,255,255), (wrist.x*100, wrist.y*100), (wrist.x*100, 0))
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
    
    

camera.release()
cv2.destroyAllWindows()
