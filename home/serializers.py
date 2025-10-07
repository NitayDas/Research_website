from rest_framework import serializers

from .models import *

class StudentSpeechSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentSpeech
        fields = '__all__'



class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'