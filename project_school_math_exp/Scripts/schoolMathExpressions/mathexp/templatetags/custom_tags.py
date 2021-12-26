from django import template, forms
from ..models import  *
from ..forms import *
register = template.Library()
'''
@register.simple_tag
def get_sum_purchase():
    purchase = Purchase.objects.select_related('menu_item').all()
    menu = MenuItem.objects.all()
    price_purchase_list=[]
    for m in menu:
        for p in purchase:
            if m.title == str(p.menu_item):
                price_purchase_list.append(m.price)
    price_purchase_sum = sum(price_purchase_list)
    return price_purchase_sum

@register.simple_tag
def get_class_num(name):
    name_id = name
    if name_id != int:
        classNum = 'test'
        print('class '+classNum)
        return classNum
    else:
        classNum = forms.CharField(queryset=Student.objects.values().filter(pk=name_id)[0]['schoolClassNum'], label='Номер класса')
        print('class '+ classNum)
        return classNum
'''
@register.simple_tag
def get_fields(obj):
    return obj._meta.get_fields()