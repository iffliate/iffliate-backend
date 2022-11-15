
from decimal import Decimal
import random
import string

def convert_naira_to_kobo(naira):
    naira = float(naira)*100
    kobo = int(naira)
    return kobo




def get_amount_by_percent(percent,amount): 
    "this function gets the amount of a percent on a money"
    return Decimal(percent/100) *(amount)

def generate_n(number:int=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(number))