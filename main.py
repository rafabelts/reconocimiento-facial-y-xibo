import cv2
from camera import get_camera
import dlib
import face_recognition

cam_available = get_camera()
face_detector = dlib.get_frontal_face_detector()


while True: 
    ret, frame = cam_available.read()
    
    if not ret:
        break
        
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector(gray)

    if len(faces) > 0:
        face_landmarks_list = face_recognition.face_landmarks(frame)

        if face_landmarks_list:
            landmarks = face_landmarks_list[0]
            nose_bridge = landmarks['nose_bridge']
            chin = landmarks['chin']

            face_width = abs(chin[0][0] - chin[-1][0])
            face_height = abs(nose_bridge[-1][1] - chin[8][1])
            aspect_ratio = face_width / face_height

            if 0.8 < aspect_ratio < 1.2:
                print(True)

    cv2.imshow('Camera', frame)

    k = cv2.waitKey(1)

    if k == ord('q') or k == 27:
        break

cam_available.release()
cv2.destroyAllWindows()
