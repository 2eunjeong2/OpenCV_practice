import urllib.request
import os
import numpy as np
import cv2 as cv

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

img = cv.imread(get_sample('messi5.jpg', repo='opencv'), cv.IMREAD_GRAYSCALE)

# 이미지의 높이와 너비 값 가져오기
rows,cols = img.shape


M = cv.getRotationMatrix2D(((cols-1)/2.0,(rows-1)/2.0),90,1)
# ((cols-1)/2.0, (rows-1)/2.0) : 이미지의 정중앙을 의미하고 회전 중심점이 됨
# 90 : angle, 반시계 방향 90도 회전 '회전각'
# 1 : 크기 변화 없음 (1.0 = 원본크기)

dst = cv.warpAffine(img,M,(cols,rows))

cv.imshow('original', img) # 원본 출력
cv.imshow('rotation', dst) # rotation 이미지 출력

cv.waitKey(0)
cv.destroyAllWindows