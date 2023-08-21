from django.forms import ModelForm
from .models import Product
from django import forms


# Создаём модельную форму
class ProductForm(ModelForm):
    # В класс мета, как обычно, надо написать модель, по которой будет строиться форма, и нужные нам поля. Мы уже делали что-то похожее с фильтрами
    class Meta:
        model = Product
        fields = ['name', 'price', 'type', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'price': forms.TextInput(attrs={
                'type': 'number',
                'class': 'form-control',
                'value': 0
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
            }),
        }
