from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device

@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    return pipeline(
        task="text-classification",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        device=get_pipeline_device(),
    )

def run_sentiment(text):
    classifier = get_sentiment_pipeline()
    # top_k=None을 주면 모든 레이블(positive, neutral, negative)의 점수를 다 받을 수 있습니다.
    results = classifier(text, top_k=None)
    return results