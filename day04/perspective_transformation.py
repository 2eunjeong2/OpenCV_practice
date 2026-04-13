# Perspective Transformation : 
# 4개의 점 쌍으로 변환 행렬을 결정하는 방식으로,
# 찌그러진/기울어진 이미지를 정면에서 본 것처럼 펼쳐줍니다.
# 흔히 원근 변환, 투시 변환 이라고도 부릅니다.

import urllib.request
import os
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

def get_sample(filename, repo='insightbook'):

    """부교 또는 OpenCV 공식 샘플 이미지 자동 다운로드
    
    Args:
        filename (str): 이미지 파일명 (예: 'morphological.png')
        repo (str): 'insightbook' (부교) 또는 'opencv' (공식)
    
    Returns:
        str: 다운로드된 파일명
    """
    if not os.path.exists(filename):
        if repo == 'insightbook':
            url = f"https://raw.githubusercontent.com/dltpdn/insightbook.opencv_project_python/master/img/{filename}"
        else:  # opencv 공식
            url = f"https://raw.githubusercontent.com/opencv/opencv/master/samples/data/{filename}"
        urllib.request.urlretrieve(url, filename)
    return filename

# 사용 방법
# img = cv.imread(get_sample('morphological.png', repo='insightbook'))

img = cv.imread(get_sample('sudoku.png', repo='opencv'))

# 이미지의 높이와 너비 값 가져오기
rows,cols,ch = img.shape

pts1 = np.float32([[56,65],[368,52],[28,387],[389,390]]) # 원본 4점
pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]]) # 변환 후 4점

M = cv.getPerspectiveTransform(pts1,pts2)

dst = cv.warpPerspective(img,M,(300,300))

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()
