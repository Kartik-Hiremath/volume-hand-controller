import cv2
import mediapipe as mp
import numpy as np
import time
import HandTrackingModule as htm
import math
import platform
from subprocess import run

# For Windows, we'll use pycaw but we should only import it if the platform is Windows
try:
    if platform.system() == "Windows":
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        windows = True
    else:
        windows = False
except ImportError:
    windows = False


def set_volume(vol):
    if windows:
        # Windows Volume Control using pycaw
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        # Convert volume percentage to decibels
        dB = np.interp(vol, [0, 100], [-65.25, 0])  # Mapping vol (0-100) to decibels (-65.25 to 0)
        volume.SetMasterVolumeLevel(dB, None)
    else:
        # Mac and Linux volume control
        if platform.system() == "Darwin":  # macOS
            # Use osascript to control volume
            run(["osascript", "-e", f"set volume output volume {vol}"])
        elif platform.system() == "Linux":  # Linux
            # Use amixer to control volume
            run(["amixer", "-D", "pulse", "sset", "Master", f"{vol}%"])


def main():
    wCam, hCam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    cTime, pTime = 0, 0

    detector = htm.handDetector(detectionCon=0.7)  # Using your handTrackingModule

    vol = 0
    volBar, volPer = 400, 0

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList = detector.findPosition(img, handNo=0, draw=False)

        if len(lmList) != 0:
            x1, y1 = lmList[4][1], lmList[4][2]  # Thumb
            x2, y2 = lmList[8][1], lmList[8][2]  # Index finger
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2  # Midpoint between thumb and index

            # Draw circles and line between thumb and index finger
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

            # Calculate the distance between the thumb and index finger
            length = math.hypot(x2 - x1, y2 - y1)
            if length < 40:
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
            elif length > 180:
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

            # Interpolate the volume based on the distance between thumb and index
            vol = np.interp(length, [20, 120], [0, 100])  # Mapping length to volume range (0-100)
            volBar = np.interp(length, [50, 150], [400, 150])  # Mapping length to volume bar height
            volPer = np.interp(length, [50, 150], [0, 100])  # Mapping length to percentage

            # Set the system volume
            set_volume(vol)

        # Drawing the volume bar on screen
        cv2.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, f"Volume: {int(volPer)}%", (0, 450), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)

        # Display the FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f"FPS: {int(fps)}", (0, 40), cv2.FONT_ITALIC, 1, (255, 255, 0), 2)

        # Show the resulting image
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    main()