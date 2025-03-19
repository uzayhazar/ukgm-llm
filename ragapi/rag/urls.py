from django.urls import include, path
from rag.views import RagPromptTest, RagPrompt

from .views import logout_view, dummy, google_login_redirect

app_name = "rag"

urlpatterns = [
    path('prompt_internal/', RagPromptTest.as_view()),
    path('prompt/', RagPrompt.as_view()),
    path('google/login/', google_login_redirect, name='google_login_redirect'),
    path('logout/', logout_view, name='logout'),
    path('testt/', dummy, name='testt')
]
