import time

import cv2
import mediapipe as mp
import autopy

wcam, hcam = 640, 680
cap = cv2.VideoCapture(0)  # Use 0 instead of 1 for the default webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, wcam)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hcam)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Set the offset for the camera window placement
screen_width, screen_height = autopy.screen.size()
offset_x = screen_width - wcam

ptime=0
ctime=0

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        success, img = cap.read()

        # Convert the image to RGB
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the image with Mediapipe hand detection
        results = hands.process(rgb_image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # display fps
        ctime= time.time()
        fps= 1/(ctime-ptime)
        ptime=ctime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),4)

        # Display the image
        cv2.imshow("Image", img)

        # Move the mouse cursor to the right side of the screen
        # autopy.mouse.move(offset_x, 0)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

cap.release()
cv2.destroyAllWindows()
