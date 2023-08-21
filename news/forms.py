from django.forms import ModelForm
from .models import Post
from django import forms


# Создаём модельную форму
class NewsForm(ModelForm):
    # В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами
    class Meta:
        model = Post
        fields = ['author', 'choice', 'header', 'text']
        widgets = {
            'header': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'choice': forms.Select(attrs={
                'class': 'form-control',
            }),
            'author': forms.Select(attrs={
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }
