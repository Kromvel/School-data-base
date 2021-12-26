from django import forms
from django.forms.models import ModelForm
from .models import *



class Loginform(forms.Form):
    username = forms.CharField(max_length= 25,label="Введите имя пользователя")
    password = forms.CharField(max_length= 30, label='Введите пароль', widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(Loginform, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'birthDate','admissionYear','schoolClassNum','schoolClassName']
        labels = {
        "name": "ФИО",
        "birthDate": "Дата рождения",
        "admissionYear": "Год поступления",
        'schoolClassNum': "Номер класса",
        'schoolClassName': "Буква класса",
    }
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['birthDate'].widget.attrs.update({'class': 'form-control'})
        self.fields['admissionYear'].widget.attrs.update({'class': 'form-control'})
        self.fields['schoolClassNum'].widget.attrs.update({'class': 'form-control'})
        self.fields['schoolClassName'].widget.attrs.update({'class': 'form-control'})


class MathExpressionsForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Student.objects.all(), label='Выберите ученика')
    mathExpression = forms.CharField(max_length= 255, label='Пропишите математическое выражение')
    ResolveNumber = forms.CharField(label='Укажите ответ')

    def clean_mathExpression(self):
        data = self.cleaned_data['mathExpression']
        return data
    
    def __init__(self, *args, **kwargs):
        super(MathExpressionsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['mathExpression'].widget.attrs.update({'class': 'form-control'})
        self.fields['ResolveNumber'].widget.attrs.update({'class': 'form-control'})

class MathExpressionsListForm(forms.Form):
    #name = forms.ModelChoiceField(empty_label='Choose category', queryset=Student.objects.all(), initial='Все ученики', label='Выберите ученика')
    name = forms.ChoiceField(choices=Student.objects.values_list('name', flat=True))
    def __init__(self, *args, **kwargs):
        super(MathExpressionsListForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

    
    


