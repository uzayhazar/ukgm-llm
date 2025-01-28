from rest_framework import serializers

class PromptSerializer(serializers.Serializer):
    prompt = serializers.CharField(required=True, help_text="The input prompt as a string.")