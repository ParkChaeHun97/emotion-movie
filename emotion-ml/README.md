# Emotion-ML — 콘텐츠 감정 분류 파이프라인

[emotion](https://github.com/kowanwooo/emotion) 서비스에서 콘텐츠(영화)에 감정 태그를 부여하기 위해 만든 크롤링 + KoBERT 파인튜닝 파이프라인입니다.

> 이 중 크롤링(`crawling/`)과, 학습된 모델을 이용한 영화별 감정 태깅 코드(`notebooks/` 후반부)는 제가 직접 작성했습니다.

## 파이프라인 개요

```
1. 콘텐츠 메타데이터/리뷰 크롤링 (crawling/)
        ↓
2. 감정 분류 데이터셋(19,374문장, 7-class)으로 KoBERT 파인튜닝 (notebooks/)
        ↓
3. 학습된 모델로 각 영화 리뷰를 감정 분류 → 다수결로 영화의 대표 감정 태깅
        ↓
4. 결과를 emotion 서비스의 MongoDB Contents 컬렉션에 반영
```

## 구성

```
emotion-ml
├── crawling/
│   ├── movie.py          # Selenium + BeautifulSoup으로 다음(Daum) 영화 페이지에서
│   │                      # 제목/장르/국가/평점/줄거리/리뷰 등 수집
│   └── pdUrlCrow.py       # KOBIS 박스오피스 영화명 → 다음 영화 상세페이지 URL 매핑
├── notebooks/
│   └── emotion_classification_kobert.ipynb
│                          # KoBERT 파인튜닝 (7-class 감정 분류) 및
│                          # 크롤링한 리뷰에 대한 감정 추론
├── requirements.txt
└── .gitignore
```

## 모델

- Base model: [SKT KoBERT](https://github.com/SKTBrain/KoBERT)
- Task: 7-class 감정 분류 (공포/놀람/분노/슬픔/중립/행복/혐오)
- 학습 데이터: 대화체 문장 19,374개 (train 80% / test 20%)
- 하이퍼파라미터: max_len 64, batch_size 64, 5 epochs, lr 5e-5, dropout 0.5
- 성능(5 epoch 기준): **Test accuracy 91% / Train accuracy 98%**

## 회고

- 학습된 모델 가중치를 저장(`torch.save`)하지 않아 재현 시 매번 재학습이 필요함
- 감정 클래스 분포가 불균형(행복 4,548 vs 공포 1,386)한데 class weighting을 적용하지 않아, accuracy 외 F1-score 등으로 검증하지 못함
- Train/Test 정확도 격차(98% vs 91%)로 볼 때 경미한 과적합 가능성 — epoch 수 조정이나 정규화 강화 여지가 있음
- 크롤링 스크립트는 다음 영화 페이지의 DOM 구조에 의존적이라 사이트 개편 시 깨질 수 있음

