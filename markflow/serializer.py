from rest_framework import serializers
from markflow.models import Document, Tags


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"


class TagSerializer(serializers.Serializer):
    class Meta:
        model = Tags
        fields = "__all__"