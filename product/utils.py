import random
from .models import Order
letters = [
  'A',
  'B',
  'C',
  'D',
  'E',
  'F',
  'G',
  'H',
  'I',
  'J',
  'K',
  'L',
  'M',
  'N',
  'O',
  'P',
  'Q',
  'R',
  'S',
  'T',
  'U',
  'V',
  'W',
  'X',
  'Y',
  'Z',
]

def getUniqueId():
    isUnique = False
    while not isUnique:
        word = letters[random.randint(1, len(letters)-1)] + letters[random.randint(1, len(letters)-1)]
        number = random.randint(10000,99999)
        orderId = str(number) + word
        try:
            Order.objects.get(orderId=orderId)
        except Order.DoesNotExist:
            isUnique = True
    return orderId




