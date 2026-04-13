# ROI로 영역 지정하기
# ROI 추출 : [높이 시작 : 높이 끝, 너비 시작 : 너비 끝]
# ROI란 : 이미지에서 내가 처리하고 싶은 부분만 잘라내는 것

import cv2 as cv 
import urllib.request
import sys 
import os

# github sample 주소 : https://github.com/opencv/opencv/tree/master/samples/data
def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return cv.imread(filename)

# 파일 읽기
img = get_sample("orange.jpg")

# ROI 좌표 및 크기 설정
x = 300     # 시작 x 좌표
y = 100     # 시작 y 좌표
w = 50      # 너비
h = 50      # 높이

# ROI 추출 : [높이 시작 : 높이 끝, 너비 시작 : 너비 끝]
# ROI란 : 이미지에서 내가 처리하고 싶은 부분만 잘라내는 것
roi = img[y : y + h, x : x + w]
print(roi.shape)

# ROI 영역에 사각형 그리기
cv.rectangle(roi, (0,0), (h -1, w -1), (0,255,0))

# 파일 이미지 창 열기
cv.imshow("ROI", img)

# 창 닫기 
k = cv.waitKey(0)

# 파일 저장 
if k == ord("s"):
    cv.imwrite("start_night.png", img)