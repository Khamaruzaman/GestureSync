import time
import cv2
import mediapipe as mp


class Handdetection:
    def __init__(self, mode=False, max_hands=2, model_comp=1, detection_conf=0.7, tracking_conf=0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.modelComp = model_comp
        self.detectionConf = detection_conf
        self.trackingConf = tracking_conf

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(self.mode, self.maxHands, self.modelComp, self.detectionConf,
                                         self.trackingConf)
        self.mp_drawing = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        # Convert the image to RGB
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the image with Mediapipe hand detection
        results = self.hands.process(rgb_image)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for ID, lm in enumerate(hand_landmarks.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * h), int(lm.y * w)
                    print(ID, "-", cx, cy)
                if draw:
                    self.mp_drawing.draw_landmarks(img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        # Display the image
        cv2.imshow("Image", img)

        return img


def main():
    ptime = 0

    wcam, hcam = 640, 480

    cap = cv2.VideoCapture(0)  # Use 0 instead of 1 for the default webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, wcam)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, hcam)

    detector = Handdetection()

    while True:
        success, img = cap.read()

        img = detector.find_hands(img)

        # display fps
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img, 'FPS: ' + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

