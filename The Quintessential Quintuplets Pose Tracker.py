import os
import math
import time
import subprocess
import sys
import importlib
import base64
import keyboard
import pyautogui
pyautogui.PAUSE = 0 
#BETA 1.0.2 MB GUYS I FORGOT TO UPDATE THIS PART, I'VE BEEN AT BETA 1.0.0 SINCE SEPTEMBER 1
#DONT MIND THE CAMERA SETTINGS AND SHI I AINT DONE YET WITH THAT I KNOW THEYRE A BROKEN LOOP AND I FOCUSED ON THE REAL DEAL FIRST

#print(f"{sys.executable}")
parent_folder = os.path.dirname(os.path.abspath(__file__))
os.chdir(parent_folder)

mouth_left=left_y_cheek=mouth_top_right= mouth_right= mouth_top= mouth_down= lowerright_jaw= cheek_left= cheek_right= forehead= chin= index= middle= thumb= wrist= ring= ring_mid= index_base= pinky = None

image_folder = os.path.join(parent_folder, "Nakano Sisters")
if sys.version_info.major != 3 or not(9 <=sys.version_info.minor <= 12):
    print(f"Sorry lil bro, your Python version {sys.version_info.major}.{sys.version_info.minor} cannot support the needed modules. Please install Python 3.9 or 3.10 or 3.11 or 3.12 until I patch for the current Python version you are using. Might as well say goodbye to The Quintessential Quintuplets 💔💔")
    sys.exit(1)



def pip_install(module, package):
    print(2*"")
    try:
        return __import__(module)
    except ImportError:
        print("")
        permission = input(f"Permission to install the missing dependency? {package} [Y/N]: ")
        if permission.lower() == 'y':
            print(f"Installing {package} for Python {sys.version_info.major}.{sys.version_info.minor}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package, "--user"],
                    stdout = subprocess.DEVNULL,
                    stderr = subprocess.DEVNULL
                )
            except subprocess.CalledProcessError:
                try:
                    print("Standard install failed. Retrying with user-isolation flags...")
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", package, "--user", "--no-cache-dir"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except subprocess.CalledProcessError:
                    print("CRITCAL: Windows is blocking file access")
                    print("Please restart VS Code /  terminal and try again.")
                    print("")
                    print("If the issue persists, run this manually in Command Prompt:")
                    print(f"pip install {package} --user")
                    sys.exit(1)

            print(f"Finished installing {package}")
            print("")
            
            importlib.invalidate_caches()
            return importlib.import_module(module)

        else:
            print("Suit yourself buddy")
            sys.exit(1)
            

cv2 = pip_install("cv2", "opencv-python")
mediapipe = pip_install("mediapipe", "mediapipe==0.10.21")
pygame = pip_install("pygame", "pygame-ce")
pydub = pip_install("simpleaudio", "simpleaudio-patched")


print(f"Yep you're good to go. Packages:")
print(f"OpenCV2 Version {cv2.__version__}")
print(f"MediaPipe Version {mediapipe.__version__}")

import pygame
import cv2 
import mediapipe as mp
import numpy as np
import io
from pydub import AudioSegment
from pydub.playback import play

#For the out of place mouse thingy
frame_count = 0
even_coord = odd_coord = 0
scroll_state = "Wsg"

def listcameras(max = 10):
    available = []

    for index in range(max):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW) if hasattr(cv2, 'CAP_DSHOW') else cv2.VideoCapture(index)

        if cap.isOpened():
            available.append(index)
            cap.release()
    return available


try:
    from cv2_enumerate_cameras import enumerate_cameras
except ImportError:
    print("OpenCV2 Enumerate Camera Module is not installed. Beginning Installation...")
    pip_install("cv2_enumerate_cameras", "cv2-enumerate-cameras")
    from cv2_enumerate_cameras import enumerate_cameras



print("")
permission = input("Permission to turn on camera? (Don't worry your video will not be collected or saved to a cloud storage. You can even turn off your wifi from this point on) [Y/N]: ")
print("")


