import json,requests
from django.conf import settings
import os


class UserPaymentPreparation:


    def __init__(self):
        'allow us to set the amout any time'
        self.amount =0



    """
    this class handles every thing to prepare the user for payment
    it doesnt pay the user it runs fo verication it pass it goes saves the user in the database
    allowing the user to be ready for payment
    it the user Payment class that pays the user
    IT THE ADMIN that will triger the userPayment class
    """


    def get_bankCodeFromJSON(self):
        'this function avoid repeating calling the json file'
        with open('./payment/bankCodes.json','r') as bankCodes:
            return json.loads(bankCodes.read())

   
    def get_available_bank_name(self):
        """
            this method returns a list of available bank names
            javascript will manipulate in such a way that the user will click it 

        """
        allBankCode = self.get_bankCodeFromJSON()
        list_of_bank_names = []
        for bank in allBankCode:
            list_of_bank_names.append(bank.get('name'))

        return list_of_bank_names

    def get_bank_code(self,bankName):

        """
            this method takes in a second parameter called bankName
            js will send a Bank name the user click now we will write a if statment to get the bank code
            THIS WILL RETURN A DICTIONARY THAT CONTAINS THE SPECIFIC BANK CODE  
        """
        
        
        allBankCode = self.get_bankCodeFromJSON()
        correctBank = dict()
        for bank in allBankCode:
            # list_of_bank_names.append(bank.get('name'))
            if bankName == bank.get('name'):
            
                correctBank = bank
                
                # print(bankName,bank.get('name'))
        return correctBank.get('code')

    def create_transfer_recipient(self,data):
        url = f'https://api.paystack.co/transferrecipient'
        headers = {
            'Authorization': 'Bearer '+os.environ.get('PAYSTACK_SECRET'),
            'Content-Type' : 'application/json',
            'Accept': 'application/json',
             "currency": "NGN"
        }
        try:
            resp = requests.post(url,headers=headers,data=json.dumps(data))
            
            return resp.json()
        except requests.exceptions.ConnectionError:
            return {'status':False,'message':'Network Problem'}



    def test_user_account(self,accountNumber,bankCode,Bankname):
        """this test the user account if it valid or not
            not only that if the request was okay it create paystack Transfer recipt
            else it retuns status:false
        """
        # print(accountNumber,bankCode)
        
        url = f'https://api.paystack.co/bank/resolve?account_number={accountNumber}&bank_code={bankCode}'
        headers = {
            'Authorization': 'Bearer '+os.environ.get('PAYSTACK_SECRET'),
            'Content-Type' : 'application/json',
            'Accept': 'application/json',
        }
        try:
            resp = requests.get(url,headers=headers)
            respData = resp.json()


            if respData.get('status') == True:
                # if the user test account passed then we need to create a transfer recipient
                # after we save the recipient,amount to database then the user is ready for payment
                DATA = { "type": Bankname,"name": respData.get('data').get('account_name'),
                "account_number": respData.get('data').get('account_number'),
                "bank_code": bankCode, "currency": "NGN"}

                return self.create_transfer_recipient(DATA)
            
            else:

                return respData

        except requests.exceptions.ConnectionError:
            return {'status':False,'message':'Network Problem'}

    def run(self,bankName,realAcctNum):
        
        bankInfo = self.get_bank_code(bankName)
        PaystackInfo = self.test_user_account(realAcctNum,bankInfo.get('code'),bankName)

        return PaystackInfo

    def transfer_money(self,amount,reference,recipient,metadata=dict()):
        "dont forget to turn off otp in paystack dashbaorad"
        headers = {
            'Authorization': 'Bearer '+os.environ.get('PAYSTACK_SECRET'),
            'Content-Type' : 'application/json',
            'Accept': 'application/json',
        }
        url = 'https://api.paystack.co/transfer'
        data ={ 
                "source": "balance", 
                "amount": int(amount),
                "reference":reference, 
                "recipient": recipient, 
                "reason": "Shop Withdraw",
                'metadata':metadata
            }
        try:
            resp = requests.post(url,headers=headers,data=json.dumps(data))
            respData = resp.json()
            if respData.get('status') == True:
                return {'message':'Transfer has been queued','status':True}
        except requests.exceptions.ConnectionError:
            return {'status':False ,'message':'something went wrong check Your internet and try again in a few min'}

        finally:
            if respData.get('status'): return  {'message': respData.get('message',False),'status':True}
            message = respData.get('message',False)
            
            return {'status':False,'message':message if message  else'something unexpected happened if it happens again react out to our team'}
