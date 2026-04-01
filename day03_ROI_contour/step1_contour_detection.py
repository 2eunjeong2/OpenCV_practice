import cv2 as cv
import numpy as np

# 이미지 로드 (그레이스케일)
img = cv.imread('./img/aircraft.jpg', cv.IMREAD_GRAYSCALE)

if img is None:
    print("이미지를 불러올 수 없어요!")
    exit()

# 이진화
_, binary = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)

# 컨투어 검출
contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

# 컬러 이미지로 변환 (그리기용)
img_color = cv.cvtColor(binary, cv.COLOR_GRAY2BGR)

# 모든 컨투어 초록색으로 그리기
cv.drawContours(img_color, contours, -1, (0, 255, 0), 2)

# 면적 필터링 (100~5000 픽셀 범위) → 파란색으로 그리기
total_count    = len(contours)   # 전체 컨투어 개수
filtered_count = 0               # 필터링된 컨투어 개수

for cnt in contours:
    area = cv.contourArea(cnt)
    if 100 < area < 5000:
        cv.drawContours(img_color, [cnt], 0, (255, 0, 0), 2)
        filtered_count += 1

noise_count = total_count - filtered_count  # 제외된 노이즈 개수

# ✅ 과제 답안 출력
print("=" * 40)
print(f"전체 컨투어 개수       : {total_count}")
print(f"필터링된 컨투어 개수   : {filtered_count}")
print(f"제외된 노이즈          : {noise_count}")
print("=" * 40)

# 결과 표시
cv.imshow('Filtered Contours', img_color)
cv.waitKey(0)
cv.destroyAllWindows()