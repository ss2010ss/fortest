from django import forms
from helloapp.models import textsfortest

class TextForm(forms.ModelForm):
    class Meta:
        model = textsfortest
        fields = ['text', 'parenttext', 'weight']  # Указываем поля формы
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цитату',
                'rows': 4,
            }),
            'parenttext': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Источник текста ',
            }),
            
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите вес',
            }),
        }
        labels = {
            'text': 'Текст цитаты',
            'parenttext': 'Источник текста',
        
            'weight': 'Вес',
        }