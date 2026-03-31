import cv2 as cv
import numpy as np
import urllib.request
import os

# 이미지 읽기 (그레이스케일)
# — cv.imread('image.png', cv.IMREAD_GRAYSCALE)
# — 또는 노이즈 제거: cv.medianBlur(img, 5)
# github sample 주소 : https://github.com/opencv/opencv/tree/master/samples/data
def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return cv.imread(filename)

img = get_sample("sudoku.png")
img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)

assert img is not None, "file could not be read, check with os.path.exists()"
img = cv.medianBlur(img,5)

# 콜백 함수 (트랙바용 — 빈 함수)
# def nothing(x):
#     pass

def nothing(x):
    pass

cap = cv.VideoCapture(0)

# 창 생성 (namedWindow)

cv.namedWindow('trackbar')

# 트랙바 생성
# — threshold (0~255, 초기값 127)
# — mode: 0=THRESH_BINARY, 1=THRESH_BINARY_INV

cv.createTrackbar('threshold', 'trackbar', 127, 255, nothing)
cv.createTrackbar('mode', 'trackbar', 0, 1, nothing)

# 반복문
while(1):
    _, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # 트랙바 값 읽기 (getTrackbarPos)
    threshold = cv.getTrackbarPos('threshold', 'trackbar')
    mode = cv.getTrackbarPos('mode', 'trackbar')

    # 이진화 적용
    # — mode가 0이면 THRESH_BINARY, 1이면 THRESH_BINARY_INV
    thresh_mode = cv.THRESH_BINARY if mode == 0 else cv.THRESH_BINARY_INV
    _, result = cv.threshold(gray, threshold, 255, thresh_mode)

    # 원본 | 이진화 결과 나란히 표시
    # — np.hstack([img, thresh]) 또는 np.hstack([img, result])
    combined = np.hstack([gray, result])

    # 현재 임계값을 화면에 표시
    # — cv.putText(result, f'Thresh: {value}', ...)
    cv.putText(combined, f'Thresh: {threshold}', (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv.imshow('trackbar', combined)

    # 'q' → 종료
    if cv.waitKey(1) == ord('q'):
        break

# 창 닫기
cv.destroyAllWindows()