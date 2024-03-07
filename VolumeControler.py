import cv2
import time

import numpy as np

import HandDetectionModule as HDM
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


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

    dectector = HDM.HandDetection()

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    print(volume.GetVolumeRange())
    volume_range = volume.GetVolumeRange()
    max_range = volume_range[1]
    min_range = volume_range[0]

    previous_time = 0

    vol_bar = 400
    vol_per = 0

    while True:
        success, image = cap.read()

        if not success:
            print("Error reading frame from webcam")
            break

        # Pass image to the `find_hands` method for processing
        image = dectector.find_hands(image)

        # gets landmark location of each point
        lm_list = dectector.locate_hands(image, draw=False)

        # Calculate FPS (frames per second)
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        # Display FPS on image (properly indented)
        cv2.putText(image, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        if len(lm_list):
            # print(lm_list[4], lm_list[8])  # print hand landmark of thumb and index finger to terminal
            x1, y1 = lm_list[4][1], lm_list[4][2]
            x2, y2 = lm_list[8][1], lm_list[8][2]

            cv2.circle(image, (x1, y1), 5, (255, 0, 255), 5, cv2.FILLED)  # colour thumb fingertip
            cv2.circle(image, (x2, y2), 5, (255, 0, 255), 5, cv2.FILLED)  # colour index fingertip
            cv2.line(image, (x1, y1), (x2, y2), (0, 0, 0), 3)  # draw line btw the points

            # find center of line and colour it
            cx, cy = (x2 + x1) // 2, (y2 + y1) // 2
            cv2.circle(image, (cx, cy), 5, (255, 0, 255), 5, cv2.FILLED)

            # distance btw the two points
            distance = math.hypot(x1 - x2, y1 - y2)
            print(distance)

            # colour center point green/red when distance is min/max
            if distance < 50:
                cv2.circle(image, (cx, cy), 5, (0, 255, 0), 5, cv2.FILLED)
            elif distance >= 250:
                cv2.circle(image, (cx, cy), 5, (0, 0, 255), 5, cv2.FILLED)

            # set volume according to distance
            vol = np.interp(distance, [50, 250], [min_range, max_range])
            volume.SetMasterVolumeLevel(vol, None)

            vol_bar = np.interp(distance, [50, 250], [400, 150])
            vol_per = np.interp(distance, [50, 250], [0, 100])

        # volume percentage on screen
        cv2.putText(image, f'{int(vol_per)} %', (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # volume meter on screen
        cv2.rectangle(image, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(image, (50, int(vol_bar)), (85, 400), (255, 0, 0), cv2.FILLED)

        # Display the image
        cv2.imshow("Image", image)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
