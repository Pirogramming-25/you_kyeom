# 🚀 Django_GPT

피로그래밍 25기 5주차 과제 - Hugging Face AI 모델과 Django를 연동한 웹 서비스

---

## 🛠️ 기술 스택

- **Backend**: Django 5.x, Django ORM, Django Authentication
- **AI / ML**: Hugging Face Transformers (`pipeline`), PyTorch
- **Frontend**: HTML / CSS / JavaScript (`Fetch API`, CSRF Protection)

---

## 🤖 사용한 Hugging Face 모델 정보

| 기능               | Task                  | Model ID                                           | 라이선스   | 입력 언어          | 주요 출력 레이블                                                        |
| :----------------- | :-------------------- | :------------------------------------------------- | :--------- | :----------------- | :---------------------------------------------------------------------- |
| **감정 분석**      | `text-classification` | `cardiffnlp/twitter-roberta-base-sentiment-latest` | MIT        | 영어 (1~1,000자)   | `positive`, `neutral`, `negative`                                       |
| **문서 요약**      | `summarization`       | `sshleifer/distilbart-cnn-6-6`                     | Apache 2.0 | 영어 (100~5,000자) | `summary_text` (요약문)                                                 |
| **유해 표현 분석** | `text-classification` | `unitary/toxic-bert`                               | Apache 2.0 | 영어 (1~1,000자)   | `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate` |

---

## ⚙️ 환경변수 설정 방법 (.env)

프로젝트 최상단 루트에 `.env` 파일을 생성하고 아래 예시를 참고하여 설정해 주세요. (공개 모델을 사용하므로 별도의 허깅페이스 토큰은 필수가 아닙니다.)

env
DEBUG=True
SECRET_KEY=your_django_secret_key_here
HUGGINGFACE_TOKEN=your_optional_token_here

실행 방법 (Installation & Run)

1. 저장소 클론 및 이동

Bash
git clone [https://github.com/사용자이름/Django_GPT.git](https://github.com/사용자이름/Django_GPT.git)
cd Django_GPT 2. 가상환경 생성 및 활성화

Bash
python -m venv venv

# Mac / Linux

source venv/bin/activate

# Windows

venv\Scripts\activate 3. 필수 패키지 설치

Bash
pip install -r requirements.txt 4. 데이터베이스 마이그레이션

Bash
python manage.py makemigrations
python manage.py migrate 5. 관리자 계정 생성 (로그인 테스트용)

Bash
python manage.py createsuperuser 6. 개발 서버 실행

Bash
python manage.py runserver
