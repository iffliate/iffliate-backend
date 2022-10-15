


from decimal import Decimal


def convert_naira_to_kobo(naira):
    naira = float(naira)*100
    kobo = int(naira)
    return kobo




def get_amount_by_percent(percent,amount): 
    "this function gets the amount of a percent on a money"
    return Decimal(percent/100) *(amount)