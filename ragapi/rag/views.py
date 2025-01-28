# from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rag.serializers import PromptSerializer
from rag_model.rag_implementation import RAGChat


# User = get_user_model()
from rest_framework import serializers

class PromptSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True, help_text="The input prompt as a string.")

class RagPrompt(APIView):
    # permission_classes = (permissions.IsAuthenticated,)
    @swagger_auto_schema(
        request_body=PromptSerializer,  # This tells Swagger about the input
        responses={
            200: openapi.Response(
                description="Successful response",
                examples={
                    "application/json": {"result": "Generated response from RAGChat."},
                },
            ),
            400: openapi.Response(
                description="Invalid input",
                examples={
                    "application/json": {"error": "Missing 'prompt' in the request body"},
                },
            ),
        },
    )

    # def post(self, request, *args, **kwargs):

    #     authorize_url = None
    #     return Response(authorize_url, status=status.HTTP_200_OK)
    def post(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        serializer = PromptSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract 'prompt' from validated data
        prompt = serializer.validated_data['prompt']

        # Use the prompt in your RAGChat logic
        rag = RAGChat(prompt)
        query_result = rag.generate_response_with_gptj()
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