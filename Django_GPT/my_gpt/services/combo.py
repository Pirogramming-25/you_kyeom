from .summarizer import get_summarizer_pipeline
from .sentiment import get_sentiment_pipeline
from .moderator import get_moderator_pipeline

def run_combo_pipeline(text):
    # 1. 요약 모델 실행
    summarizer = get_summarizer_pipeline()
    # 요약 결과가 다르게 나오도록 do_sample=True 및 파라미터 활용 가능
    summary_result = summarizer(
        text,
        max_length=180,
        min_length=40,
        do_sample=True,
        top_p=0.9,
        temperature=0.8
    )
    summary_text = summary_result[0]['summary_text']

    # 2. 감정 분석 모델 실행 (입력: 요약문)
    classifier = get_sentiment_pipeline()
    sentiment_raw = classifier(summary_text, top_k=None)
    sentiment_scores = {item['label']: round(item['score'] * 100, 2) for item in sentiment_raw}
    # 가장 높은 감정 레이블
    top_sentiment_label = max(sentiment_scores, key=sentiment_scores.get)
    top_sentiment_score = sentiment_scores[top_sentiment_label]

    # 3. 유해 표현 분석 모델 실행 (입력: 요약문)
    moderator = get_moderator_pipeline()
    moderator_raw = moderator(summary_text)
    if isinstance(moderator_raw, list) and len(moderator_raw) > 0 and isinstance(moderator_raw[0], list):
        moderator_raw = moderator_raw[0]
    moderator_scores = {item['label']: round(item['score'] * 100, 2) for item in moderator_raw}
    
    highest_toxic_label = max(moderator_scores, key=moderator_scores.get)
    highest_toxic_score = moderator_scores[highest_toxic_label]

    # 4. 종합 판정 로직 생성
    if top_sentiment_label == "negative":
        sentiment_desc = "부정적인 평가를 포함합니다."
    else:
        sentiment_desc = "강한 부정적 평가는 확인되지 않았습니다."

    if highest_toxic_score >= 50.0:  # 점수 기준 50% 이상
        toxicity_desc = "유해 표현 가능성이 높습니다."
    else:
        toxicity_desc = "심각한 유해 표현 가능성은 낮습니다."

    comprehensive_verdict = f"이 피드백은 {sentiment_desc} 또한 {toxicity_desc}"

    return {
        "summary": summary_text,
        "sentiment": {
            "label": top_sentiment_label,
            "score": top_sentiment_score,
            "all_scores": sentiment_scores
        },
        "toxicity": {
            "highest_label": highest_toxic_label,
            "highest_score": highest_toxic_score,
            "all_scores": moderator_scores
        },
        "verdict": comprehensive_verdict
    }