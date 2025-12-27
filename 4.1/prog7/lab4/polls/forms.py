from django import forms


class PollCreateForm(forms.Form):
    question_text = forms.CharField(max_length=200, label='Заголовок вопроса')
    choices_text = forms.CharField(
        widget=forms.Textarea,
        label='Варианты ответа (каждый с новой строки)'
    )
