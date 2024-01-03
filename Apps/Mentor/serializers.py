from rest_framework import serializers
from .models import Mentor, Assessment_Questions


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = "__all__"
class AssessmentQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment_Questions 
        fields = ['id','question', 'option_1', 'option_2', 'option_3', 'option_4']
