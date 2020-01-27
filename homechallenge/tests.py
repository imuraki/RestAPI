import json
from django.test import TestCase
from rest_framework.test import APITestCase, APITransactionTestCase, APISimpleTestCase 
from rest_framework import status

# Create your tests here.

class LoanApplicationTestCase(APITestCase):

    def setUp(self):
        self.data={
            "AppID": 1,
            "RequestHeader": {
                "CFRequestId": "555",
                "RequestDate": "2020-01-24T06:55:34.626038Z",
                "CFApiUserId": "akhil",
                "CFApiPassword": "123456",
                "IsTestLead": True
            },
            "Business": {
                "Name": "ufy",
                "SelfReportedCashFlow": {
                    "AnnualRevenue": 23.52,
                    "MonthlyAverageBankBalance": 41.25,
                    "MonthlyAverageCreditCardVolume": 60.32
                },
                "Address": {
                    "Address1": "212 Barton Creek Drive D",
                    "Address2": "kk",
                    "City": "Charlotte",
                    "State": "NC",
                    "Zip": "28262"
                },
                "TaxID": "555",
                "Phone": "+1 09804300626",
                "NAICS": "hhh",
                "HasBeenProfitable": True,
                "HasBankruptedInLast7Years": False,
                "InceptionDate": "2020-01-06T06:00:00Z"
            },
            "Owners": [
                {
                    "Name": "Akhil Chundarathil",
                    "FirstName": "Akhil",
                    "LastName": "Chundarathil",
                    "Email": "akhilkc9@gmail.com",
                    "HomeAddress": {
                        "Address1": "House No 906, 6th A Main road",
                        "Address2": "Near Wipro park signal",
                        "City": "BANGALORE",
                        "State": "KARNATAKA",
                        "Zip": "560034"
                    },
                    "DateOfBirth": "2020-01-29T00:00:00Z",
                    "HomePhone": "+1 09804300626",
                    "SSN": "12345",
                    "PercentageOfOwnership": 6.0
                },
                {
                    "Name": "ANOOP CHUNDARATHIL",
                    "FirstName": "ANOOP",
                    "LastName": "CHUNDARATHIL",
                    "Email": "anoopc8171@outlook.com",
                    "HomeAddress": {
                        "Address1": "Room no 201,Saravana Inn,Near Bells hotel,Saravanampatti",
                        "Address2": "pp",
                        "City": "Coimbatore",
                        "State": "TAMIL NADU",
                        "Zip": "641035"
                    },
                    "DateOfBirth": "2020-01-05T12:00:00Z",
                    "HomePhone": "09629031744",
                    "SSN": "1234555",
                    "PercentageOfOwnership": 8.0
                },
                {
                    "Name": "SAVE THE CHILDREN",
                    "FirstName": "SAVE",
                    "LastName": "CHILDREN",
                    "Email": "anoopc8171@outlook.com",
                    "HomeAddress": {
                        "Address1": "JAnaki nivas, thekkethara",
                        "Address2": "kavassery po",
                        "City": "Palakkad",
                        "State": "Kerala",
                        "Zip": "678543"
                    },
                    "DateOfBirth": "2020-01-06T18:00:00Z",
                    "HomePhone": "09629031744",
                    "SSN": "555",
                    "PercentageOfOwnership": 20.0
                }
            ],
            "CFApplicationData": {
                "RequestedLoanAmount": "5555555555555",
                "StatedCreditHistory": 888,
                "LegalEntityType": "llc",
                "FilterID": "kkk"
            }}
        self.maxDiff = None

    def test_postloanapplication(self):
        response = self.client.post('/loanapp/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {
                "status": 'OK',
                "AppID": 1,
                "Location": "http://127.0.0.1:8000/loanapp/1"
            })
        
        response = self.client.post('/loanapp/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_postduplicateloanapplication(self):
        response = self.client.post('/loanapp/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        #Duplicate information by assuimg each user has unique userid, using which they try to submit multiple applications.
        # In case of duplication, only fields data is not overwritten, only fields that are changed are updated  
        self.data['AppID'] = 2
        self.data['RequestHeader']['CFApiUserId'] = 'akhil'
        self.data['Business']['SelfReportedCashFlow']['AnnualRevenue'] = 20.50
        self.data['Business']['Phone'] = 9567959971

        response = self.client.post('/loanapp/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {
                "status": 'OK',
                "AppID": 1,
                "Location": "http://127.0.0.1:8000/loanapp/1"
            })

        #Lets see if the returned old application has the fields updated
        response = self.client.get('/loanapp/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['Business']['SelfReportedCashFlow']['AnnualRevenue'], 20.50)
        self.assertEqual(json.loads(response.content.decode('utf-8'))['Business']['Phone'], '9567959971')




    def test_getloanapplication(self):
        self.client.post('/loanapp/', self.data, format='json')
        response = self.client.get('/loanapp/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/loanapp/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/loanapp/2')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {
                'status': 'Resource Not Found'
            })
    
    def test_getstatus(self):
        self.client.post('/loanapp/', self.data, format='json')
        response = self.client.get('/status/?loanappid=1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {
            'data':{
                'AppID':1,
                'Status':'Submitted',
                'loanapplication':  "http://127.0.0.1:8000/loanapp/1"
            }
        })

        response = self.client.get('/status/?loanappid=2')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {
                'status': 'Resource Not Found'
            })

    def test_deleteloanapplication(self):
        self.client.post('/loanapp/', self.data, format='json')
        response = self.client.delete('/loanapp/1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content.decode('utf-8')), {
                'status': 'NO CONTENT'
            })