if permission.lower() == 'y':
    print("List of Cameras:")
    print("----------------------")
    for i in listcameras():
        print(i,end='')
        if i == 0:
            print(" (Defualt Camera)")
        else:
            print()

    print("")
    camerno = int(input("Which camera number will you use?: "))
    print("")

    camera = cv2.VideoCapture(camerno)
    if not camera.isOpened():
        camera = cv2.VideoCapture(0)
        print("Defaulting to default camera...")
        if not camera.isOpened():
            print("Default Camera not found. Rerouting to different camera")
            camera = cv2.VideoCapture(1)

            if not camera.isOpened():
                indice = input("Please re-input the camera you want to use: ")
elif permission.lower() == 'n':
    print("You'll have no camera tho :(")
else:
    print("buddy u ain't slick")

print(2*"")

mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh

hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence= 0.7)
face = mp_face.FaceMesh(max_num_faces=2, refine_landmarks=True, min_detection_confidence=0.7)
draw = mp.solutions.drawing_utils
drawstyle = mp.solutions.drawing_styles

RefreshRate = pygame.time.Clock()


#Images
try:
    try:
        miku_image = cv2.imread("Nakano Sisters/Miku.jpg")
        mheight, mwidth = miku_image.shape[:2]
        mhopeful_width = 200
        mratio = mhopeful_width/mwidth
        mhopeful_height = int(mheight * mratio)
        mdim = (mhopeful_width, mhopeful_height)
        miku_image = cv2.resize(miku_image, mdim, interpolation=cv2.INTER_AREA)
    except FileNotFoundError:
        print("HOW. HOW COULD YOU BRO. YOU EVIL PIECE OF HUMAN FLESH. HOW COULD U NOT HAVE MIKU'S IMAGE IN YOUR LOCAL DRIVE?? (GET AN IMAGE OF MIKU AND NAME IT 'Miku.jpg')")

    try:
        yotsuba_image = cv2.imread("Nakano Sisters/Yotsuba.jpg")
        yheight, ywidth = yotsuba_image.shape[:2]
        yhopeful_width = 200
        yratio = yhopeful_width/ywidth
        yhopeful_height = int(yheight * yratio)
        ydim = (yhopeful_width, yhopeful_height)
        yotsuba_image = cv2.resize(yotsuba_image, ydim, interpolation=cv2.INTER_AREA)

    except FileNotFoundError:
        print("YO WHY THE HELL IS YOTSUBE MISSING (Required: file named 'Yotsuba.jpg')")


    try:
        nino_image = cv2.imread("Nakano Sisters/Nino.jpg")
        nheight, nwidth = nino_image.shape[:2]
        nhopeful_width = 200
        nratio = nhopeful_width/nwidth
        nhopeful_height = int(nheight * nratio)
        ndim = (nhopeful_width, nhopeful_height)
        nino_image = cv2.resize(nino_image, ndim, interpolation=cv2.INTER_AREA)  


    except:
        print("SON IS REALLY MISSING NINO?? GO GET HER BRO (Required: file named 'Nino.jpg')")


    try:
        itsuki_image = cv2.imread("Nakano Sisters/Itsuki.jpg")
        eatheight, eatwidth = itsuki_image.shape[:2]
        eathopeful_width = 200
        eatratio = eathopeful_width/eatwidth
        eathopeful_height = int(eatheight * eatratio)
        eatdim = (eathopeful_width, eathopeful_height)
        itsuki_image = cv2.resize(itsuki_image, eatdim, interpolation=cv2.INTER_AREA)

    except:
        print("bro. bro. are we deadass rn. You're really missing out on eatsuki?? (Required: file named 'Itsuki.jpg')")


    try:
        ichika_image = cv2.imread("Nakano Sisters/Ichika.jpg")
        icheight, icwidth = ichika_image.shape[:2]
        ichopeful_width = 200
        icratio = ichopeful_width/icwidth
        ichopeful_height = int(icheight * icratio)
        icdim = (ichopeful_width, ichopeful_height)
        ichika_image = cv2.resize(ichika_image, icdim, interpolation=cv2.INTER_AREA)

    except:
        print("*speed dissapointed face* (Required: file named 'Ichika.jpg')")

        
