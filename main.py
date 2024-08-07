import cv2
import numpy as np
from filter import filter
from camera import get_cameras
from detector import process_frame, detectedFace

def main():
    running_program = True
    while running_program:
        try:
            cameras = get_cameras()
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            if not cameras:
                raise Exception('No cameras found')

            # Parametros para el smoothing de datos de caras detectadas
            previous_faces = { camera_index: [] for camera_index, _ in cameras } 
            max_faces_to_track = 3 
            min_detection_stability = 3
            face_detection_start_time = {}
            detection_pause_time = 15  # Pausa de 5 segundos después de detectar un rostro por 3 segundos
            detection_enabled_time = 0  # Inicialmente la detección está habilitada

            while True:
                for camera_index, camera in cameras:
                    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
                    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
           
                    frame, stable_faces = process_frame(
                        camera,
                        camera_index,
                        face_cascade,
                        previous_faces[camera_index],
                        max_faces_to_track,
                        min_detection_stability
                    )

                    detectedFace(stable_faces, face_detection_start_time, detection_pause_time, detection_enabled_time)

                    if frame is not None:
                        cv2.imshow(f'Camera {camera_index}', frame)
        
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    running_program = False
                    break

            for _, camera in cameras:
                camera.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error: {e}. Searching again for cameras...")

if __name__ == "__main__":
    main()
