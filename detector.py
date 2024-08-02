import cv2
import numpy as np
from camera import get_camera
from filter import filter

def detector():
    camera = get_camera()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    

    # Parametros para el smoothing de datos de caras detectadas
    previous_faces = []
    max_faces_to_track = 5
    min_detection_stability = 5

    while True:
        ret, frame = camera.read()

        if not ret:
            break

        frame_2_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        faces = face_cascade.detectMultiScale(frame_2_gray, 
                                              scaleFactor=1.2, 
                                              minNeighbors=6, 
                                              minSize=(30, 30),
                                              maxSize=(200, 200),
                                              )
        face_detected = False
        stable_faces = filter(previous_faces, faces, max_faces_to_track, min_detection_stability)

        for(x, y, w, h) in stable_faces:
            face_detected = True
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            print(face_detected)

        if not face_detected:
            print(False)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    camera.release()
    cv2.destroyAllWindows()
