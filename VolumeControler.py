import cv2
import numpy as np
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import HandDetectionModule as HDM


def main():
    # Set webcam width and height
    webcam_width, webcam_height = 640, 480

    try:
        cap = cv2.VideoCapture(0)  # Use 0 for default webcam
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)
    except Exception as e:
        print("Error opening webcam:", e)
        exit()

    detector = HDM.HandDetection(max_hands=1)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)

    while True:
        success, image = cap.read()

        if not success:
            print("Error reading frame from webcam")
            break

        # Pass image to the `find_hands` method for processing
        image = detector.find_hands(image)

        # gets landmark location of each point
        list_of_lm, bbox, image = detector.find_position(image, draw=True)

        # frame rate
        image = detector.show_fps(image)

        if len(list_of_lm):
            # filter based on size
            area = ((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])) // 100
            # print(area)
            if 150 < area < 800:

                # draw line btw thump and index, find distance btw them
                image, distance, line_info = detector.find_distance(image, 4, 8)

                # covert volume
                vol_bar = np.interp(distance, [50, 180], [400, 150])
                vol_per = np.interp(distance, [50, 180], [0, 100])

                # reduce resolution to make smoother
                smoothness = 10
                vol_per = round(int(vol_per) / smoothness) * smoothness

                # check finger up
                fingers = detector.fingers_up()

                # if pinky up, set volume
                if not fingers[4] and (fingers[2] and fingers[3]):
                    volume.SetMasterVolumeLevelScalar(vol_per / 100, None)

                # drawing
                if distance < 50:  # colour center point green/red when distance is min/max
                    cv2.circle(image, (line_info[4], line_info[5]), 5, (0, 255, 0), 5, cv2.FILLED)
                elif distance >= 180:
                    cv2.circle(image, (line_info[4], line_info[5]), 5, (0, 0, 255), 5, cv2.FILLED)

                cv2.putText(image, f'{int(vol_per)} %',
                            (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)  # volume percentage on screen

                cv2.rectangle(image, (50, 150), (85, 400), (255, 0, 0), 3)  # volume meter on screen
                cv2.rectangle(image, (50, int(vol_bar)), (85, 400), (255, 0, 0), cv2.FILLED)

                current_volume = int(volume.GetMasterVolumeLevelScalar() * 100)
                cv2.putText(image, f'Volume: {current_volume}', (400, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Display the image
        cv2.imshow("GestureSync", image)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()
