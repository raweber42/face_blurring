# https://pysource.com/blur-faces-in-real-time-with-opencv-mediapipe-and-python
import cv2
import mediapipe as mp
import numpy as np
from facial_landmarks import FaceLandmarks

     
def replace_with_blurred_face(frame, convexhull, blur_level):
  
  height, width, _ = frame.shape
  mask = np.zeros((height, width), np.uint8)
  cv2.fillConvexPoly(mask, convexhull, 255)
  
  frame_copy = frame.copy()
  frame_copy = cv2.blur(frame_copy, (blur_level, blur_level))
  face_extracted = cv2.bitwise_and(frame_copy, frame_copy, mask=mask)

  background_mask = cv2.bitwise_not(mask)
  background = cv2.bitwise_and(frame, frame, mask=background_mask)

  frame_with_blurred_face = cv2.add(background, face_extracted)
  cv2.imshow("Frame with blurred face", frame_with_blurred_face)
  


def apply_blur(video_path, blur_level, resize_factor):

  face_landmarks = FaceLandmarks()
  capture = cv2.VideoCapture(video_path)

  while True:
      ret, frame = capture.read()
      if not ret:
        break

      frame = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor)
      

      landmarks = face_landmarks.get_facial_landmarks(frame)
      convexhull = cv2.convexHull(landmarks)

      replace_with_blurred_face(frame, convexhull, blur_level)
      
      key = cv2.waitKey(30)
      match key:
        case 27:
            break
        case 82:
          blur_level = blur_level + 1
          if blur_level == 100:
            continue
        case 84:
          if blur_level == 1:
            continue
          blur_level = blur_level - 1
        case _:
          continue
          
  capture.release()
  cv2.destroyAllWindows()
