# 과제 1: 🟢 GREEN 1 — 최소 구현

# 라이브러리 import
import numpy as np
import cv2 as cv

# 웹캠을 열기 
cap = cv.VideoCapture(0)
MIN_AREA = 5000

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 감지할 색상의 HSV 범위 설정 - 민트색
lower_color = np.array([50,0,0])
upper_color = np.array([100,255,255])

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

#   마스크 생성 (특정 색상만 추출) 
    mask = cv.inRange(hsv, lower_color, upper_color)

    res = cv.bitwise_and(frame, frame, mask=mask)

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

    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    # cv.imshow('res', res)

#   'q' 키 입력 시 루프 종료
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
