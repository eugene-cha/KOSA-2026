import cv2
import os

# 데이터 관리를 위한 폴더 (data 폴더가 없으면 생성)
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_FILE_PATH):
    os.makedirs(DATA_FILE_PATH)

dataFile = os.path.join(DATA_FILE_PATH, 'road.mp4')

# 동영상 파일을 읽어서 표시
cap = cv2.VideoCapture(dataFile)
while True:
    retval, frame = cap.read()
    if not retval:
        break
    cv2.imshow('frame', frame)

    key = cv2.waitKey(25)
    if key == 27:  # Esc
        break

cap.release()
cv2.destroyAllWindows()
