#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from polls.models import Question, Choice
from django.utils import timezone
import datetime

questions_data = [
    {
        'question_text': 'Какой язык программирования вы предпочитаете?',
        'choices': ['Python', 'JavaScript', 'Java', 'C++', 'Go']
    },
    {
        'question_text': 'Какой фреймворк для веб-разработки лучше?',
        'choices': ['Django', 'Flask', 'FastAPI', 'Express.js', 'Spring Boot']
    },
    {
        'question_text': 'Какой тип данных вы используете чаще всего?',
        'choices': ['Строки', 'Числа', 'Списки', 'Словари', 'Объекты']
    },
    {
        'question_text': 'Какой редактор кода вы предпочитаете?',
        'choices': ['VS Code', 'PyCharm', 'Sublime Text', 'Vim', 'Atom']
    },
    {
        'question_text': 'Какой способ развертывания приложений вы используете?',
        'choices': ['Docker', 'Виртуальные машины', 'Облачные сервисы', 'Локальный сервер', 'Serverless']
    }
]

for i, q_data in enumerate(questions_data):
    question = Question.objects.create(
        question_text=q_data['question_text'],
        pub_date=timezone.now() - datetime.timedelta(days=i*2)
    )
    
    for j, choice_text in enumerate(q_data['choices']):
        import random
        votes = random.randint(0, 50)
        Choice.objects.create(
            question=question,
            choice_text=choice_text,
            votes=votes
        )

print("Тестовые данные созданы успешно!")
print(f"Создано {Question.objects.count()} голосований")
print(f"Создано {Choice.objects.count()} вариантов ответов")