except:
    print("WHHHATTT. HOW THE HELL")

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

newplacex, newplacey = 100,100

def menu(finger, finger2, frame):
    global newplacex, newplacey
    text = "Chud??"
    placex, placey = newplacex, newplacey
    font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
    base_size = 1
    color = (0, 0, 0)
    thickness = 1
    type = cv2.LINE_AA
    #print(f"index: {round(finger.y,2)}")
    #print(f"angle thumb {angle_finger(finger, finger2)}")
    #print(f"distance {distance(index, thumb, wrist, index)}")
    print(f"{thumb.x*w}, {thumb.y*h}")
    print(f"{newplacex}, {newplacey}")
    if distance(index, thumb, wrist, index) <= 0.2 and ((placex - 40) <= (thumb.x*w) <= (placex + 40)) and ((placey - 40) <= (thumb.y*h) <= (placey + 40)):
        newplacex = int(thumb.x*w)
        newplacey = int(thumb.y*h)
        #test run with miku :33 CUZ MIKU IS THE GOAT
        #frame[placey:placey+mheight, placex:placex+mwidth] = miku_image
        
    if 0.15 <= round(finger.y,2) <= 0.25:
        text = "Chud ←"
        if base_size <= 5:
           base_size += 0.01
        color = (20, 20, 20)

        if  round(angle_finger(finger, finger2)) <= 50:
            extras = "*.+*"
            explace = (75,75)
            exfont = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
            exbase_size = 1
            excolor = (120,200,200)
            exthickness = 1
            extype = cv2.LINE_AA
            cv2.putText(frame,extras,explace,exfont,exbase_size,excolor,exthickness,extype)
   
    
    cv2.putText(frame,text,(placex, placey),font,base_size,color,thickness,type)

def unrelated_mouse():
    global frame_count, even_coord, odd_coord, scroll_state
    pyautogui.moveTo(int(index.x*1920), int(index.y*1080))

    frame_count += 1

    if frame_count % 2 == 0:
        even_coord = int(index.y * h)
    elif frame_count % 2 == 1 :
        odd_coord = int(index.y * h) 
    initial_y = index.y*h

    print(f"{even_coord} {odd_coord} {abs(0 - index.y*h)} {abs(h - index.y*h)}")

    if abs(odd_coord - even_coord) >= 10 :
        if ((int(index.y*h) > even_coord) or (int(index.y*h) > odd_coord)):
            pyautogui.scroll(int(2*abs(odd_coord - even_coord)))
        
        elif ((int(index.y*h) < even_coord) or (int(index.y*h) < odd_coord)):
            pyautogui.scroll(int(-2* abs((odd_coord - even_coord))))
    
##DAM U BRO IT TOOK ME A LONG TIME TO FIX THIS




    if distance(index, thumb, wrist, index) <= 0.2:
        pyautogui.click()


def jukebox():
    pygame.init()
    pygame.mixer.init()
    jukebox_folder = "Songs"
    actual_chad = os.path.join(parent_folder, jukebox_folder)
    name = str(input("What song do you wanna play?: "))

    try: 
        for music in os.listdir(actual_chad):
            if name.lower() in music.lower():
                song_dir = os.path.join(actual_chad, music)
                pygame.mixer_music.load(f"Songs/{music}")
                pygame.mixer_music.play()
                print(f"Playing {music}...")
    except FileNotFoundError:
        print("SON WHERE THE HELL IS THE SONGS FOLDER HOW ARE YOU GONNA LISTEN TO PEAK NOW??")
        return

