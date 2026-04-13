import cv2 as cv
import numpy as np

# 트랙바 콜백 (아무것도 안 해도 되지만 필수로 있어야 함)
def nothing(x):
    pass

cap = cv.VideoCapture(0)

# 트랙바 창 생성
cv.namedWindow('trackbar')

# 트랙바 6개 생성 (이름, 창이름, 초기값, 최대값, 콜백)
cv.createTrackbar('H_min', 'trackbar', 0,   180, nothing)
cv.createTrackbar('H_max', 'trackbar', 180, 180, nothing)
cv.createTrackbar('S_min', 'trackbar', 0,   255, nothing)
cv.createTrackbar('S_max', 'trackbar', 255, 255, nothing)
cv.createTrackbar('V_min', 'trackbar', 0,   255, nothing)
cv.createTrackbar('V_max', 'trackbar', 255, 255, nothing)

while(1):
    _, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV) # RGB > HSV로 변환하는 함수

    # 트랙바에서 현재 값 읽기
    h_min = cv.getTrackbarPos('H_min', 'trackbar')
    h_max = cv.getTrackbarPos('H_max', 'trackbar')
    s_min = cv.getTrackbarPos('S_min', 'trackbar')
    s_max = cv.getTrackbarPos('S_max', 'trackbar')
    v_min = cv.getTrackbarPos('V_min', 'trackbar')
    v_max = cv.getTrackbarPos('V_max', 'trackbar')

    # 트랙바 값으로 범위 설정
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    mask = cv.inRange(hsv, lower, upper)
    res = cv.bitwise_and(frame, frame, mask=mask)

    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv.destroyAllWindows()