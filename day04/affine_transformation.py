# affine_transformation : 
# 3개의 점 쌍으로 변환 행렬을 결정하는 방식으로,
#  이동 / 회전 / 크기 / 기울기(shear)를 동시에 표현할 수 있습니다.
# 단, 평행한 선은 변환 후에도 평행을 유지합니다.

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

img = cv.imread(get_sample('messi5.jpg', repo='opencv'))

# 이미지의 높이와 너비 값 가져오기
rows,cols,ch = img.shape


pts1 = np.float32([[50,50],[200,50],[50,200]])  # 원본 3 점
pts2 = np.float32([[10,100],[200,50],[100,250]])  # 변환 후 3점

M = cv.getAffineTransform(pts1,pts2)

dst = cv.warpAffine(img,M,(cols,rows))

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(dst),plt.title('Output')
plt.show()
