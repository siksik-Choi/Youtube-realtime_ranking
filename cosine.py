#!/usr/bin/python

from konlpy.tag import Okt 
from numpy import dot
from numpy.linalg import norm 
import numpy as np 

# 코사인 유사도를 구하는 함수 
def cos_sim(a, b): 
  return dot(a, b)/(norm(a)*norm(b))

# 기준이 되는 키워드와 벡터 키워드 리스트를 받아서 키워드별 빈도를 구하는 함수 
def make_matrix(feats, list_data):
  freq_list = [] 
  for feat in feats: 
    freq = 0 
    for word in list_data: 
      if feat == word: 
        freq += 1 
    freq_list.append(freq)
  return freq_list 

#파일 내부 값 읽기
def cos(recent, past):

  # 단어들을 중복제거를 위해, set에 데이터를 쌓는다 
  v4 = recent + past
  feats = set(v4) 
  v1_arr = np.array(make_matrix(feats, recent)) 
  v2_arr = np.array(make_matrix(feats, past)) 

  cs = cos_sim(v1_arr, v2_arr) 
  
  return cs
  # 인기 검색어 변동이 큽니다
