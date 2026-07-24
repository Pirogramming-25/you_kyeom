from functools import lru_cache
from transformers import pipeline
from .common import get_pipeline_device

@lru_cache(maxsize=1)
def get_moderator_pipeline():
    return pipeline(
        task="text-classification",
        model="unitary/toxic-bert",
        top_k=None,
        device=get_pipeline_device(),
    )

def run_moderator(text):
    moderator = get_moderator_pipeline()
    results = moderator(text)
    # top_k=None인 경우 결과가 [[{...}, {...}, ...]] 형태로 반환될 수 있음
    if isinstance(results, list) and len(results) > 0 and isinstance(results[0], list):
        results = results[0]
    return results