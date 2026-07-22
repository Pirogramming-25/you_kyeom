from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device

@lru_cache(maxsize=1)
def get_summarizer_pipeline():
    return pipeline(
        task="summarization",
        model="sshleifer/distilbart-cnn-6-6",
        device=get_pipeline_device(),
    )

def run_summarizer(text):
    summarizer = get_summarizer_pipeline()
    # 요약 실행 (최소/최대 길이 설정 등)
    result = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return result[0]['summary_text']