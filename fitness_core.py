from PIL import Image, ImageDraw, ImageFont
from sense_hat import SenseHat
import numpy as np
import argparse
import time
import cv2
import sys
import threading

# Conditional imports for TPU or CPU
try:
    from pycoral.adapters import common
    from pycoral.utils.edgetpu import make_interpreter
except ImportError:
    pass

try:
    import tensorflow as tf
except ImportError:
    pass

#Constants and Variables
_NUM_KEYPOINTS = 17
CONFIDENCE_THRESHOLD = 0.5

sense = SenseHat()
green = (0, 255, 0)
purple = (128, 0, 128)

#functions
def wait_for(condition, period_of_time):
    while condition:
        for i in range(0,period_of_time):
            time.sleep(1)
        return True
    