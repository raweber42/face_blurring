import cv2
import mediapipe as mp
import numpy as np
from facial_landmarks import FaceLandmarks
import config

def apply_blur(video_path, resize_factor):

  face_landmarks = FaceLandmarks()
  capture = cv2.VideoCapture(video_path)
  frame_width = int(capture.get(3))
  frame_height = int(capture.get(4))
  fps= int(capture.get(cv2.CAP_PROP_FPS))

  while not config.stream_stopped:
    success, frame = capture.read()
    if not success:
      break

    frame = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor)
    
    try:
      landmarks = face_landmarks.get_facial_landmarks(frame)
    except Exception:
      frame = render_without_blurred_face(frame)
    else: 
      convexhull = cv2.convexHull(landmarks)
      frame = render_with_blurred_face(frame, convexhull)

    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
  capture.release()
  cv2.destroyAllWindows()


def render_with_blurred_face(frame, convexhull):
  
  height, width, _ = frame.shape
  mask = np.zeros((height, width), np.uint8)
  cv2.fillConvexPoly(mask, convexhull, 255)
  
  frame_copy = frame.copy()
  frame_copy = cv2.blur(frame_copy, (config.blur_level, config.blur_level))
  face_extracted = cv2.bitwise_and(frame_copy, frame_copy, mask=mask)

  background_mask = cv2.bitwise_not(mask)
  background = cv2.bitwise_and(frame, frame, mask=background_mask)

  frame_with_blurred_face = cv2.add(background, face_extracted)
  frame_with_blurred_face, buffer = cv2.imencode('.jpg', frame_with_blurred_face)
  frame = buffer.tobytes()
  return frame


def render_without_blurred_face(frame):
  
  ret, buffer = cv2.imencode('.jpg', frame)
  frame = buffer.tobytes()
  return frame

  
# TODO: How to do sound?
# TODO: How to handle multiple faces?
