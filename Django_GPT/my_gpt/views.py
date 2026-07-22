import json
import logging
from django.http import JsonResponse
from django.shortcuts import render
from .services.sentiment import run_sentiment
from .services.summarizer import run_summarizer
from .services.moderator import run_moderator
from .decorators import model_login_required
from .models import InferenceHistory
from .services.combo import run_combo_pipeline

logger = logging.getLogger(__name__)

def sentiment_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "").strip()
        except Exception:
            text = request.POST.get("text", "").strip()

        if not text:
            return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)
        if len(text) > 1000:
            return JsonResponse({"error": "입력값은 1,000자 이하여야 합니다."}, status=400)

        try:
            raw_results = run_sentiment(text)
            formatted_results = {item['label']: round(item['score'] * 100, 2) for item in raw_results}
            
            # 로그인 유저일 경우 DB 저장
            if request.user.is_authenticated:
                InferenceHistory.objects.create(
                    user=request.user,
                    task=InferenceHistory.Task.SENTIMENT,
                    input_text=text,
                    output_text=str(formatted_results),
                    result_data=formatted_results
                )

            return JsonResponse({"results": formatted_results})
        except Exception:
            logger.exception("Model inference failed.")
            return JsonResponse({"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."}, status=502)

    # GET 요청 시 로그인 유저라면 DB에서 최근 기록 5개 조회
    histories = []
    if request.user.is_authenticated:
        histories = InferenceHistory.objects.filter(
            user=request.user, task=InferenceHistory.Task.SENTIMENT
        )[:5]

    return render(request, "my_gpt/sentiment.html", {"histories": histories})


@model_login_required
def summarize_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "").strip()
        except Exception:
            text = request.POST.get("text", "").strip()

        if len(text) < 100:
            return JsonResponse({"error": "요약할 문서는 100자 이상 입력해주세요."}, status=400)
        if len(text) > 5000:
            return JsonResponse({"error": "문서는 5,000자 이하로 입력해주세요."}, status=400)

        try:
            summary = run_summarizer(text)
            orig_len = len(text)
            sum_len = len(summary)
            ratio = round((sum_len / orig_len) * 100, 2)

            result_data = {
                "original_length": orig_len,
                "summary_length": sum_len,
                "summary_ratio": ratio,
                "summary": summary
            }

            InferenceHistory.objects.create(
                user=request.user,
                task=InferenceHistory.Task.SUMMARIZE,
                input_text=text,
                output_text=summary,
                result_data=result_data
            )

            return JsonResponse(result_data)
        except Exception:
            logger.exception("Summarization failed.")
            return JsonResponse({"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."}, status=502)

    histories = InferenceHistory.objects.filter(
        user=request.user, task=InferenceHistory.Task.SUMMARIZE
    )[:5]
    return render(request, "my_gpt/summarize.html", {"histories": histories})


@model_login_required
def moderate_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "").strip()
        except Exception:
            text = request.POST.get("text", "").strip()

        if not text:
            return JsonResponse({"error": "분석할 문장을 입력해주세요."}, status=400)
        if len(text) > 1000:
            return JsonResponse({"error": "입력값은 1,000자 이하여야 합니다."}, status=400)

        try:
            raw_results = run_moderator(text)
            formatted_results = {item['label']: round(item['score'] * 100, 2) for item in raw_results}
            
            # 가장 위험도가 높은 레이블 찾기
            highest_label = max(formatted_results, key=formatted_results.get)
            highest_score = formatted_results[highest_label]

            result_data = {
                "highest_label": highest_label,
                "highest_score": highest_score,
                "all_scores": formatted_results
            }

            InferenceHistory.objects.create(
                user=request.user,
                task=InferenceHistory.Task.MODERATE,
                input_text=text,
                output_text=f"Highest: {highest_label} ({highest_score}%)",
                result_data=result_data
            )

            return JsonResponse(result_data)
        except Exception:
            logger.exception("Moderation failed.")
            return JsonResponse({"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."}, status=502)

    histories = InferenceHistory.objects.filter(
        user=request.user, task=InferenceHistory.Task.MODERATE
    )[:5]
    return render(request, "my_gpt/moderate.html", {"histories": histories})

@model_login_required
def combo_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "").strip()
        except Exception:
            text = request.POST.get("text", "").strip()

        if len(text) < 200:
            return JsonResponse({"error": "복합 분석 피드백은 200자 이상 입력해주세요."}, status=400)
        if len(text) > 5000:
            return JsonResponse({"error": "문서는 5,000자 이하로 입력해주세요."}, status=400)

        try:
            # 복합 분석 파이프라인 실행 (Chaining)
            result_data = run_combo_pipeline(text)

            # 실행 기록 저장 (재생성 시에도 새로운 기록으로 저장)
            InferenceHistory.objects.create(
                user=request.user,
                task=InferenceHistory.Task.COMBO,
                input_text=text,
                output_text=result_data["summary"],
                result_data=result_data
            )

            return JsonResponse(result_data)
        except Exception:
            logger.exception("Combo pipeline failed.")
            return JsonResponse({"error": "모델 실행에 실패했습니다. 잠시 후 다시 시도해주세요."}, status=502)

    histories = InferenceHistory.objects.filter(
        user=request.user, task=InferenceHistory.Task.COMBO
    )[:5]
    return render(request, "my_gpt/combo.html", {"histories": histories})