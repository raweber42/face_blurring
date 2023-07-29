# https://pysource.com/blur-faces-in-real-time-with-opencv-mediapipe-and-python
import cv2
import mediapipe as mp
import numpy as np
from facial_landmarks import FaceLandmarks

     
def render_with_blurred_face(frame, convexhull, blur_level):
  
  height, width, _ = frame.shape
  mask = np.zeros((height, width), np.uint8)
  cv2.fillConvexPoly(mask, convexhull, 255)
  
  frame_copy = frame.copy()
  frame_copy = cv2.blur(frame_copy, (blur_level, blur_level))
  face_extracted = cv2.bitwise_and(frame_copy, frame_copy, mask=mask)

  background_mask = cv2.bitwise_not(mask)
  background = cv2.bitwise_and(frame, frame, mask=background_mask)

  frame_with_blurred_face = cv2.add(background, face_extracted)
  cv2.imshow("Frame", frame_with_blurred_face)
  return frame_with_blurred_face;


def render_without_blurred_face(frame):
  
  cv2.imshow("Frame", frame)
  


def apply_blur_on_photo(photo_path, blur_level, resize_factor):

  face_landmarks = FaceLandmarks()
  frame = cv2.imread(photo_path)
  frame = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor)
  
  try:
    landmarks = face_landmarks.get_facial_landmarks(frame)
  except Exception:
    render_without_blurred_face(frame)
  else: 
    convexhull = cv2.convexHull(landmarks)
    frame = render_with_blurred_face(frame, convexhull, blur_level)
  
  # TODO: Render image anyways
  # TODO: How to do sound?
  # TODO: Space key for stopping
  # TODO: How to handle multiple faces?

  
  key = cv2.waitKey(0)
  match key:
    case 27:
      exit
    case 82:
      if blur_level <= 100:
        blur_level = blur_level + 1
    case 84:
      if blur_level >= 1:
        blur_level = blur_level - 1

        
  cv2.destroyAllWindows()
  out_path = photo_path.rsplit('.', maxsplit=1)[0]
  cv2.imwrite(out_path + '_blurred_' + str(blur_level) + '.jpg', frame)
