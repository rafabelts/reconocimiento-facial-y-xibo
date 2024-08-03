import cv2

def get_cameras():
    ports = []
    cameras = []
    for i in range(8):
        cap = cv2.VideoCapture(i)
        if cap is  None or not cap.isOpened():
           print(f"No se encontró ninguna camara en el puerto: {i}")

        else:
            ports.append(i)
        cap.release()

    for port in ports:
        cameras.append((port, cv2.VideoCapture(port)))

    return cameras 
