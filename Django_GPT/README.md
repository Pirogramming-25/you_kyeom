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

'''env
DEBUG=True
SECRET_KEY=your_django_secret_key_here
HUGGINGFACE_TOKEN=your_optional_token_here
'''

---

## 🛠 실행 방법 (How to Run)

**1. 가상환경 생성 및 활성화**

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

```

**2. 패키지 설치**

```bash
pip install -r requirments.txt

```

**3. 마이그레이션 (DB 생성)**

```bash
python manage.py makemigrations
python manage.py migrate

```

**4. 서버 실행**

```bash
python manage.py runserver

```
