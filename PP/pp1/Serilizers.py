from rest_framework import serializers
from .models import User, Paragraph, WordIndex

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = '__all__'

class WordIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordIndex
        fields = '__all__'
