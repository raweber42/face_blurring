import numpy as np
import argparse
import os
from blur_faces import apply_blur

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--videopath", required=True,
	help="Path to the video in which you want to blur faces")
ap.add_argument("-b", "--blurlevel", type=int, default=13,
	help="Level of blurryness: the higher the number, the blurryer the face gets")
ap.add_argument("-r", "--resizefactor", type=float, default=0.25,
	help="Factor by which the video gets scaled")
args = vars(ap.parse_args())

apply_blur(args["videopath"], args["blurlevel"], args["resizefactor"])
