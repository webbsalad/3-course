from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Q, Sum

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:10]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы не выбрали вариант.'
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class SearchView(generic.TemplateView):
    template_name = 'polls/search.html'


def search_api(request):
    """API для поиска голосований"""
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    sort_by = request.GET.get('sort_by', 'pub_date')
    
    queryset = Question.objects.all()
    
    # Поиск по тексту
    if query:
        queryset = queryset.filter(
            Q(question_text__icontains=query) |
            Q(choices__choice_text__icontains=query)
        ).distinct()
    
    # Фильтрация по дате
    if start_date:
        queryset = queryset.filter(pub_date__gte=start_date)
    if end_date:
        queryset = queryset.filter(pub_date__lte=end_date)
    
    # Сортировка
    if sort_by == 'popularity':
        queryset = queryset.annotate(
            total_votes=Sum('choices__votes')
        ).order_by('-total_votes')
    elif sort_by == 'date':
        queryset = queryset.order_by('-pub_date')
    elif sort_by == 'title':
        queryset = queryset.order_by('question_text')
    
    # Подготавливаем данные для JSON
    results = []
    for question in queryset[:20]:  # Ограничиваем 20 результатами
        total_votes = sum(choice.votes for choice in question.choices.all())
        results.append({
            'id': question.id,
            'question_text': question.question_text,
            'pub_date': question.pub_date.strftime('%Y-%m-%d %H:%M'),
            'author': question.author.username if question.author else 'Anonymous',
            'total_votes': total_votes,
            'choices_count': question.choices.count()
        })
    
    return JsonResponse({'results': results})