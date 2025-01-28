from django.urls import include, path
from rag.views import RagPrompt

app_name = "rag"

urlpatterns = [
    path('prompt/', RagPrompt.as_view()),
]
