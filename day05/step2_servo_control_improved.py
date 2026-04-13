# 과제 2: 🟢 GREEN 2 — 최소 구현

# 라이브러리 import
import numpy as np
import cv2 as cv
import serial
import time

COM_PORT = 'COM3' 
try:
    arduino = serial.Serial(COM_PORT, 9600, timeout=1)
    time.sleep(2) 
    print("✅ PASS: 아두이노 연결 성공!")
except Exception as e:
    print(f"❌ FAIL: 아두이노 연결 실패 ({e})")
    arduino = None

# 웹캠을 열기
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
MIN_AREA = 5000

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 색상 범위 설정 (과제 1에서 확인한 값)
lower_color = np.array([50,0,150])
upper_color = np.array([100,255,255])

# 감지 면적 임계값 설정git add step2_servo_control.py
def detect_color(frame):
    contours, _ = cv.findContours(frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0  # 가장 큰 면적 저장

    for contour in contours:
        area = cv.contourArea(contour)
        if area > max_area:
            max_area = area
        
    return max_area > MIN_AREA, max_area

# 이전 상태 변수 초기화
prev_status = None

# 반복:
while True:
#   웹캠에서 프레임 읽기
    ret, frame = cap.read()

    if not ret:
        break

#   HSV 색공간으로 변환
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

#   마스크 생성
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

#   상태가 이전 상태와 다르면 아두이노에 명령 전송
    if status != prev_status:
        if arduino:  # 연결 실패 시 None이므로 체크
            if result:
                arduino.write(b'O')  # ser → arduino
            else:
                arduino.write(b'C')  # ser → arduino
        prev_status = status

#   현재 상태를 화면에 표시
    cv.putText(frame, status, (30, 50), cv.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
    cv.putText(frame, f"Area: {int(area)}", (30, 100), cv.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

#   'q' 키 입력 시 루프 종료
    cv.imshow('frame', frame)
    cv.imshow('mask', mask)
    # cv.imshow('res', res)

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