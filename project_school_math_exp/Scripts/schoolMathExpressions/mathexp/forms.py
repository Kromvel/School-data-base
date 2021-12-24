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




