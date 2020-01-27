from rest_framework import serializers
from .models import LoanApplication, RequestHeaderModel, BusinessModel, AddressModel, HomeAddressModel, OwnersModel, SelfReportedCashFlowModel, CFApplicationDataModel, CFApplicationDataModel

class RequestHeaderSerializer(serializers.ModelSerializer):

     class Meta:
        model = RequestHeaderModel
        fields = ('CFRequestId', 'RequestDate', 'CFApiUserId', 'CFApiPassword', 'IsTestLead')

class AddressModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressModel
        fields = ('Address1','Address2','City','State','Zip')

class SelfReportedCashFlowModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SelfReportedCashFlowModel
        fields = ('AnnualRevenue','MonthlyAverageBankBalance','MonthlyAverageCreditCardVolume')

class HomeAddressModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeAddressModel
        fields = ('Address1','Address2','City','State','Zip')


class OwnersModelSerializer(serializers.ModelSerializer):
    HomeAddress = HomeAddressModelSerializer()

    class Meta:
        model = OwnersModel
        fields=('Name','FirstName','LastName','Email','HomeAddress','DateOfBirth','HomePhone','SSN','PercentageOfOwnership')


class BusinessModelSerializer(serializers.ModelSerializer):
    Address = AddressModelSerializer()
    SelfReportedCashFlow = SelfReportedCashFlowModelSerializer()

    class Meta:
        model = BusinessModel
        fields = ('Name','SelfReportedCashFlow','Address','TaxID','Phone','NAICS','HasBeenProfitable','HasBankruptedInLast7Years','InceptionDate')


class CFApplicationDataModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = CFApplicationDataModel
        fields = ('RequestedLoanAmount','StatedCreditHistory','LegalEntityType','FilterID')


class LoanApplicationSerializer(serializers.ModelSerializer):  # create class to serializer model
    RequestHeader = RequestHeaderSerializer()
    Business = BusinessModelSerializer()
    Owners = OwnersModelSerializer(many=True)
    CFApplicationData = CFApplicationDataModelSerializer()


    class Meta:
        model = LoanApplication
        fields = ('AppID','RequestHeader','Business','Owners','CFApplicationData','Status')

    def create(self, validated_data):
        # validated_data['Status'] = 'Submitted'

        RequestHeader_data = validated_data.pop('RequestHeader')
        Business_data = validated_data.pop('Business')
        Owners_data  = validated_data.pop('Owners')
        CFApplicationData_data = validated_data.pop('CFApplicationData')



        loanapplication = LoanApplication.objects.create(**validated_data)

        RequestHeader = RequestHeaderModel.objects.create(**RequestHeader_data, loanapplication=loanapplication)

        Address_data = Business_data.pop('Address')
        SelfReportedCashFlow_data = Business_data.pop('SelfReportedCashFlow')

        Business = BusinessModel.objects.create(**Business_data, loanapplication=loanapplication)
        Address = AddressModel.objects.create(**Address_data, business=Business)
        SelfReportedCashFlow = SelfReportedCashFlowModel.objects.create(**SelfReportedCashFlow_data, business=Business)

        for eachOwner_data in Owners_data:
            HomeAddress_data = eachOwner_data.pop('HomeAddress')
            Owner = OwnersModel.objects.create(**eachOwner_data, loanapplication=loanapplication)
            HomeAddress = HomeAddressModel.objects.create(**HomeAddress_data, owner=Owner)

        CFApplicationData = CFApplicationDataModel.objects.create(**CFApplicationData_data, loanapplication=loanapplication)    

        return loanapplication


