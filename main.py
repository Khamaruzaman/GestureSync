import HandDetectionModule as hdm
import cv2


def main():
    # Set webcam width and height for desired resolution
    webcam_width, webcam_height = 1200, 720

    try:
        cap = cv2.VideoCapture(0)  # Use 0 for default webcam
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)
    except Exception as e:
        print("Error opening webcam:", e)
        exit()

    detector = hdm.HandDetection()

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
            detector.fingers_up()

        image = detector.mode_select(image, webcam_width)
        if detector.mode == 0:
            image = detector.volume_controller(image)
        elif detector.mode == 1:
            image = detector.brightness_controller(image)
        elif detector.mode == 2:
            # cv2.circle(image, (webcam_width // 2, webcam_height // 2), 10, (255, 0, 0))
            image = detector.cursor_move(image, webcam_width, webcam_height)
            detector.click()
            detector.scroll()
            # detector.click_and_drag()
        elif detector.mode == 3:
            image = detector.hand_keyboard(image)

        # Display the image
        cv2.imshow("Image", image)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
