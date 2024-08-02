import numpy as np

def filter(previous_faces, faces, max_faces_to_track, min_detection_stability):
    previous_faces.append(faces)
    if len(previous_faces) > max_faces_to_track:
        previous_faces.pop(0)

    stable_faces = []
    for face in faces:
        if sum(1 for frame_faces in previous_faces 
                if any(np.linalg.norm(np.array(face[:2]) - np.array(f[:2])) < 20 for f in frame_faces)
            ) >= min_detection_stability:
            stable_faces.append(face)

    return stable_faces


