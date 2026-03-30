import numpy as np
import cv2 as cv
 
# my_photo.png 읽기
img = cv.imread("my_photo.png")

# 이미지 높이(h), 너비(w) 가져오기 — img.shape[:2]
print(img.shape)  # (높이, 너비, 채널) 출력 예시 → (480, 640, 3)

height, width = img.shape[:2]
print(f"너비: {width}, 높이: {height}")

# --- 하단 반투명 배경 바 ---
# 1) overlay = img.copy()
# 2) overlay 하단 80px 영역에 검정 사각형 채우기 (thickness=-1)
# 3) addWeighted로 img와 overlay를 50:50 합성
overlay = img.copy()
cv.rectangle(img,(0, 380),(640,480),(0,0,0),-1)
img = cv.addWeighted(img, 0.5, overlay, 0.5, 0)

# --- 텍스트 ---
# 이름 텍스트 넣기 (putText) — 하단 배경 바 안쪽 위치
# 소속 텍스트 넣기 (putText) — 이름 아래에 작은 크기로
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'Olivia',(10,430), font, 1.5,(255,255,255),1,cv.LINE_AA)
cv.putText(img,'Slytherin',(13,460), font, 0.7,(255,255,255),1,cv.LINE_AA)

# 이미지 출력
cv.imshow("my_id_card", img)

# 결과 표시 + 키 입력 대기
k = cv.waitKey(0)

# my_id_card.png로 저장
if k == ord('s'):                    # s 누르면 저장
    cv.imwrite("my_id_card.png", img)
    print("이미지가 저장되었습니다!")

elif k == ord('q'):                  # q 누르면 종료
    cv.destroyAllWindows()