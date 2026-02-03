import cv2
import numpy as np
import os

# 데이터 관리를 위한 폴더 (data 폴더가 없으면 생성)
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_FILE_PATH):
    os.makedirs(DATA_FILE_PATH)

# 원본 이미지 읽고 표시
imageFile = os.path.join(DATA_FILE_PATH, 'lena.jpg')
img = cv2.imread(imageFile)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # 특정 영역의 색상 변경을 위한 HSV 색 공간으로 변환

# img[10:50, 10:50] = 70, 255, 255 # BGR (Blue/Green/Red)
cv2.rectangle(img, (10, 10), (50, 50), (0, 255, 0), 2)

lower_green = np.array([40, 50, 50])
upper_green = np.array([80, 255, 255])
mask = cv2.inRange(hsv, lower_green, upper_green)

# 마스크를 이용하여 색상 변경 (흰색 영역을 파란색으로)
img[mask > 0] = [255, 0, 0] # BGR

# Text
# time.sleep(1000)
cv2.putText(img, 'OpenCV!', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.line(img, (500, 0), (0, 500), (255, 255, 255), 5)
# OPEN
cv2.imshow('lena ED', img)
imageFile = os.path.join(DATA_FILE_PATH, 'lena-ed.png')
cv2.imwrite(imageFile, img) # 다른 이름으로 저장

# # 사용자가 키를 입력하면 창을 닫고 종료하기
cv2.waitKey()
cv2.destroyAllWindows()
