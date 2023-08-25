from django.forms import ModelForm
from .models import Post
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
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


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get_or_create(name='common')[0]
        basic_group.user_set.add(user)
        return user
