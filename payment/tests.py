from django.test import TestCase
from decimal import Decimal

# Create your tests here.


def get_amount_by_percent(percent,amount): 
    "this function gets the amount of a percent on a money"
    return Decimal(percent/100) *(amount)

print(get_amount_by_percent(75,200*2))