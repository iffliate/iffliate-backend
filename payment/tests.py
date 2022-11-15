from django.test import TestCase
from decimal import Decimal

# Create your tests here.


a = {'event': 'transfer.success',
 'data': {'amount': 100, 'createdAt': '2022-11-15T22:56:54.000Z', 'currency': 'NGN',
  'domain': 'test', 'failures': None, 
  'id': 202783608, 
  'integration': {'id': 730834, 'is_live': True, 'business_name': 'savvyschools',
   'logo_path': 'https://public-files-paystack-prod.s3.eu-west-1.amazonaws.com/integration-logos/paystack.jpg'},
    'reason': 'Shop Withdraw', 'reference': 'elspetbflr', 'source': 'balance', 'source_details': None, 
    'status': 'success', 'titan_code': None, 'transfer_code': 'TRF_njhedyrormomfods', 'transferred_at': None, 'updatedAt': '2022-11-15T22:56:54.000Z',
     'recipient': {'active': True, 'createdAt': '2022-11-05T23:23:57.000Z', 'currency': 'NGN', 'description': None, 'domain': 'test', 'email': None, 'id': 42160415, 'integration': 730834, 'metadata': None, 'name': 'OGECHUKWU MATTHEW NWOKOLO', 'recipient_code': 'RCP_f1aaswov5781pa9', 'type': 'nuban', 'updatedAt': '2022-11-05T23:23:57.000Z', 'is_deleted': False, 'details': {'authorization_code': None, 'account_number': '2209134092', 'account_name': 'OGECHUKWU MATTHEW NWOKOLO', 'bank_code': '057', 'bank_name': 'Zenith Bank'}}, 'session': {'provider': None, 'id': None}, 'fee_charged': 0}}


print(a['data']['recipient']['recipient_code'])