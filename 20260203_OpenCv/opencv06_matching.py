import cv2
import os

# 데이터 관리를 위한 폴더 (data 폴더가 없으면 생성)
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_FILE_PATH):
  os.makedirs(DATA_FILE_PATH)

# 찾고자 하는 이미지를 읽고 가로/세로 크기를 구함
image_file = os.path.join(DATA_FILE_PATH, 'wili.png')
template = cv2.imread(image_file)
th, tw = template.shape[:2]
cv2.imshow('template', template)

# 배경 이미지를 준비
image_file = os.path.join(DATA_FILE_PATH,'original.jpg')
image = cv2.imread(image_file)

# 이미지 특징 매칭
result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

# 매칭 좌표를 이미지에 그리기
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
top_left = maxLoc
match_val = maxVal
bottom_right = (top_left[0] + tw, top_left[1] + th)
cv2.rectangle(image, top_left, bottom_right, (0, 0, 255), 7)
cv2.imshow('Result', image)

# 키 입력시 창을 닫고 종료
cv2.waitKey(0)
cv2.destroyAllWindows()
