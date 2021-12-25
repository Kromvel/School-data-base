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
    
    name = forms.ModelChoiceField(queryset=Student.objects.all())
    mathExpression = forms.CharField(max_length= 255, label='Математическое выражение')
    def clean_mathExpression(self):
        checkSymbols = '0123456789+-*/.^()'
        parenthesis = '()'
        data = self.cleaned_data['mathExpression']
        for i in data:
            parenthesisCount = 0
            if i not in checkSymbols:
                raise forms.ValidationError("В выражении есть некорректный символ, например: {}".format(i))
            elif i in parenthesis:
                parenthesisCount += 1
                if parenthesisCount % 2 != 0:
                    raise forms.ValidationError("Количество скобок нечетное")
            elif data.isalpha() == False:
                pass
        return data
    
    def __init__(self, *args, **kwargs):
        super(MathExpressionsForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['mathExpression'].widget.attrs.update({'class': 'form-control'})
    
    


