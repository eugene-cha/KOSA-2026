import cv2
import os

# 데이터 관리를 위한 폴더 (data 폴더가 없으면 생성)
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_FILE_PATH):
    os.makedirs(DATA_FILE_PATH)

dataFile = os.path.join(DATA_FILE_PATH, 'road.mp4')

# 동영상 파일을 읽어서 표시
cap = cv2.VideoCapture(dataFile) # 0 넣으면 웹캠
while True:
    retval, frame = cap.read()
    if not retval:
        break
    cv2.imshow('frame', frame)

    # 이미지를 그레이 스케일로 변환, 엣지(윤곽선) 추출 후 표시
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    cv2.imshow('edges', edges)

    if cv2.waitKey(25) == 27:  # Esc
        break

cap.release()
cv2.destroyAllWindows()
