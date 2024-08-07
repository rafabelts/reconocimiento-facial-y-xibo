import cv2
import numpy as np
from filter import filter
import time
from xibo import reloadContent

def process_frame(
        camera, 
        camera_index, 
        face_cascade, 
        previous_faces, 
        max_faces_to_track,
        min_detection_stability):
    ret, frame = camera.read()
    if not ret:
        print(f"Failed to read frame from camera {camera_index}")
        return None, previous_faces

    frame_2_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(frame_2_gray, 
                                          scaleFactor=1.2, 
                                          minNeighbors=6, 
                                          minSize=(30, 30),
                                          maxSize=(200, 200))
    
    stable_faces = filter(previous_faces, faces, max_faces_to_track, min_detection_stability)

    for (x, y, w, h) in stable_faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    return frame, stable_faces

def detectedFace(stable_faces, face_detection_start_time):
    current_time = time.time()

    # Iteramos entre las caras detectadas
    for i, face in enumerate(stable_faces):
        # Si el indice no se encuentra en los tiempos inicalizamos un tiempo
        if i not in face_detection_start_time:
            face_detection_start_time[i] = time.time()

        # Si ya se encuentra calculamos el tiempo q lleva detectado el rostro
        else:
            time_detected = current_time - face_detection_start_time[i]

            # Si lleva de 3 segundos en adelante se manda un mensaje y se reinicia para la prox deteccion
            if time_detected >= 3:
                print("Pasaron 3 segundos")
                reloadContent('4')
                # Si una de las caras se detecta por 3 segundos se reinician los demas tiempos
                for i in list(face_detection_start_time.keys()):
                    face_detection_start_time[i] = time.time()  
                time.sleep(15)

    # Se eliminan las caras que ya no estan siendo detectadas
    detected_faces = set(range(len(stable_faces)))
    for i in list(face_detection_start_time.keys()):
        if i not in detected_faces:
            del face_detection_start_time[i]
