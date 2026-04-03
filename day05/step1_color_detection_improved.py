# 과제 1: 🔵 REFACTOR 1 — 안정성 개선

# 라이브러리 import
import numpy as np
import cv2 as cv

# 웹캠을 열기 
cap = cv.VideoCapture(0)
MIN_AREA = 5000

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 트랙바 콜백 (아무것도 안 해도 되지만 필수로 있어야 함)
def nothing(x):
    pass

# 트랙바 창 생성
cv.namedWindow('trackbar')
cv.resizeWindow('trackbar', 300, 300)

# 트랙바 6개 생성 (이름, 창이름, 초기값, 최대값, 콜백)
cv.createTrackbar('H_min', 'trackbar', 0,   180, nothing)
cv.createTrackbar('H_max', 'trackbar', 180, 180, nothing)
cv.createTrackbar('S_min', 'trackbar', 0,   255, nothing)
cv.createTrackbar('S_max', 'trackbar', 255, 255, nothing)
cv.createTrackbar('V_min', 'trackbar', 0,   255, nothing)
cv.createTrackbar('V_max', 'trackbar', 255, 255, nothing)

# 감지 면적 임계값 설정
def detect_color(frame):
    contours, _ = cv.findContours(frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0  # 가장 큰 면적 저장

    for contour in contours:
        area = cv.contourArea(contour)
        if area > max_area:
            max_area = area
        
    return max_area > MIN_AREA, max_area

# 반복:
while True:
#   웹캠에서 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        break

#   HSV 색공간으로 변환
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
#   트랙바에서 현재 값 읽기
    h_min = cv.getTrackbarPos('H_min', 'trackbar')
    h_max = cv.getTrackbarPos('H_max', 'trackbar')
    s_min = cv.getTrackbarPos('S_min', 'trackbar')
    s_max = cv.getTrackbarPos('S_max', 'trackbar')
    v_min = cv.getTrackbarPos('V_min', 'trackbar')
    v_max = cv.getTrackbarPos('V_max', 'trackbar')

    # 트랙바 값으로 범위 설정
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

#   마스크 생성 (특정 색상만 추출) 
    mask = cv.inRange(hsv, lower, upper)

    res = cv.bitwise_and(frame, frame, mask=mask)
    
#   모폴로지 연산으로 노이즈 제거
    kernel = np.ones((5, 5), np.uint8)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)   # 작은 노이즈 제거
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)  # 구멍 메우기

#   ROI 좌표 및 크기 설정
    h, w = frame.shape[:2]      # 높이, 너비
    rect_w, rect_h = 320, 240   # 사각형 높이, 너비

#   좌상단 좌표
    x1 = w // 2 - rect_w // 2
    y1 = h // 2 - rect_h // 2 

#   우하단 좌표
    x2 = w // 2 + rect_w // 2
    y2 = h // 2 + rect_h // 2

    # (np.zeros((h, w), dtype=np.uint8) 전부 검정(0)으로 채워진 빈 영역 생성
    roi_mask = np.zeros((h, w), dtype=np.uint8)

    # 사각형 영역만 흰색(255)으로 채움
    roi_mask[y1:y2, x1:x2] = 255
    
    # bitwise_and 함수로 일치하는 부분만 남김
    mask = cv.bitwise_and(mask, roi_mask)
    res = cv.bitwise_and(frame,frame, mask= mask)

    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv.rectangle(res, (x1, y1), (x2, y2), (0, 0, 255), 2)

#   마스크 픽셀 면적 계산
    result, area = detect_color(mask)

#   면적과 임계값 비교하여 상태 결정
    if result:
        status = "DETECTED"
        color = (0, 255, 0) # 문자 색
    else:
        status = "NOT DETECTED"
        color = (0, 0, 255) # 문자 색

#   상태를 터미널과 화면에 표시
    cv.putText(frame, status, (30, 50), cv.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
    cv.putText(frame, f"Area: {int(area)}", (30, 100), cv.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    print(f"Area: {int(area)}")
    
#   'q' 키 입력 시 루프 종료
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    cv.imshow('res', res)

    print(f"shape: {frame.shape}") # (높이, 너비, 채널)

    key = cv.waitKey(1)

    if key == ord('q'):
        if result:
            print("✅ PASS: 색상 감지 성공!")
        else:
            print("❌ FAIL: detect_color() 함수가 아직 구현되지 않았습니다")
        cap.release()
        break

# 리소스 해제
cv.destroyAllWindows()