class theposetracker():
    def __init__(self, frame):
        global mid_index, mid_middle, mid_pinky, mid_ring, mouth_left,left_y_cheek,mouth_top_right, mouth_right, mouth_top, mouth_down, lowerright_jaw, cheek_left, cheek_right, forehead, chin, index, middle, thumb, wrist, ring, ring_mid, index_base, pinky
                
        self.frame = cv2.flip(frame, 1)
        self.chud_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.hand_results = hands.process(self.chud_rgb)
        self.face_results = face.process(self.chud_rgb)
        if self.hand_results.multi_hand_landmarks and self.face_results.multi_face_landmarks:
            for hand_landmarks in self.hand_results.multi_hand_landmarks:
                for face_landmarks in self.face_results.multi_face_landmarks:
    
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
    
                    
    
                    index = hand_landmarks.landmark[8]
                    middle = hand_landmarks.landmark[12]
                    thumb = hand_landmarks.landmark[4]
                    wrist = hand_landmarks.landmark[0]
                    ring = hand_landmarks.landmark[16]
                    ring_mid = hand_landmarks.landmark[14]
                    index_base = hand_landmarks.landmark[5]
                    pinky = hand_landmarks.landmark[20] 
                    pinky_base = hand_landmarks.landmark[17]
                    mid_middle = hand_landmarks.landmark[10]
                    mid_ring = hand_landmarks.landmark[14]
                    mid_pinky = hand_landmarks.landmark[18] 
                    mid_index = hand_landmarks.landmark[6]

        

    def posetracker(self, frame):
        if self.hand_results.multi_hand_landmarks and self.face_results.multi_face_landmarks:
            for hand_landmarks in self.hand_results.multi_hand_landmarks:
                for face_landmarks in self.face_results.multi_face_landmarks:
    
        #draw.draw_landmarks(frame,hand_landmarks, mp_hands.HAND_CONNECTIONS, drawstyle.get_default_hand_landmarks_style(), drawstyle.get_default_hand_connections_style())
        #draw.draw_landmarks(image=frame,landmark_list=face_landmarks, connections=mp_face.FACEMESH_TESSELATION, landmark_drawing_spec=None, connection_drawing_spec=drawstyle.get_default_face_mesh_tesselation_style())

                    print()
    
    
    
                    if distance(pinky, mouth_down, forehead, mouth_down) <= 0.35 and 0.01 <= distance(mouth_top, mouth_down, forehead, chin)  and 150 <= angle_finger(ring, mid_ring) and angle_finger(pinky, wrist) <= 5 :
                        print("ITSUKI")
                        frame[50:50+eatheight, 50:50+eatwidth] = itsuki_image
                    elif 170 <= angle_finger(ring, mid_ring) and angle_finger(pinky, wrist) <= 10 and distance(pinky, mouth_down, forehead, mouth_down) <= 1:
                        print("...i don't even have anymore words bro its freaking eatsuki she has one of the most distinct poses...")
    
    
                    elif 0.015 <= distance(mouth_down, mouth_top, forehead, chin) and (0.35 <= distance(thumb, index, index, wrist) <= 0.45) and angle_finger(index, wrist) <= 20 and not(160 <= angle_finger(ring, ring_mid) <= 170) :
                        print("MIKU NAKANO")
                        frame[50:50+mheight, 50:50+mwidth] = miku_image
                        
                                    
                    elif (0.35 <= distance(thumb, index, index, wrist) ) and angle_finger(index, wrist) <= 30 and distance(index, mouth_top, wrist, forehead) <= 0.5 and not(160 <= angle_finger(ring, ring_mid) <= 170) and not(3<=angle_finger(forehead,chin)):
                        print("BUDDY IT AIN'T THAT HARD TO DO MIKU'S POSE ITS A FRIGGING SHOCKED FACE")
                      
    
                    elif 0.42 <= distance(mouth_left, mouth_right, cheek_left, cheek_right) and distance(ring, mouth_right, ring, wrist) <= 0.3 and 0.05 <= distance(mouth_top, mouth_down, ring, wrist)  and 0.1 <= distance(mouth_top_right, left_y_cheek, ring, wrist) <= 0.55 and 55 <= angle_finger(ring, wrist):
                        print("YOTSUBA")
                        frame[50:50+yheight, 50:50+ywidth] = yotsuba_image
    
                    elif distance(ring,mouth_right, ring, wrist) <= 0.1 and 50 <= angle_finger(ring, wrist):
                        print("HOW. HOW ARE YOU GENUINELY TWEAKING WITH YOTSUBA'S POSE?? ")
    
                    
                    elif 3 <= angle_finger(forehead, chin) and distance(index, lowerright_jaw, forehead, chin) <= 1 and 3 <=angle_finger(index, wrist) and 0.50 <= distance(index, thumb, wrist, index) <= 0.67 and 155 <= angle_finger(middle, mid_middle) <= 180 and 150 <= angle_finger(ring, mid_ring) <= 180 and 150 <= angle_finger(pinky, mid_pinky) <= 180:
                        print("NINO")
                        frame[50:50+nheight, 50:50+nwidth] = nino_image


                    elif 75 <= angle_finger(middle, wrist) <= 85 and 50 <=angle_finger(thumb, index) <= 70 and angle_finger(forehead, chin) <= 7 and 0.01 <= distance(mouth_down, mouth_top, forehead, chin) <= 0.03 and 0.30 <=  distance(middle, index, wrist, thumb) <= 0.45 and 83 <= angle_finger(index, index_base) <= 100 and distance(thumb, mouth_down, wrist, forehead) <= 0.2 and 0.50 <= distance(thumb, index, index, wrist) <= 0.85:
                        print("ICHIKA")
                        frame[50:50+icheight, 50:50+icwidth] = ichika_image

                    elif 73 <= angle_finger(middle, wrist) <= 87 and 55 <=angle_finger(thumb, index) and 3 <= angle_finger(forehead, chin) <= 10:
                        print("BUDDY HOLLY IT AINT THAT HARD TO DO ICHIKA'S")

                    elif 3 <= angle_finger(forehead, chin) :
                        print("okay ye to be fair, nino's is pretty hard 🤷‍♂️")

                    #ITSUKI debugging

    def itsuki_debug(self):
        if self.hand_results.multi_hand_landmarks and self.face_results.multi_face_landmarks:
            for hand_landmarks in self.hand_results.multi_hand_landmarks:
                for face_landmarks in self.face_results.multi_face_landmarks:
                    print(f"Pinky to mouth: {distance(pinky, mouth_down, forehead, mouth_down)}")
                    print(f"Mouth is {distance(mouth_top, mouth_down, forehead, chin)} wide")
                    print(f"{angle_finger(ring, ring_mid)}")
    
                    #MIKU debugging
    def miku_debug(self):
        if self.hand_results.multi_hand_landmarks and self.face_results.multi_face_landmarks:
            for hand_landmarks in self.hand_results.multi_hand_landmarks:
                for face_landmarks in self.face_results.multi_face_landmarks:        
                    print(f" Mouth is{distance(mouth_down, mouth_top, forehead, chin)} wide")
                    print(f"Distance from thumb to index: {distance(thumb, index, index, wrist)}")
                    print(f"Tilt of index: {angle_finger(index, wrist)}")
                    print(f"Tilt of ring finger: {angle_finger(ring, ring_mid)}")
                
    
                    #Yotsuba Debugging
    def yotsuba_debug(self):
        if self.hand_results.multi_hand_landmarks and self.face_results.multi_face_landmarks:
            for hand_landmarks in self.hand_results.multi_hand_landmarks:
                for face_landmarks in self.face_results.multi_face_landmarks:
                    print(f"Distance between left and right of mouth: {distance(mouth_left, mouth_right, cheek_left, cheek_right)}")
                    print(f"Distance between ring and mouth right: {distance(ring, mouth_right, ring, wrist)}")
                    print(f"Mouth is {distance(mouth_top, mouth_down, ring, wrist)} wide")
                    print(f"Distance between top right corner of mouth to left cheek: {distance(mouth_top_right, left_y_cheek, ring, wrist)}")
                    print(f"Tilt of ring finger: {angle_finger(ring, wrist)}")
    
                    #Nino debugging
    def nino_debug(self):
        if self.hand_results.multi_hand_landmarks and self.face_results.multi_face_landmarks:
            for hand_landmarks in self.hand_results.multi_hand_landmarks:
                for face_landmarks in self.face_results.multi_face_landmarks:                        
                    print(f"Tilt of forehead{angle_finger(forehead, chin)}")
                    print(f"Distance between index and lower right jaw: {distance(index, lowerright_jaw, forehead, chin)}")
                    print(f"Tilt of index{angle_finger(index, wrist)}")
                    print(f"Distance between index and thumb {distance(index, thumb, wrist, index)}")
                    print(f"Angle of bent index {angle_finger(index, mid_index)}")
                    print(f"Angle of middle bent {angle_finger(middle, mid_middle)}")
                    print(f"Angle of ring bent {angle_finger(ring, mid_ring)}")
                    print(f"Angle of pinky bent {angle_finger(pinky, mid_pinky)}")
    
    def ichika_debug(self):
        if self.hand_results.multi_hand_landmarks and self.face_results.multi_face_landmarks:
            for hand_landmarks in self.hand_results.multi_hand_landmarks:
                for face_landmarks in self.face_results.multi_face_landmarks:        
        #i just gotta figure out the wrist angle, the thumb to thumb base joint to index angle, 
        # the face to neck angle, the gap between the lips, distance, between index and middle fingers, 
        # angle of index-index base joint, and middle finger oh and finger to mouth distance and thumb to index distance
                    print(f"Wrist Angle tilt: {angle_finger(middle, wrist)}")
                    print(f"Thumb to Index angle: {angle_finger(thumb, index)}")
                    print(f"Chin to Forehead: {angle_finger(forehead, chin)}")
                    print(f"Mouth is {distance(mouth_down, mouth_top, forehead, chin)} wide")
                    print(f"Middle to index is {distance(middle, index, wrist, thumb)}")
                    print(f"Angle of index finger {angle_finger(index, index_base)}")
                    print(f"Distance between thumb and mouth {distance(thumb, mouth_down, wrist, forehead)}")
                    print(f"Distance between Thumb to index {distance(thumb, index, index, wrist)}")
