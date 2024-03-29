import cv2
import HandDetectionModule as HDM


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

    detector = HDM.HandDetection()

    while True:
        success, image = cap.read()

        if not success:
            print("Error reading frame from webcam")
            break

        # Pass image to the `find_hands` method for processing
        image = detector.find_hands(image)

        image = detector.show_fps(image)

        # print hand landmark to terminal
        list_of_lm, bbox, image = detector.find_position(image, 0, False)

        if len(list_of_lm):
            detector.fingers_up()

        image = detector.volume_controller(image)

        image = detector.brightness_controller(image)

        # Display the image
        cv2.imshow("Image", image)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
