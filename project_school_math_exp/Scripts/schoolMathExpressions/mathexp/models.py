# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.urls import reverse

# Create your models here.
class Student(models.Model):
    def current_year():
        return datetime.date.today().year
    def max_value_current_year(value):
        return MaxValueValidator(Student.current_year())(value)
    WITHOUT_CLASS = 'класс не выбран'
    MEASURE_CHOICES_CLASS_NUM = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11')
    ]
    MEASURE_CHOICES_CLASS_NAME = [
        ('А', 'А'),
        ('Б', 'Б'),
        ('В', 'В'),
    ]
    
    
    name = models.CharField(max_length=255)
    birthDate = models.DateField()
    admissionYear = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])
    schoolClassNum = models.CharField(max_length=5, choices=MEASURE_CHOICES_CLASS_NUM, default=WITHOUT_CLASS)
    schoolClassName = models.CharField(max_length=25, choices=MEASURE_CHOICES_CLASS_NAME, default=WITHOUT_CLASS)
    
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('studentlist')

    class Meta:
        ordering = ['name']

class MathExpressions(models.Model):
    def validate_even(value):
        if value > 1 or value < 0 or type(value) != int:
            raise ValidationError(_('%(value)s недопустимое значение: должно быть 0 или 1'), params={'value': value})
    
    name = models.ForeignKey(Student, on_delete=models.CASCADE)
    mathExpression = models.CharField(max_length=255)
    validExpression = models.PositiveIntegerField(default=0, validators=[validate_even])
    nonvalidExpression = models.PositiveIntegerField(default=0, validators=[validate_even])
    validMathResolve = models.PositiveIntegerField(default=0, validators=[validate_even])
    nonvalidMathResolve = models.PositiveIntegerField(default=0, validators=[validate_even])
    def __str__(self):
        return str(self.name)