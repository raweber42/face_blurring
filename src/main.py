import numpy as np
import argparse
import os
from blur_faces import apply_blur
from blur_faces_photo import apply_blur_on_photo

ap = argparse.ArgumentParser()
ap.add_argument("--type", required=True,
	help="Choice of video vs photo")
ap.add_argument("-p", "--path", required=True,
	help="Path to the video in which you want to blur faces")
ap.add_argument("-b", "--blurlevel", type=int, default=13,
	help="Level of blurryness: the higher the number, the blurryer the face gets")
ap.add_argument("-r", "--resizefactor", type=float, default=0.25,
	help="Factor by which the video gets scaled")
args = vars(ap.parse_args())

if args["type"] == "video":
  apply_blur(args["path"], args["blurlevel"], args["resizefactor"])
elif args["type"] == "photo":
  apply_blur_on_photo(args["path"], args["blurlevel"], args["resizefactor"])
else:
  print("Error: Invalid type. Enter 'video' or 'photo'")