jukebox()



mp_selfie = mp.solutions.selfie_segmentation
selfie = mp_selfie.SelfieSegmentation(model_selection=0)

#cv2.namedWindow("The Quintessential Quintuplets Pose Project", cv2.WINDOW_NORMAL)
#cv2.resizeWindow("The Quintessential Quintuplets Pose Project", 800, 600)
h, w, c = 0, 0, 0
while camera.isOpened():

    RefreshRate.tick(60)
    success, frame = camera.read()
    if not success:
        print("whadahell")
        continue        
    
    frame = cv2.flip(frame, 1)
    chud_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = selfie.process(chud_rgb)
    you = results.segmentation_mask
    condition = np.stack((you,) * 3, axis=-1) > 0.5
    bg = np.zeros(frame.shape, dtype=np.uint8) 
    output_frame = np.where(condition, frame, bg)

    chud_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    hand_results = hands.process(chud_rgb)
    face_results = face.process(chud_rgb)

    if hand_results.multi_hand_landmarks and face_results.multi_face_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:  
                    h, w, c = frame.shape
                    
                    main = theposetracker(frame)
                    #main.posetracker(frame)


                    #menu(index, pinky, frame)
                    unrelated_mouse()
                
               
    
    
                
    cv2.imshow("The Quintessential Quintuplets Pose Project", frame)
    
    #pygame.draw.line(screen, (255,255,255), (wrist.x*100, wrist.y*100), (wrist.x*100, 0))
    if cv2.waitKey(1) & 0XFF == ord('q'):
        break
    
    

camera.release()
cv2.destroyAllWindows()
