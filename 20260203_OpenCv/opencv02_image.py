import cv2
import os

# 데이터 관리를 위한 폴더 (data 폴더가 없으면 생성)
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "data")
if not os.path.exists(DATA_FILE_PATH):
  os.makedirs(DATA_FILE_PATH)

# 원본 이미지를 읽고 화면에 표시
imageFile = os.path.join(DATA_FILE_PATH, 'lena.jpg')
img = cv2.imread(imageFile)
cv2.imshow('Lena Original',img)

# 선과 사각형 그리기
pt1 = 100, 100
pt2 = 300, 300
cv2.rectangle(img, pt1, pt2, (0, 255, 0), 2)

cv2.line(img, (0, 0), (400, 0), (255, 0, 0), 10)
cv2.line(img, (0, 0), (0, 400), (0, 0, 255), 10)

# 특정 영역의 색상 변경
img[10:50, 10:50] = 0

# 텍스트 출력
font = cv2.FONT_HERSHEY_SIMPLEX
text = "Hello"
cv2.putText(img, text, (300, 300), font, 1, (255, 255, 255), 4)

# 편집한 이미지를 저장하고 다시 읽기 (단, 저장시 낮은 품질로 저장해 보기)
cv2.imshow('Lena Edited', img)
imageFile = os.path.join(DATA_FILE_PATH, 'Lena2.jpg')
cv2.imwrite(imageFile, img, [cv2.IMWRITE_JPEG_QUALITY, 2])
img = cv2.imread(imageFile)
cv2.imshow('Lena 2nd', img)

# 임의의 키를 누르면 창을 닫고 종료
cv2.waitKey()
cv2.destroyAllWindows()
