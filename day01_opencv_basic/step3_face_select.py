import numpy as np
import cv2 as cv
 
# my_id_card.png 읽기
img = cv.imread("my_id_card.png")

# 원본 복사본 만들기 — 드래그 중 이전 사각형을 지우기 위해
temp = img.copy()  # 임시 이미지 추가

# 전역 변수: ix, iy (시작점), drawing (드래그 중 여부)
drawing = False
mode = True
ix, iy = -1, -1

# 마우스 콜백 함수 정의
    # LBUTTONDOWN: 드래그 시작, 시작점(ix, iy) 저장
    # MOUSEMOVE: 드래그 중이면
    #     원본에서 img 복원 (이전 사각형 제거)
    #     현재 위치까지 초록색 사각형 그리기 (두께 2)
    # LBUTTONUP: 드래그 끝
    #     최종 사각형 그리기
    #     사각형 위에 "FACE" 텍스트 넣기
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode, img, temp, cropped
    font = cv.FONT_HERSHEY_SIMPLEX

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                temp = img.copy()  # 원본 복사 후 임시 이미지에만 그리기
                cv.rectangle(temp, (ix, iy), (x, y), (0, 255, 0), 2)
            else:
                cv.circle(img, (x, y), 5, (0, 0, 255), -1)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            img = temp.copy()  # 마우스 떼면 원본에 반영
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)


            # 텍스트가 정확히 중앙에 오도록 텍스트 크기만큼 보정
            text_size = cv.getTextSize('FACE', font, 1, 2)[0]  # (너비, 높이) 반환
            
            # 사각형 중앙 좌표               
            
            x1, y1 = min(ix, x), min(iy, y)  # 드래그 방향 상관없이 정렬
            x2, y2 = max(ix, x), max(iy, y)

            tx = (x1 + x2) // 2 - text_size[0] // 2
            ty = (y1) + text_size[1] + 20

            cv.putText(img, 'FACE', (tx, ty), font, 1, (255, 255, 255), 1)

            

            cropped = img[y1:y2, x1:x2]  # y: 100~300, x: 200~400

        else:
            cv.circle(img, (x, y), 5, (0, 0, 255), -1)

cv.namedWindow('image')
cv.setMouseCallback('image', draw_circle)


# 창 생성 + 마우스 콜백 등록
# 반복문
    # 이미지 표시
    # 키 입력 대기
    # 's' → my_id_card_final.png로 저장 후 break
    # 'q' → break

while(1):
    if drawing and mode:
        cv.imshow('image', temp)  # 드래그 중엔 임시 이미지 표시
    else:
        cv.imshow('image', img)   # 평소엔 원본 표시
    
    key = cv.waitKey(1)

    # 창 닫기, 저장
    if key == ord('q'):
        break
    elif key == ord('s'):
        cv.imwrite("my_id_card_final.png", img)
        cv.imwrite("my_id_card_final_2.png", cropped)
        print("이미지가 저장되었습니다!")
        break



