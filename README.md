# Daily English with Gemini

매일 Google Gemini AI를 활용해 영어 공부 콘텐츠를 생성하고 이메일로 받아보는 프로젝트입니다.

## 주요 기능

*   **자동 콘텐츠 생성**: Google `gemini-2.5-flash` 모델을 사용하여 매일 새로운 영어 학습 자료를 만듭니다.
*   **프롬프트 기반**: `prompts/daily_prompt.txt` 파일에 정의된 지침에 따라 맞춤형 콘텐츠를 생성합니다.
*   **이메일 전송**: 생성된 내용을 보기 편한 HTML 형식으로 변환하여 지정된 이메일 주소로 발송합니다.
*   **환경 변수 관리**: API 키와 이메일 정보를 환경 변수로 안전하게 관리합니다.

## 시작하기

### 1. 필수 조건

*   Python 3.8 이상
*   Google Gemini API Key
*   Gmail 계정 (앱 비밀번호 필요)

### 2. 설치

필요한 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

다음 환경 변수를 설정해야 합니다.

| 변수명 | 설명 |
|---|---|
| `GEMINI_API_KEY` | Google AI Studio에서 발급받은 API 키 |
| `EMAIL_USER` | 발송할 이메일 주소 (Gmail) |
| `EMAIL_PASS` | Gmail 앱 비밀번호 (일반 비밀번호 아님) |
| `EMAIL_RECEIVER` | 메일을 받을 이메일 주소 |

### 4. 실행

```bash
python daily_english.py
```

## 파일 구조

```
eng_with_gemini/
├── daily_english.py  # 메인 실행 스크립트
├── requirements.txt  # 의존성 패키지 목록
└── prompts/
    └── daily_prompt.txt # AI에게 전달할 프롬프트 파일
```