import urllib.request
import os
from pathlib import Path
import cv2 as cv
import numpy as np
import matplotlib.pylab as plt 

# ============================================================
# 샘플 이미지 자동 다운로드
# ============================================================
def get_sample(filename, repo='opencv'):
    """
    샘플 이미지를 자동으로 다운로드하는 헬퍼 함수
    
    Args:
        filename (str): 이미지 파일명 (예: 'sudoku.png')
        repo (str): 저장소 선택
            - 'opencv': https://github.com/opencv/opencv/samples/data
            - 'insightbook': https://github.com/dltpdn/insightbook.opencv_project_python/img
    
    Returns:
        str: 로컬 파일 경로 (다운로드되지 않으면 None)
    
    Example:
        img = cv.imread(get_sample('sudoku.png'))
        img2 = cv.imread(get_sample('street.jpg', repo='insightbook'))
    """
    
    # 저장소 URL 매핑
    repo_urls = {
        'opencv': 'https://raw.githubusercontent.com/opencv/opencv/master/samples/data',
        'insightbook': 'https://raw.githubusercontent.com/dltpdn/insightbook.opencv_project_python/master/img'
    }
    
    if repo not in repo_urls:
        print(f"❌ 알 수 없는 저장소: {repo}. 'opencv' 또는 'insightbook' 중 선택하세요.")
        return None
    
    # 로컬 파일 존재 확인
    if os.path.exists(filename):
        print(f"✅ 이미 존재: {filename}")
        return filename
    
    # 다운로드
    url = f"{repo_urls[repo]}/{filename}"
    try:
        print(f"📥 다운로드 중: {filename} ({repo})...")
        urllib.request.urlretrieve(url, filename)
        print(f"✅ 다운로드 완료: {filename}")
        return filename
    except Exception as e:
        print(f"❌ 다운로드 실패: {e}")
        print(f"   URL: {url}")
        return None
    
# 이미지 로드
img = cv.imread(get_sample('moon_gray.jpg', repo='insightbook'))

if img is None:
    print("❌ 이미지를 불러올 수 없습니다.")
    exit()

# 그레이스케일 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# ============================================================
# 1. Canny 에지 검출
# ============================================================
threshold1 = 100   # 낮은 임계값
threshold2 = 200  # 높은 임계값
#
# Canny 에지 검출 적용
edges = cv.Canny(gray, threshold1, threshold2)

# ============================================================
# 2. 모폴로지 연산 — 열기 (Opening)
# ============================================================
# 커널 생성 (5x5 타원)
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
#
# 열기 연산 (침식 후 팽창: 노이즈 제거)
edges_cleaned = cv.morphologyEx(edges, cv.MORPH_OPEN, kernel)
#
# 선택사항: 닫기 연산 (팽창 후 침식: 구멍 채우기)
edges_closed = cv.morphologyEx(edges_cleaned, cv.MORPH_CLOSE, kernel)

# ============================================================
# 3. 결과 비교 표시
# ============================================================
# 원본 → Canny → 열기 → 닫기 순서로 4개 이미지 배열
canny_color = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
cleaned_color = cv.cvtColor(edges_cleaned, cv.COLOR_GRAY2BGR)
closed_color = cv.cvtColor(edges_closed, cv.COLOR_GRAY2BGR)
#
top_row = np.hstack([img, canny_color])
bottom_row = np.hstack([cleaned_color])
result = np.hstack([top_row, bottom_row])
#
cv.imshow('Edge Detection + Morphology', result)
cv.waitKey(0)
cv.destroyAllWindows()