import numpy as np
import cv2 as cv

drawing = False
mode = True
ix, iy = -1, -1

img = np.zeros((512, 512, 3), np.uint8)
temp = img.copy()  # ✅ 임시 이미지 추가

def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, mode, img, temp

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            if mode == True:
                temp = img.copy()  # ✅ 원본 복사 후 임시 이미지에만 그리기
                cv.rectangle(temp, (ix, iy), (x, y), (0, 255, 0), 2)
            else:
                cv.circle(img, (x, y), 5, (0, 0, 255), -1)

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        if mode == True:
            img = temp.copy()  # ✅ 마우스 떼면 원본에 반영
            cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
        else:
            cv.circle(img, (x, y), 5, (0, 0, 255), -1)

cv.namedWindow('image')
cv.setMouseCallback('image', draw_circle)

while(1):
    if drawing and mode:
        cv.imshow('image', temp)  # ✅ 드래그 중엔 임시 이미지 표시
    else:
        cv.imshow('image', img)   # ✅ 평소엔 원본 표시
    
    k = cv.waitKey(1) & 0xFF
    if k == ord('m'):
        mode = not mode
    elif k == 27:
        break

cv.destroyAllWindows()
