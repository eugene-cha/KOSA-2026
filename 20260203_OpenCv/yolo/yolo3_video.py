import cv2
import numpy as np
import os

# 경로 설정
WORKING_PATH = os.path.dirname(__file__)
DATA_FILE_PATH = os.path.join(WORKING_PATH, "data")
if not os.path.exists(DATA_FILE_PATH):
    os.makedirs(DATA_FILE_PATH)

WEIGHTS_FILE = os.path.join(WORKING_PATH, "yolov3.weights")
CFG_FILE = os.path.join(WORKING_PATH, "yolov3.cfg")
NAMES_FILE = os.path.join(WORKING_PATH, "coco.names")
VIDEO_FILE = os.path.join(DATA_FILE_PATH, "road.mp4") # road.mp4

# YOLO 네트워크 로드
net = cv2.dnn.readNet(WEIGHTS_FILE, CFG_FILE)

# 클래스 이름 로드
with open(NAMES_FILE, "r") as f:
    classes = [line.strip() for line in f.readlines()]

output_layers_names = net.getUnconnectedOutLayersNames()

# 동영상 캡처
cap = cv2.VideoCapture(VIDEO_FILE) # 0: WebCam

frame_count = 0
while True:
    retval, frame = cap.read()
    if not retval:
        break

    frame_count += 1
    if frame_count % 6 != 0:
        continue # 3프레임 중 1프레임만 처리

    frame = cv2.resize(frame, (800, 516))
    height, width, _ = frame.shape

    # YOLO 입력 Blob 생성
    blob = cv2.dnn.blobFromImage(
        frame, 1 / 255.0, (320, 320), swapRB=True, crop=False
    )
    net.setInput(blob)

    # YOLO Forward
    layer_outputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    # 결과 해석
    for output in layer_outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # NMS 적용
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # 박스 그리기
    if len(indices) > 0:
        for i in indices.flatten():
            x, y, w, h = boxes[i]
            label = classes[class_ids[i]]
            confidence = round(confidences[i], 2)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{label} {confidence}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    cv2.imshow("YOLO Video", frame)

    if cv2.waitKey(25) == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
