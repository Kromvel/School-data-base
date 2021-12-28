from django import forms
from django.forms.models import ModelForm
from .models import *
from django.contrib.auth.models import User

class Loginform(forms.Form):
    # форма для авторизации
    def __init__(self, *args, **kwargs):
        super(Loginform, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        
    username = forms.CharField(max_length= 25,
                               label="Введите имя пользователя"
                               )
    password = forms.CharField(max_length= 30,
                               label='Введите пароль',
                               widget=forms.PasswordInput
                               )

class StudentForm(ModelForm):
    # форма для списка учеников
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['birthDate'].widget.attrs.update({'class': 'form-control'})
        self.fields['admissionYear'].widget.attrs.update({'class': 'form-control'})
        self.fields['schoolClassNum'].widget.attrs.update({'class': 'form-control'})
        self.fields['schoolClassName'].widget.attrs.update({'class': 'form-control'})
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

class MathExpressionsForm(forms.Form):
    # форма для прописывания математического выражения
    def __init__(self,  *args, **kwargs):
        super(MathExpressionsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['mathExpression'].widget.attrs.update({'class': 'form-control'})
        self.fields['ResolveNumber'].widget.attrs.update({'class': 'form-control'})
        
    name = forms.ModelChoiceField(queryset=Student.objects.all().exclude(pk=6),
                                  label='Выберите ученика'
                                  )
    mathExpression = forms.CharField(max_length= 255,
                                     label='Пропишите математическое выражение'
                                     )
    ResolveNumber = forms.CharField(label='Укажите ответ')    
        


class MathExpressionsListForm(forms.Form):
     # форма для вывода результатов учеников
    def __init__(self, *args, **kwargs):
        super(MathExpressionsListForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        
    name = forms.ModelChoiceField(empty_label='Ученики',
                                  queryset=Student.objects.all(),
                                  initial='Все ученики',
                                  label='Выберите ученика'
                                  )
    

    
    


