from imutils.video import VideoStream
from flask import Flask
from flask import Response
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2

from blur_faces import apply_blur
import globals

app = Flask(__name__)


@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

@app.route('/video_feed')
def video_feed():
  # TODO: replace 0 with video_path
  return Response(apply_blur(0, 0.75), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/blur_more', methods=['POST'])
def blur_more():
  if globals.blur_level <= 100:
    globals.blur_level = globals.blur_level + 1
    return "More blur applied"
  else:
    return "Maximum blur level reached"

@app.route('/blur_less', methods=['POST'])
def blur_less():
  if globals.blur_level > 1:
    globals.blur_level = globals.blur_level - 1
    return "Less blur applied"
  else:
    return "Minimum blur level reached"

@app.route('/stop_video', methods=['POST'])
def stop_video():
  globals.stream_stopped = True
  print("Video stream stopped")
  return "Video stream stopped"

@app.route('/start_video', methods=['POST'])
def start_video():
  globals.stream_stopped = False
  print("Video stream started")
  return "Video stream started"



if __name__ == '__main__':
  globals.initialize()
  app.run()
