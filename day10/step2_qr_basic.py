"""
[Step 2] 이미지 전처리 추가
- Step 1에서 만든 기본 코드에 enhance_frame() 함수 추가
- 어두운 환경에서도 QR을 잘 감지하도록 개선

목표:
  1. enhance_frame() 함수 구현 (그레이스케일 + 명도 조정 + CLAHE)
  2. pyzbar.decode(detect_frame) 사용 (원본 대신 전처리된 이미지)
  3. 전처리 여부를 설정으로 선택 가능하게

개선 원리:
  - 그레이스케일: 컬러 정보 제거 (바코드는 흑백만 중요)
  - 명도 조정: 어두운 부분을 밝게
  - CLAHE: 로컬 대비(contrast) 강화 (인접한 픽셀끼리만 비교)
"""

import cv2
from pyzbar import pyzbar

# ==========================================
# 설정
# ==========================================

ENHANCE_IMAGE = True  # True면 전처리 ON, False면 OFF

# ==========================================
# 1️⃣ 이미지 전처리 함수
# ==========================================

def enhance_frame(frame):
    """
    바코드 감지 향상을 위한 이미지 전처리

    입력:
      frame: 원본 컬러 이미지 (BGR)

    출력:
      enhanced: 전처리된 그레이스케일 이미지
    """

    # TODO: 단계 1 - 그레이스케일로 변환
    #       cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # TODO: 단계 2 - 명도 조정 (어두운 부분을 밝게)
    #       cv2.convertScaleAbs(gray, alpha=1.3, beta=20)
    #       - alpha: 명도 배율 (1.3 = 30% 더 밝게)
    #       - beta: 절대 밝기 추가 (20 = 추가로 +20)
    cv2.convertScaleAbs(gray, alpha=1.3, beta=20)

    # TODO: 단계 3 - CLAHE로 대비 강화
    #       clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    #       enhanced = clahe.apply(enhanced)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(enhanced)

    return enhanced  # 전처리된 이미지 반환

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("[오류] 웹캠을 열 수 없습니다.")
    exit()

print("QR Code Scanner 시작 - Step 1: 기본")
print("  q: 종료")


while True:
    ret, frame = cap.read()
    if not ret:
        continue

    qr_codes = pyzbar.decode(frame)

    for qr in qr_codes:
        if qr.type != 'QRCODE':
            continue

        x, y, w, h = qr.rect

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        data = qr.data.decode('utf-8')

        cv2.putText(frame, data, (x, y -10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,255,0), 2)

        print(f"[감지 QR] {data}")
        pass

    cv2.imshow('QR Code SCanner', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print("\n[완료] Step 2 종료")
print("\n📊 비교 관찰:")
print("  1. ENHANCE_IMAGE = True → 어두운 환경에서도 감지")
print("  2. ENHANCE_IMAGE = False → 밝은 환경에서만 감지")
print("  💡 전처리 과정의 중요성을 확인했습니다!")