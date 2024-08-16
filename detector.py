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
    
    return frame, np.array(stable_faces, dtype=np.int32)

def detectedFace(stable_faces, face_detection_start_time, last_detected_faces):
    current_time = time.time()
    for i, face in enumerate(stable_faces):
        if i not in face_detection_start_time:
            face_detection_start_time[i] = current_time
            last_detected_faces[i] = {
                'face': np.array(face, dtype=np.int32),
                'face_already_detected': False
            }

        else:
            time_detected = current_time - face_detection_start_time[i]

            if np.array_equal(face, last_detected_faces[i]['face']):
                if time_detected >= 3 and not last_detected_faces[i]['face_already_detected']:
                    print("Pasaron 3 segundos")
                    reloadContent(4)
                    last_detected_faces[i]['face_already_detected'] = True
                else:
                    print(f"Cara {i} detectada continuamente. Pausando por 5 segundos...")
                    time.sleep(5)
                    face_detection_start_time[i] = current_time
            else:
                if time_detected >= 5:
                    face_detection_start_time[i] = current_time
                    last_detected_faces[i]['face_already_detected'] = False
                    last_detected_faces[i]['face'] = np.array(face, dtype=np.int32)

    # Elimina las caras que ya no se detectan
    detected_faces = set(range(len(stable_faces)))
    for i in list(face_detection_start_time.keys()):
        if i not in detected_faces:
            del last_detected_faces[i]
            del face_detection_start_time[i]
