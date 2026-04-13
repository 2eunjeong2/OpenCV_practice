import cv2 as cv
import numpy as np
import urllib.request
import os

# 이미지 읽기 (그레이스케일)
# — 조명 불균형이 있는 이미지 권장
def get_sample(filename):
    if not os.path.exists(filename):
        url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return cv.imread(filename)

img = get_sample("sudoku.png")
img = cv.imread('sudoku.png', cv.IMREAD_GRAYSCALE)

assert img is not None, "file could not be read, check with os.path.exists()"
img = cv.medianBlur(img,5)

# 콜백 함수
# def nothing(x):
#     pass
def nothing(x):
    pass

# 창 생성
cv.namedWindow('trackbar')

# 트랙바 생성
# — blockSize (3~31, 초기값 11, 반드시 홀수)
# — C (0~20, 초기값 2)
cv.createTrackbar('blockSize', 'trackbar', 11, 31, nothing)
cv.createTrackbar('C', 'trackbar', 2, 20, nothing)

# 반복문
while(1):
    # 트랙바 값 읽기
    blockSize = cv.getTrackbarPos('blockSize', 'trackbar')
    C = cv.getTrackbarPos('C', 'trackbar')

    # blockSize가 짝수면 1 더하기 (홀수 보장)
    # — if blockSize % 2 == 0: blockSize += 1
    if blockSize % 2 == 0: blockSize += 1

    # 최소값 3 보정
    if blockSize < 3: blockSize = 3

    # Global Threshold (고정)
    # — cv.threshold(img, 127, 255, cv.THRESH_BINARY)
    _, global_th = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

    # Otsu 자동 이진화
    # — cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    _, otsu_th = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Adaptive Mean Threshold
    # — cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C,
    #                        cv.THRESH_BINARY, blockSize, C)
    th_mean = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                   cv.THRESH_BINARY, blockSize, C)

    # Adaptive Gaussian Threshold
    # — cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                        cv.THRESH_BINARY, blockSize, C)
    th_gaussian  = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv.THRESH_BINARY, blockSize, C)

    # 2x2 격자로 표시
    # — top = np.hstack([global_th, otsu_th])
    # — bottom = np.hstack([mean_th, gaussian_th])
    # — result = np.vstack([top, bottom])
    top    = np.hstack([global_th, otsu_th])
    bottom = np.hstack([th_mean, th_gaussian ])
    result = np.vstack([top, bottom])

    cv.imshow('trackbar', result)

    # 'q' → 종료
    if cv.waitKey(1) == ord('q'):
        break

# 창 닫기
cv.destroyAllWindows()
