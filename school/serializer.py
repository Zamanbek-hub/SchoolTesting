from rest_framework import serializers
from .models import *


#serilaizer
class pagination_ser(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Question #model

class serializa_answer(serializers.ModelSerializer):
    class Meta:
        fields = ('__all__')
        model = Answer #model


# class TimelineSerializer(serializers.Serializer):
#     tweets = pagination_ser(many=True)
#     articles = serializa_answer(many=True)

    