
from common_imports import torch, np
from detection import detection

WEIGHTS_PATH = f"best.pt"
model = torch.hub.load('ultralytics/yolov5', 'custom', WEIGHTS_PATH, device=0)


SOURCE_VIDEO_PATH = f"realbayern.mp4"
TARGET_VIDEO_PATH = f"final/realbarca.mp4"

color_list = ['Team 1', 'Team 2']
#color_list = ['#0035d4', '#f2f3f5']
#boundaries = [
#    (np.array([43, 31, 4]), np.array([250, 88, 50])),  # blue
#    (np.array([187, 169, 112]), np.array([255, 255, 255]))  # white
#]

boundaries = [
    (np.array([0, 0, 100]), np.array([100, 100, 255])),  # blue
    (np.array([187, 169, 112]), np.array([255, 255, 255]))  # whiteba
]

detection(WEIGHTS_PATH, model, SOURCE_VIDEO_PATH, TARGET_VIDEO_PATH, color_list, boundaries)