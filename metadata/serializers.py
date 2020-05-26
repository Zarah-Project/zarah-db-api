from rest_framework import serializers

from metadata.models import ClassificationField, ClassificationCategory, ConsentType


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ClassificationFieldListSerializer(serializers.ModelSerializer):
    field_id = serializers.IntegerField(source='id')
    category_key = serializers.SlugRelatedField(queryset=ClassificationCategory.objects.all(),
                                                slug_field='key', source='category')
    children = RecursiveSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = ClassificationField
        fields = ('field_id', 'category', 'category_key', 'field_type', 'field', 'full_name', 'children')


class ConsentFieldsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsentType
        fields = ('id', 'key', 'type')
