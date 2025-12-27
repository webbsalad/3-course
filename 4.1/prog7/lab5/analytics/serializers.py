from rest_framework import serializers
from polls.models import Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'votes']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    total_votes = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'author', 'choices', 'total_votes']
    
    def get_total_votes(self, obj):
        return sum(choice.votes for choice in obj.choices.all())


class QuestionStatsSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    total_votes = serializers.SerializerMethodField()
    choice_percentages = serializers.SerializerMethodField()
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date', 'total_votes', 'choices', 'choice_percentages']
    
    def get_total_votes(self, obj):
        return sum(choice.votes for choice in obj.choices.all())
    
    def get_choice_percentages(self, obj):
        total = self.get_total_votes(obj)
        if total == 0:
            return []
        return [
            {
                'choice_text': choice.choice_text,
                'votes': choice.votes,
                'percentage': round((choice.votes / total) * 100, 2)
            }
            for choice in obj.choices.all()
        ]
