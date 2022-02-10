import cv2

# Multithreading class!!!
from threadedCam import ThreadedCamera

# My import for constant parameters
from params import *

# Open both cameras
codriverCam =  ThreadedCamera(CO_DRIVER_CAM) # cv2.VideoCapture(0)

if __name__ == '__main__':
    while True:

        codriverCam.update()
        codriverCamFrame = codriverCam.grab_frame()

        # If cannot catch any frame, break
        if codriverCamFrame.any():
            continue

        # Preprocessing the frames for faster display times

        scale_percent = 75 # percent of original size

        reWidth = int(codriverCamFrame.shape[1] * scale_percent / 100)
        reHeight = int(codriverCamFrame.shape[0] * scale_percent / 100)
        codriverCamFrame = cv2.resize(codriverCamFrame, (reWidth, reHeight))

        # Displaying FPS, specific camera locations on screen
        # driverFPS = driverCam.get_FPS()
        codriverFPS = codriverCam.get_FPS()

        # text params
        name_coords = (50, 50)
        fps_coords = (50, 100)

        formattedCodriverCamFrame = cv2.putText(
            codriverCamFrame, 
            "Codriver Cam", 
            name_coords, 
            FONT, 
            FONT_SCALE, 
            TEXT_COLOR, 
            THICKNESS
        )

        formattedCodriverCamFrame = cv2.putText(
            formattedCodriverCamFrame, 
            f"FPS: {codriverFPS}", 
            name_coords, 
            FONT, 
            FONT_SCALE, 
            TEXT_COLOR, 
            THICKNESS
        )

        # Show the frames
        # cv2.imshow("Driver Camera", formattedDriverCamFrame)
        cv2.imshow("CoDriver Camera", formattedCodriverCamFrame)

        # Hit "q" to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release and destroy all windows before termination
    cv2.destroyAllWindows()
