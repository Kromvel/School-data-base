from django import template
from ..models import  *

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
'''