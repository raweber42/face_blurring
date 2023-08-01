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

from video_state import video_state
from blur_faces import apply_blur

app = Flask(__name__)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")

@app.route('/video_feed_1')
def video_feed_1():
  return Response(apply_blur("src/templates/benedict_oceans_eleven_cut.mp4", 0.75), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_2')
def video_feed_2():
  return Response(apply_blur("src/templates/sad_woman.mp4", 0.75), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed_3')
def video_feed_3():
  return Response(apply_blur("https://storage.googleapis.com/sample_videos_mvp/serious-job-talk-asian-man.mp4", 0.75), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/blur_more', methods=['POST'])
def blur_more():
  if video_state.blur_level <= 100:
    video_state.blur_level = video_state.blur_level + 1
    return "More blur applied"
  else:
    return "Maximum blur level reached"

@app.route('/blur_less', methods=['POST'])
def blur_less():
  if video_state.blur_level > 1:
    video_state.blur_level = video_state.blur_level - 1
    return "Less blur applied"
  else:
    return "Minimum blur level reached"

@app.route('/stop_video', methods=['POST'])
def stop_video():
  video_state.stream_stopped = True
  print("Video stream stopped")
  return "Video stream stopped"

@app.route('/start_video', methods=['POST'])
def start_video():
  video_state.stream_stopped = False
  print("Video stream started")
  return "Video stream started"
