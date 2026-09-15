# Emotion — 감정 기반 콘텐츠 추천 서비스

웹캠으로 표정을 인식해서 사용자의 감정을 분석하고, 그 감정에 맞는 영화 콘텐츠를 추천해주는 웹 서비스입니다. 대학교 졸업 프로젝트로 팀원들과 함께 개발했습니다.

> ⚠️ 원본 저장소: [kowanwooo/emotion](https://github.com/kowanwooo/emotion) — 팀 프로젝트를 학습/포트폴리오 목적으로 Fork하여 정리했습니다.

## 주요 기능

이 서비스는 두 가지 감정 인식을 결합합니다.

1. **사용자 실시간 감정 인식**: `face-api.js`로 웹캠에서 사용자 표정을 분석해 7가지 감정(행복/슬픔/분노/공포/놀람/혐오/중립) 중 하나로 실시간 분류
2. **콘텐츠(영화) 감정 태깅**: 다음(Daum) 영화 리뷰를 크롤링한 뒤, 19,374개 문장으로 파인튜닝한 KoBERT 모델로 리뷰를 감정 분류 → 다수결로 영화별 대표 감정을 미리 태깅 (→ [`emotion-ml/`](./emotion-ml) 참고)

이 두 감정을 매칭해서, "지금 사용자의 표정과 같은 감정을 가진 콘텐츠"를 추천합니다.

- **표정 인식 기반 추천**: 위 1번 기반으로 사용자 감정에 맞는 콘텐츠 추천
- **감정/장르/국가별 콘텐츠 탐색**: 감정, 장르, 국가(한국/해외) 기준으로 콘텐츠 필터링 및 페이지네이션 조회
- **회원 시스템**: 회원가입/로그인, JWT + 쿠키 기반 인증, bcrypt 비밀번호 해싱
- **콘텐츠 상호작용**: 좋아요, 찜하기(위시리스트), 시청 기록 저장
- **커뮤니티**: 게시판, 댓글 기능
- **마이페이지**: 내가 찜한 콘텐츠, 방문한 콘텐츠 모아보기

## 기술 스택

**Client**
- React
- (상태관리 / 라이브러리 구성은 `client/src/_actions`, `_reducers` 참고)
- face-api.js (얼굴 표정 인식)

**Server**
- Node.js, Express
- MongoDB, Mongoose
- JWT, bcrypt

## 폴더 구조

```
emotion
├── client          # React 프론트엔드
│   └── src
│       ├── components
│       │   ├── FaceApi      # 표정 인식 & 추천
│       │   ├── LandingPage
│       │   ├── BoardPage
│       │   ├── MyPage
│       │   └── ...
│       ├── _actions
│       └── _reducers
├── server          # Express 백엔드
│   ├── models       # User, Contents, Board, Comment, Like ...
│   ├── routes       # 인증, 콘텐츠, 게시판, 마이페이지 ...
│   └── middleware   # JWT 인증
└── emotion-ml      # 콘텐츠 크롤링 + KoBERT 감정 분류 파이프라인
    ├── crawling
    └── notebooks
```

## 콘텐츠 감정 분류 파이프라인 (ML)

영화 콘텐츠에 감정 태그를 붙이는 작업은 별도 파이프라인으로 진행했습니다. (코드: [`emotion-ml/`](./emotion-ml) 폴더)

- **크롤링**: Selenium + BeautifulSoup으로 다음(Daum) 영화 페이지에서 제목/장르/국가/평점/줄거리/리뷰 수집, KOBIS 박스오피스 데이터와 결합
- **감정 분류 모델**: [KoBERT](https://github.com/SKTBrain/KoBERT)를 대화체 문장 19,374개(7-class: 행복/슬픔/분노/공포/놀람/혐오/중립)로 파인튜닝
- **성능**: 5 epoch 기준 Test accuracy 91%, Train accuracy 98%
- **적용**: 학습된 모델로 영화별 리뷰를 감정 분류한 뒤 다수결로 대표 감정을 산출, `Contents` 컬렉션에 저장

> 클래스 불균형(행복 4,548 vs 공포 1,386)에 대한 처리가 없었고, 모델 가중치를 저장하지 않아 재현 시 매번 재학습이 필요했던 점은 한계로 남아있습니다. 자세한 내용은 [`emotion-ml/README.md`](./emotion-ml/README.md) 참고.

## 내가 맡은 부분

- 콘텐츠 크롤링 (`emotion-ml/crawling/movie.py`, `pdUrlCrow.py`) — Selenium + BeautifulSoup으로 다음(Daum) 영화 페이지에서 메타데이터/리뷰 수집, KOBIS 박스오피스 데이터 매핑
- 학습된 KoBERT 모델을 이용한 콘텐츠 감정 태깅 코드 (`emotion-ml/notebooks/emotion_classification_kobert.ipynb` 후반부) — 영화별 리뷰를 감정 분류한 뒤 다수결로 대표 감정 산출
- 백엔드: 좋아요(`server/routes/like.js`), 찜하기(`server/routes/wishContents.js`), 투표(`server/routes/voteuser.js`), 마이페이지 콘텐츠 조회 기록(`server/routes/lookContents.js`) API
- 위 기능들과 연결된 프론트엔드 및 CSS 스타일링


## 회고

제가 직접 구현한 `like.js`, `wishContents.js`, `voteuser.js`, `lookContents.js`를 지금 다시 보면 가장 먼저 눈에 띄는 문제는 **권한 검증 부재**입니다. 이 라우트들은 `auth` 미들웨어 없이, 요청 body로 받은 `userFrom` 값을 그대로 신뢰해서 좋아요/찜하기/투표/시청기록을 처리합니다. 즉 로그인 토큰과 무관하게 body에 임의의 사용자 ID를 넣으면 다른 사람 행세로 요청을 보낼 수 있는 구조였습니다 (IDOR / Broken Access Control). 지금이라면 `auth` 미들웨어를 거쳐 `req.user._id`로 본인 여부를 서버에서 직접 확인하고, 클라이언트가 보낸 사용자 ID는 신뢰하지 않았을 것입니다.

그 외에도 당시엔 REST 컨벤션이나 에러 핸들링을 깊이 고려하지 못하고 콜백 기반으로 구현했는데, 지금 다시 본다면 async/await 기반으로 리팩토링하고, 감정별로 중복된 라우트들을 파라미터화해서 정리했을 것 같습니다.
