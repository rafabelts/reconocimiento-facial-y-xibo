import numpy as np
import cv2


def get_camera():
    cam = ''

    for i in range(8):
        cap = cv2.VideoCapture(i)
        if cap is None or not cap.isOpened():
            print(f"No se encontró ninguna camara en el puerto: {i}")
        else:
            cam = i
            break

        cap.release()
    
    cam_available = cv2.VideoCapture(cam)

    return cam_available
