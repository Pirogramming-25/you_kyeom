
from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/sentiment/", permanent=False), name="index"),
    path("sentiment/", views.sentiment_view, name="sentiment"),
    path("summarize/", views.summarize_view, name="summarize"),
    path("moderate/", views.moderate_view, name="moderate"),
    path("combo/", views.combo_view, name="combo"),
]