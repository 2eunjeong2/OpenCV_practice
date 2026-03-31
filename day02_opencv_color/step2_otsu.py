import cv2 as cv
import numpy as np
import urllib.request
import os

# 이미지 읽기 (그레이스케일)
def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return cv.imread(filename)

img = get_sample("sudoku.png")
img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)

assert img is not None, "file could not be read, check with os.path.exists()"
img = cv.medianBlur(img,5)

# 창 생성
def nothing(x):
    pass

cv.namedWindow('trackbar')

# 트랙바 생성
# — manual_thresh (0~255, 초기값 127) — 수동 이진화용
# — mode: 0=Otsu만, 1=수동+ Otsu 비교

cv.createTrackbar('manual_thresh', 'trackbar', 127, 255, nothing)
cv.createTrackbar('mode', 'trackbar', 0, 1, nothing)

# 반복문
while(1):
    # 수동 이진화
    # — cv.threshold(img, manual_thresh, 255, cv.THRESH_BINARY)
    manual_thresh = cv.getTrackbarPos('manual_thresh', 'trackbar')
    ret1,th1 = cv.threshold(img, manual_thresh, 255, cv.THRESH_BINARY)

    # Otsu 자동 이진화
    # — cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # — 반환값 중 ret이 실제 계산된 임계값
    ret2,th2 = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # 2개 또는 3개 비교 표시
    # — mode가 0이면: 원본 | 수동 | Otsu
    # — mode가 1이면: 원본 | 수동 | Otsu
    mode = cv.getTrackbarPos('mode', 'trackbar')
    if mode == 0:
        combined = np.hstack([img, th1])
    else:
        combined = np.hstack([img, th1, th2])

    # Otsu 임계값을 화면에 표시
    # — cv.putText(otsu_th, f'Otsu: {ret_otsu:.0f}', ...)
    cv.putText(combined, f'Otsu: {ret2:.0f}', (10, 30),
               cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv.imshow('trackbar', combined)
    
    # 'q' → 종료
    if cv.waitKey(1) == ord('q'):
        break

cv.destroyAllWindows()
