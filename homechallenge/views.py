from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import LoanApplication, RequestHeaderModel, BusinessModel, AddressModel, HomeAddressModel, OwnersModel, SelfReportedCashFlowModel, CFApplicationDataModel
from .serializers import LoanApplicationSerializer
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
class get_delete_update_movie(RetrieveUpdateDestroyAPIView):
    serializer_class = LoanApplicationSerializer

    def get_queryset(self, pk):
        try:
            loanapplication = LoanApplication.objects.get(AppID=pk)
        except ObjectDoesNotExist:
            return None             
        return loanapplication

    # Get a loanapplication
    def get(self, request, pk):

        loanapplication = self.get_queryset(pk)
        if loanapplication != None:
            loanapplication.RequestHeader = RequestHeaderModel.objects.get(loanapplication=loanapplication)
            loanapplication.Business = BusinessModel.objects.get(loanapplication=loanapplication)
            loanapplication.Business.Address = AddressModel.objects.get(business=loanapplication.Business)
            loanapplication.Business.SelfReportedCashFlow = SelfReportedCashFlowModel.objects.get(business=loanapplication.Business)
            loanapplication.Owners = OwnersModel.objects.filter(loanapplication=loanapplication)
            for eachOwner in loanapplication.Owners:
                    eachOwner.HomeAddress = HomeAddressModel.objects.get(owner=eachOwner)
            loanapplication.CFApplicationData = CFApplicationDataModel.objects.get(loanapplication=loanapplication)
            serializer = LoanApplicationSerializer(loanapplication)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            content = {
                'status': 'Resource Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)


# Update a loanapplication
    def put(self, request, pk):
        
        loanapplication = self.get_queryset(pk)
        serializer = LoanApplicationSerializer(loanapplication, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # Delete a loanapplication
    def delete(self, request, pk):

        loanapplication = self.get_queryset(pk)

        if loanapplication != None:
            loanapplication.delete()
            content = {
                'status': 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {
                'status': 'Resource Not Found'
            }
            Response(content, status=status.HTTP_404_NOT_FOUND)
   
# Create your views here.
class get_post_movies(ListCreateAPIView):
    serializer_class = LoanApplicationSerializer

    def returnModelObject(self, modelObj, key):
        if key == 'RequestHeader':
            return modelObj.RequestHeader
        elif key == 'Business':
            return modelObj.Business
        elif key == 'SelfReportedCashFlow':
            return modelObj.SelfReportedCashFlow
        elif key == 'Address':
            return modelObj.Address
        elif key == 'HomeAddress':
            return modelObj.HomeAddress
        elif key == 'CFApplicationData':
            return modelObj.CFApplicationData

    #Find the Change in the fields and update only those respective instances of Database. Algorithm to update only change in the fields(Task 3)
    def update(self, a, b, modelObj):
        for key in list(b.keys()):
            if(isinstance(b[key], dict) == False and isinstance(b[key], list) == False):
                if(a[key] != b[key]):
                    setattr(modelObj, key, b[key])
                    modelObj.save()
                    print("key = "+ str(key) + " value = " + str(b[key]))
            elif(isinstance(b[key], dict) == False):
                if(len(a[key]) >= len(b[key])):
                    for i in range(0,len(b[key])):
                        self.update(a[key][i], b[key][i], modelObj.Owners[i])
                    for r in range(i+1, len(a[key])):
                        modelObj.Owners[r].delete()
                else:
                    for i in range(0,len(a[key])):
                        self.update(a[key][i], b[key][i], modelObj.Owners[i])
                    for r in range(i+1, len(b[key])):
                        HomeAddress_data = b[key][r].pop('HomeAddress')
                        Owner = OwnersModel.objects.create(**b[key][r], loanapplication=modelObj)
                        HomeAddressModel.objects.create(**HomeAddress_data, owner=Owner)                      
            else:
                nestedmodelObj = self.returnModelObject(modelObj, key)
                self.update(a[key], b[key], nestedmodelObj) 
    
    def get_queryset(self):
        try:
            loanapplications = LoanApplication.objects.all()
        except ObjectDoesNotExist:
            return None
        return loanapplications

    # Get all loanapplications
    def get(self, request):
        loanapplications = self.get_queryset()
        if loanapplications != None:
            for each in loanapplications:
                each.RequestHeader = RequestHeaderModel.objects.get(loanapplication=each)
                each.Business = BusinessModel.objects.get(loanapplication=each)
                each.Business.Address = AddressModel.objects.get(business=each.Business)
                each.Business.SelfReportedCashFlow = SelfReportedCashFlowModel.objects.get(business=each.Business)
                each.Owners = OwnersModel.objects.filter(loanapplication=each)
                for eachOwner in each.Owners:
                    eachOwner.HomeAddress = HomeAddressModel.objects.get(owner=eachOwner)
                each.CFApplicationData = CFApplicationDataModel.objects.get(loanapplication=each)

            serializer = self.serializer_class(loanapplications, many=True)
            content = {
                'data': serializer.data
            }
            return Response(content, status=status.HTTP_200_OK)
        else:
            content = {
                'status': 'Resource Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        

    # Create a new loanapplication
    def post(self, request):
        serializer = LoanApplicationSerializer(data=request.data)   
        if serializer.is_valid():
            RequestHeader_data = RequestHeaderModel.objects.filter(CFApiUserId=request.data['RequestHeader']['CFApiUserId'])
            if len(RequestHeader_data) != 0:
                loanapplication = RequestHeader_data[0].loanapplication
                request.data['AppID'] = loanapplication.AppID
                loanapplication.RequestHeader = RequestHeader_data[0]
                loanapplication.Business = BusinessModel.objects.get(loanapplication=loanapplication)
                loanapplication.Business.Address = AddressModel.objects.get(business=loanapplication.Business)
                loanapplication.Business.SelfReportedCashFlow = SelfReportedCashFlowModel.objects.get(business=loanapplication.Business)
                loanapplication.Owners = OwnersModel.objects.filter(loanapplication=loanapplication)
                for eachOwner in loanapplication.Owners:
                    eachOwner.HomeAddress = HomeAddressModel.objects.get(owner=eachOwner)
                loanapplication.CFApplicationData = CFApplicationDataModel.objects.get(loanapplication=loanapplication)
                db_dict = LoanApplicationSerializer(loanapplication).data
                self.update(db_dict, request.data, loanapplication)
            elif (len(LoanApplication.objects.filter(AppID=request.data['AppID'])) != 0):
                content={
                    "status": "Application Already exists, Try New Application"
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()

            content = {
                "status": 'OK',
                "AppID": request.data['AppID'],
                "Location": "http://127.0.0.1:8000/loanapp/"+str(request.data['AppID'])
            }
            return Response(content, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Get the status of a particular application given a loanappid
class get_post_status(ListCreateAPIView):
    serializer_class = LoanApplicationSerializer
    
    def get_queryset(self):
       loanappid = self.request.query_params.get('loanappid')

       if loanappid == None:
            loanapplications = LoanApplication.objects.all()
       else:
            loanapplications = LoanApplication.objects.filter(AppID=loanappid)

       return loanapplications

    def get(self, request):
        loanapplications = self.get_queryset()
        if len(loanapplications) != 0:
            if len(loanapplications) > 1:
                responseobj = {
                    'data':[]
                }
                for each in loanapplications:
                    statusobj = {}
                    statusobj.update({'AppID': each.AppID})
                    statusobj.update({'Status': each.Status})
                    statusobj.update({'loanapplication': "http://127.0.0.1:8000/loanapp/"+str(each.AppID)})
                    responseobj['data'].append(statusobj)
                return Response(responseobj, status=status.HTTP_200_OK)
            else:
                responseobj = {
                    'data': {
                        'AppID': loanapplications[0].AppID,
                        'Status': loanapplications[0].Status,
                        'loanapplication': 'http://127.0.0.1:8000/loanapp/'+str(loanapplications[0].AppID)
                    }
                }
                return Response(responseobj, status=status.HTTP_200_OK)
        else:
            content = {
                'status': 'Resource Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)


    