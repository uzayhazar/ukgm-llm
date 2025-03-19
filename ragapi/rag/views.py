import requests
import os

from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication
from rag.authentication import CsrfExemptSessionAuthentication 
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view

from rag.serializers import PromptSerializer
# from rag_model.rag_implementation import RAGChat


class RagPromptTest(LoginRequiredMixin, APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PromptSerializer

    @swagger_auto_schema(
        # security=[{'SessionAuth': []}],  # Inform Swagger that authentication is required
        request_body=PromptSerializer,
        responses={
            200: openapi.Response(description="Success"),
            400: openapi.Response(description="Invalid Input"),
            401: openapi.Response(description="Unauthorized"),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = PromptSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract 'prompt' from validated data
        prompt = serializer.validated_data['prompt']

        # Use the prompt in your RAGChat logic
        query_result = "ranndommm"
        # rag = RAGChat(prompt)
        # query_result = rag.generate_response_with_gptj()
        return Response(query_result, status=status.HTTP_200_OK)
    
    # def get(self, request, *args, **kwargs):
    #     query = request.GET.get('query')
    #     rag = RAGChat(query)
    #     query_result = rag.generate_response_with_gptj()
    #     # query_result = """
    #     # Lieber Patient,

    #     # danke, dass Sie mich konsultiert haben. Ein wesentlicher Risikofaktor für die Entwicklung des Mundhöhlenkarzinoms sind Alkoholkonsum und Tabakkonsum. Der Alkoholkonsum und der Tabakkonsum können entweder einzeln oder in Kombination auftreten und das Risiko für Mundhöhlenkarzinom signifikant erhöhen. Eine verbesserte Aufklärung über Anzeichen, Symptome und Risikofaktoren des Mundhöhlenkarzinoms kann bei der Früherkennung und Behandlung dieser Erkrankung hilfreich sein.

    #     # Ich hoffe, ich konnte Ihre Frage zufriedenstellend beantworten. Wenn Sie noch weitere Fragen haben, zögern Sie bitte nicht, mich zu kontaktieren.

    #     # Mit freundlichen Grüßen,
    #     # [Ihr Name]
    #     # """
    #     return Response(query_result, status=status.HTTP_200_OK)

class RagPrompt(LoginRequiredMixin, APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PromptSerializer

    @swagger_auto_schema(
        # security=[{'SessionAuth': []}],  # Inform Swagger that authentication is required
        request_body=PromptSerializer,
        responses={
            200: openapi.Response(description="Success"),
            400: openapi.Response(description="Invalid Input"),
            401: openapi.Response(description="Unauthorized"),
        },
    )
    def post(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        serializer = PromptSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract 'prompt' from validated data
        prompt = serializer.validated_data['prompt']

        AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY") 

        endpoint = "https://openaiwestus001.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-08-01-preview"
        parameters = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps people with breast cancer treatment decision making. Provide reliable information backed by medical guidelines."
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": "https://aisearchrag0001.search.windows.net/",
                        "index_name": "indexpdfguidelines",
                        "authentication": {
                            "type": "system_assigned_managed_identity",
                        },
                        "query_type": "vector_semantic_hybrid",
                        "embedding_dependency": {
                                "type": "deployment_name",
                                "deployment_name": "text-embedding-ada-002"
                            },
                        "semantic_configuration": "default"
                    },
                },
            ],
        }
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_API_KEY,
        }
        try:
            response = requests.post(endpoint, headers=headers, json=parameters)
            if response.status_code == 200:
                query_result =  response.json()
            else:
                query_result = None
                print("Error:", response.status_code, response.text)
        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
        return Response(query_result, status=status.HTTP_200_OK)

def google_login_redirect(request):
    """Redirect user to Google login via allauth."""
    return redirect('/accounts/google/login/')

@api_view(['GET'])
def logout_view(request):
    """Log out the user by clearing the session."""
    logout(request)
    response = Response({"message": "Logged out successfully"}, status=200)

    response.delete_cookie('sessionid')
    # response.delete_cookie('csrftoken')

    return response

@api_view(['GET'])
@login_required
def dummy(request):
    response = Response({"message": "ranndomm"}, status=200)

    return response