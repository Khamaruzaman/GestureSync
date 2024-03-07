import time
import cv2
# import mediapipe as mp
import HandDetectionModule as HDM


def main():
    previous_time = 0

    # Set webcam width and height for desired resolution
    webcam_width, webcam_height = 640, 480

    cap = cv2.VideoCapture(0)  # Use 0 for default webcam
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)

    detector = HDM.HandDetection()

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

        # print hand landmark to terminal
        list_of_lm = detector.locate_hands(image, 0, True)
        if len(list_of_lm):
            # can choose a certain landmark
            print(list_of_lm[4])

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
