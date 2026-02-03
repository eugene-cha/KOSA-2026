# Hough Line Transform을 이용한 직선 검출

import cv2 as cv
import os

# 데이터 관리를 위한 폴더 (data 폴더가 없으면 생성)
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_FILE_PATH):
  os.makedirs(DATA_FILE_PATH)

# 도로 이미지 읽어서 표시
imgfile = os.path.join(DATA_FILE_PATH, 'Roads.png')
cimg = cv.imread(imgfile)
cv.imshow('Roads - original', cimg)


# 도로이미지를 GRAY로 변환 후 이진화, 에지 추출 후 표시
img = cv.cvtColor(cimg, cv.COLOR_BGR2GRAY)
_, img = cv.threshold(img, 100, 255, cv.THRESH_BINARY)
img = cv.Canny(img, 50, 200, None, 3)
cv.imshow('Image - binary & edge', img)


# 사용자 입력키 대기 및 종료
cv.waitKey()
cv.destroyAllWindows()
