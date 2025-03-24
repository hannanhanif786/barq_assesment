from django.urls import path
from markflow.views import DocumentView, LoginView


urlpatterns = [
    path("login", LoginView.as_view()),
    path("", DocumentView.as_view()),
]