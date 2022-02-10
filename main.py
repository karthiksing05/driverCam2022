import cv2

# Multithreading classes for the camera and the transfer object
from threadedCam import ThreadedCamera
from threadedTransfer import ThreadedTransfer

# My import for constant parameters
from params import *

# Open both cameras
driverCam = ThreadedCamera(DRIVER_CAM) # cv2.VideoCapture(2)
codriverCam =  ThreadedCamera(CO_DRIVER_CAM) # cv2.VideoCapture(0)

transfer = ThreadedTransfer()
transfer.get_dev()

if __name__ == '__main__':

    sendFrame = False

    while True:

        codriverCam.update()
        driverCam.update()

        driverCamFrame = driverCam.grab_frame()
        codriverCamFrame = codriverCam.grab_frame()

        # If cannot catch any frame, break
        if not driverCamFrame.any() or not codriverCamFrame.any():
            continue

        # Preprocessing the frames for faster display times

        scale_percent = 75 # percent of original size

        reWidth = int(codriverCamFrame.shape[1] * scale_percent / 100)
        reHeight = int(codriverCamFrame.shape[0] * scale_percent / 100)
        codriverCamFrame = cv2.resize(codriverCamFrame, (reWidth, reHeight))

        reWidth = int(driverCamFrame.shape[1] * scale_percent / 100)
        reHeight = int(driverCamFrame.shape[0] * scale_percent / 100)
        driverCamFrame = cv2.resize(driverCamFrame, (reWidth, reHeight))

        # Displaying FPS, specific camera locations on screen
        driverFPS = driverCam.get_FPS()
        codriverFPS = codriverCam.get_FPS()

        # text params
        name_coords = (50, 50)
        fps_coords = (50, 100)
        fpsStr = f"FPS: {driverFPS}"

        formattedDriverCamFrame = cv2.putText(
            driverCamFrame, 
            "Driver Cam", 
            name_coords, 
            FONT, 
            FONT_SCALE, 
            TEXT_COLOR, 
            THICKNESS
        )

        formattedCodriverCamFrame = cv2.putText(
            codriverCamFrame, 
            "Codriver Cam", 
            name_coords, 
            FONT, 
            FONT_SCALE, 
            TEXT_COLOR, 
            THICKNESS
        )

        # Putting FPS on screen
        formattedDriverCamFrame = cv2.putText(
            formattedDriverCamFrame, 
            fpsStr, 
            fps_coords, 
            FONT, 
            FONT_SCALE, 
            TEXT_COLOR, 
            THICKNESS
        )

        formattedCodriverCamFrame = cv2.putText(
            formattedCodriverCamFrame, 
            fpsStr, 
            fps_coords, 
            FONT, 
            FONT_SCALE, 
            TEXT_COLOR, 
            THICKNESS
        )

        # Show the frames (testing)
        # cv2.imshow("Driver Camera", formattedDriverCamFrame)
        # cv2.imshow("CoDriver Camera", formattedCodriverCamFrame)

        # Send the frames like a USB Camera would
        if sendFrame:
            sendFrame = False
            transfer.send([driverCamFrame, codriverCamFrame])
        else:
            sendFrame = True

        # Hit "q" to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release and destroy all windows before termination
    cv2.destroyAllWindows()
