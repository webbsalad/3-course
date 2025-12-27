import base64
import io
import json
import csv
from datetime import datetime, timedelta

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio

from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count, Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from polls.models import Question, Choice
from .serializers import QuestionSerializer, QuestionStatsSerializer


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        queryset = Question.objects.all()
        
        # Фильтрация по дате
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(pub_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(pub_date__lte=end_date)
        
        # Сортировка
        sort_by = self.request.query_params.get('sort_by', 'pub_date')
        order = self.request.query_params.get('order', 'desc')
        
        if sort_by == 'popularity':
            # Сортируем по общему количеству голосов
            queryset = queryset.annotate(
                total_votes=Sum('choices__votes')
            ).order_by(f'-total_votes' if order == 'desc' else 'total_votes')
        elif sort_by == 'date':
            queryset = queryset.order_by(f'-pub_date' if order == 'desc' else 'pub_date')
        elif sort_by == 'title':
            queryset = queryset.order_by(f'-question_text' if order == 'desc' else 'question_text')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Общая статистика по всем голосованиям"""
        total_questions = Question.objects.count()
        total_votes = sum(
            sum(choice.votes for choice in question.choices.all())
            for question in Question.objects.all()
        )
        
        # Статистика по датам
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        questions_this_week = Question.objects.filter(pub_date__gte=week_ago).count()
        questions_this_month = Question.objects.filter(pub_date__gte=month_ago).count()
        
        return Response({
            'total_questions': total_questions,
            'total_votes': total_votes,
            'questions_this_week': questions_this_week,
            'questions_this_month': questions_this_month,
        })
    
    @action(detail=True, methods=['get'])
    def detailed_stats(self, request, pk=None):
        """Детальная статистика по конкретному голосованию"""
        question = self.get_object()
        serializer = QuestionStatsSerializer(question)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def chart(self, request, pk=None):
        """Генерация диаграммы для голосования"""
        question = self.get_object()
        chart_type = request.query_params.get('type', 'bar')
        
        choices = question.choices.all()
        if not choices.exists():
            return Response({'error': 'Нет данных для отображения'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        choice_texts = [choice.choice_text for choice in choices]
        votes = [choice.votes for choice in choices]
        
        if chart_type == 'bar':
            # Столбчатая диаграмма с matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))
            bars = ax.bar(choice_texts, votes, color='skyblue', edgecolor='navy')
            
            # Добавляем значения на столбцы
            for bar, vote in zip(bars, votes):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{vote}', ha='center', va='bottom')
            
            ax.set_title(f'Результаты голосования: {question.question_text}')
            ax.set_xlabel('Варианты ответа')
            ax.set_ylabel('Количество голосов')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Сохраняем в base64
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode()
            plt.close()
            
            return Response({
                'chart_type': 'bar',
                'image_base64': image_base64,
                'question_text': question.question_text,
                'data': list(zip(choice_texts, votes))
            })
        
        elif chart_type == 'pie':
            # Круговая диаграмма с plotly
            fig = go.Figure(data=[go.Pie(labels=choice_texts, values=votes)])
            fig.update_layout(title=f'Результаты голосования: {question.question_text}')
            
            # Конвертируем в HTML
            chart_html = pio.to_html(fig, include_plotlyjs=False, output_type='div')
            
            return Response({
                'chart_type': 'pie',
                'chart_html': chart_html,
                'question_text': question.question_text,
                'data': list(zip(choice_texts, votes))
            })
        
        return Response({'error': 'Неподдерживаемый тип диаграммы'}, 
                      status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        """Экспорт данных в CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="polls_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Question ID', 'Question Text', 'Publication Date', 'Author', 'Choice Text', 'Votes'])
        
        for question in self.get_queryset():
            for choice in question.choices.all():
                writer.writerow([
                    question.id,
                    question.question_text,
                    question.pub_date.strftime('%Y-%m-%d %H:%M:%S'),
                    question.author.username if question.author else 'Anonymous',
                    choice.choice_text,
                    choice.votes
                ])
        
        return response
    
    @action(detail=False, methods=['get'])
    def export_json(self, request):
        """Экспорт данных в JSON"""
        serializer = QuestionSerializer(self.get_queryset(), many=True)
        return JsonResponse(serializer.data, safe=False)