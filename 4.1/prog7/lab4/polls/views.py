from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from .models import Question, Choice
from .forms import PollCreateForm


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


@method_decorator(login_required, name='dispatch')
class PollCreateView(generic.FormView):
    template_name = 'polls/create.html'
    form_class = PollCreateForm

    def form_valid(self, form):
        question = Question.objects.create(
            question_text=form.cleaned_data['question_text'],
            author=self.request.user,
            pub_date=timezone.now(),
        )
        raw_choices = form.cleaned_data['choices_text']
        for line in raw_choices.splitlines():
            text = line.strip()
            if text:
                Choice.objects.create(question=question, choice_text=text)
        return redirect('polls:detail', pk=question.pk)

from django.shortcuts import render

# Create your views here.
