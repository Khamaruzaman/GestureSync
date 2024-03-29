import math
import time
import cv2
import mediapipe as mp
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class HandDetection:
    def __init__(self, mode=False, max_hands=2, model_complexity=1,
                 detection_confidence=0.7, tracking_confidence=0.5):
        self.previous_time = 0
        self.current_time = None
        self.list_of_lm = None
        self.results = None
        self.tipIds = [4, 8, 12, 16, 20]
        self.mode = mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.max_hands,
                                         self.model_complexity, self.detection_confidence,
                                         self.tracking_confidence)
        self.mp_drawing = mp.solutions.drawing_utils
        self.bbox = []
        self.fingers = None

    def find_hands(self, image, draw=True):
        # Convert the image to RGB format
        image_in_rgb_format = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe hands detection
        self.results = self.hands.process(image_in_rgb_format)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(image, hand_landmarks,
                                                   self.mp_hands.HAND_CONNECTIONS)

        return image

    def find_position(self, image, hand_no=0, draw=True):
        list_x = []
        list_y = []

        self.list_of_lm = []
        if self.results.multi_hand_landmarks:
            # select a hand
            my_hand = self.results.multi_hand_landmarks[hand_no]
            # store hand landmark position in to a list
            for ID, LM in enumerate(my_hand.landmark):
                h, w, c = image.shape
                cx, cy = int(LM.x * w), int(LM.y * h)
                list_x.append(cx)
                list_y.append(cy)
                self.list_of_lm.append([ID, cx, cy])

                # highlight the hand
                if draw:
                    cv2.circle(image, (cx, cy), 5, (255, 0, 255), 1)
            x_min, x_max = min(list_x), max(list_x)
            y_min, y_max = min(list_y), max(list_y)
            self.bbox = [x_min, y_min, x_max, y_max]
            if draw:
                cv2.rectangle(image, (self.bbox[0] - 10, self.bbox[1] - 10), (self.bbox[2] + 10, self.bbox[3] + 10),
                              (0, 255, 0), 2)
        return self.list_of_lm, self.bbox, image

    def fingers_up(self):
        self.fingers = []
        # Thumb
        if self.list_of_lm[self.tipIds[0]][1] > self.list_of_lm[self.tipIds[0] - 1][1]:
            self.fingers.append(1)
        else:
            self.fingers.append(0)
        # 4 Fingers
        for ID in range(1, 5):
            if self.list_of_lm[self.tipIds[ID]][2] < self.list_of_lm[self.tipIds[ID] - 2][2]:
                self.fingers.append(1)
            else:
                self.fingers.append(0)
        return self.fingers

    def show_fps(self, image):
        # Calculate FPS (frames per second)
        self.current_time = time.time()
        fps = 1 / (self.current_time - self.previous_time)
        self.previous_time = self.current_time

        # Display FPS on image (properly indented)
        cv2.putText(image, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        return image

    def find_distance(self, image, point_1, point_2, draw=True):

        x1, y1 = self.list_of_lm[point_1][1], self.list_of_lm[point_1][2]
        x2, y2 = self.list_of_lm[point_2][1], self.list_of_lm[point_2][2]

        # find center of line and colour it
        cx, cy = (x2 + x1) // 2, (y2 + y1) // 2

        if draw:
            cv2.circle(image, (x1, y1), 5, (255, 0, 255), 5, cv2.FILLED)  # colour thumb fingertip
            cv2.circle(image, (x2, y2), 5, (255, 0, 255), 5, cv2.FILLED)  # colour index fingertip
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 0), 3)  # draw line btw the points
            cv2.circle(image, (cx, cy), 5, (255, 0, 255), 5, cv2.FILLED)

        # distance btw the two points
        distance = math.hypot(x1 - x2, y1 - y2)

        return image, distance, [x1, y1, x2, y2, cx, cy]

    def volume_controller(self, image, draw=True):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)

        if len(self.list_of_lm):

            # do following if finger 2,3 is down and 4 is up
            if self.fingers[4] and not (self.fingers[2] and self.fingers[3]):
                # filter based on size
                area = ((self.bbox[2] - self.bbox[0]) * (self.bbox[3] - self.bbox[1])) // 100

                if 150 < area < 800:

                    # draw line btw thump and index, find distance btw them
                    image, distance, line_info = self.find_distance(image, 4, 8, draw=draw)

                    # covert volume
                    vol_bar = np.interp(distance, [50, 180], [400, 150])
                    vol_per = np.interp(distance, [50, 180], [0, 100])

                    # reduce resolution to make smoother
                    smoothness = 10
                    vol_per = round(int(vol_per) / smoothness) * smoothness

                    # set volume
                    volume.SetMasterVolumeLevelScalar(vol_per / 100, None)

                    # drawing
                    if draw:
                        if distance < 50:  # colour center point green/red when distance is min/max
                            cv2.circle(image, (line_info[4], line_info[5]), 5, (0, 255, 0), 5, cv2.FILLED)
                        elif distance >= 180:
                            cv2.circle(image, (line_info[4], line_info[5]), 5, (0, 0, 255), 5, cv2.FILLED)

                        cv2.putText(image, f'{int(vol_per)} %',
                                    (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)  # volume percentage on screen

                        cv2.rectangle(image, (50, 150), (85, 400), (255, 0, 0), 3)  # volume meter on screen
                        cv2.rectangle(image, (50, int(vol_bar)), (85, 400), (255, 0, 0), cv2.FILLED)

                        current_volume = int(volume.GetMasterVolumeLevelScalar() * 100)
                        cv2.putText(image, f'Volume: {current_volume}', (400, 50), cv2.FONT_HERSHEY_PLAIN,
                                    2, (255, 0, 0), 2)

        return image


def main():
    # Set webcam width and height for desired resolution
    webcam_width, webcam_height = 640, 480

    try:
        cap = cv2.VideoCapture(0)  # Use 0 for default webcam
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)
    except Exception as e:
        print("Error opening webcam:", e)
        exit()

    detector = HandDetection()

    while True:
        success, image = cap.read()

        if not success:
            print("Error reading frame from webcam")
            break

        # Pass image to the `find_hands` method for processing
        image = detector.find_hands(image)

        image = detector.show_fps(image)

        # print hand landmark to terminal
        list_of_lm, bbox, image = detector.find_position(image, 0, True)
        if len(list_of_lm):
            # can choose a certain landmark
            # print(list_of_lm[4])
            finger_up = detector.fingers_up()
            fingers = sum(finger_up)
            if len(finger_up):
                print(f'{fingers} are up')

        image = detector.volume_controller(image)

        # Display the image
        cv2.imshow("Image", image)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
