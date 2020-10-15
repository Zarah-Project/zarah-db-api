from rest_framework import serializers
from document.models import Document


class DocumentReadPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title')
