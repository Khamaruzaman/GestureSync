import time
import cv2
import mediapipe as mp


class HandDetection:
    def __init__(self, mode=False, max_hands=2, model_complexity=1,
                 detection_confidence=0.7, tracking_confidence=0.5):
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

    def find_hands(self, image, draw=True):
        # Convert the image to RGB format
        image_in_rgb_format = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image with MediaPipe hands detection
        results = self.hands.process(image_in_rgb_format)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # print hand landmark position in to terminal
                for ID, LM in enumerate(hand_landmarks.landmark):
                    # print(id, LM)
                    h, w, c = image.shape
                    cx, cy = int(LM.x * h), int(LM.y * w)
                    print(ID, "-", cx, cy)

                if draw:
                    self.mp_drawing.draw_landmarks(image, hand_landmarks,
                                                   self.mp_hands.HAND_CONNECTIONS)

        # Display the image
        cv2.imshow("Image", image)

        return image


def main():
    previous_time = 0

    # Set webcam width and height for desired resolution
    webcam_width, webcam_height = 640, 480

    cap = cv2.VideoCapture(0)  # Use 0 for default webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)

    detector = HandDetection()

    while True:
        success, image = cap.read()

        # Pass image to the `find_hands` method for processing
        image = detector.find_hands(image)

        # Calculate FPS (frames per second)
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        # Display FPS on the image (consider using a more reliable method)
        cv2.putText(image, "FPS: " + str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
