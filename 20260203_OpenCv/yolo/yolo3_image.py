import cv2
import numpy as np
import os

# NOTE: 동영상인 경우, 동영상은 정지 이미지가 n개(fps) 이상씩 이어지는 것이므로
#       for문 내에서 videoCapture 메서드를 수행시키면 됨

# 데이터 관리를 위한 폴더 (data 폴더가 없으면 생성)
WORKING_PATH = os.path.dirname(__file__)
DATA_FILE_PATH = os.path.join(WORKING_PATH, "data")
if not os.path.exists(DATA_FILE_PATH):
  os.makedirs(DATA_FILE_PATH)

WEIGHTS_FILE = os.path.join(WORKING_PATH, "yolov3.weights")
CFG_FILE = os.path.join(WORKING_PATH, "yolov3.cfg")

# YOLO model configuration과 weights를 로드
net = cv2.dnn.readNet(WEIGHTS_FILE, CFG_FILE)

# Class labels를 Load (COCO names)
NAMES_FILE = os.path.join(WORKING_PATH, "coco.names")
with open(NAMES_FILE, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# 분석 대상 파일 읽기
IMAGE_FILE = os.path.join(DATA_FILE_PATH, "animal.jpeg")
img = cv2.imread(IMAGE_FILE)
height, width, _ = img.shape

# YOLO를 이용한 분석
blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)

# Get output layer names
output_layers_names = net.getUnconnectedOutLayersNames()

# Forward pass through YOLO
layer_outputs = net.forward(output_layers_names)

# 점검 결과 분석 및 활용
boxes = []
confidences = []
class_ids = []

for output in layer_outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]

        if confidence > 0.5:  # Confidence threshold
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)

            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Apply non-maximum suppression to eliminate redundant overlapping boxes
indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Draw bounding boxes and labels on the image
if len(indices) > 0:
    for i in indices.flatten():
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = str(round(confidences[i], 2))
        color = (0, 255, 0)  # Green color for boxes

        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label + " " + confidence, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Display the image with detections
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()