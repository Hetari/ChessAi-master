from math import ceil
from src.Config import Config
from screeninfo import get_monitors


monitors = get_monitors()
width = 0
height = 0
for monitor in monitors:
    if monitor.is_primary:
        width = monitor.width
        height = monitor.height
        break

if width == 0:
    width = height = 1000

HEIGHT = WIDTH = int(height * 0.75) - int(height * 0.75) % 100

ROWS = COLS = 8  # dimension is 8*8
SQ_SIZE = ceil(HEIGHT / COLS)
MAX_FPS = 15  # for animation
IMAGES = {}
DEPTH = 4

config = Config()
