from django.db import models

# Create your models here.


class LoanApplication(models.Model):
    # requestHeader = models.ForeignKey(RequestHeader, related_name='requestHeader', on_delete=models.CASCADE)
    AppID = models.IntegerField()
    Status = models.CharField(max_length=100, default='Submitted')

    # title = models.CharField(max_length=100)
    # genre = models.CharField(max_length=100)
    # year = models.IntegerField()
    # created_at = models.DateTimeField(auto_now_add=True) # When it was create
    # updated_at = models.DateTimeField(auto_now=True) # When i was update

    def __str__(self):
        return str(self.AppID)

    
    depth = 1

class RequestHeaderModel(models.Model):
    loanapplication = models.ForeignKey(LoanApplication, null=True, on_delete=models.CASCADE)
    CFRequestId = models.CharField(max_length=100)
    RequestDate = models.DateTimeField(auto_now_add=True)
    CFApiUserId = models.CharField(max_length=100)
    CFApiPassword = models.CharField(max_length=100)    
    IsTestLead = models.BooleanField()

    def __str__(self):
        return 'RequestHeaderInfo'


class BusinessModel(models.Model):
    loanapplication = models.ForeignKey(LoanApplication, null=True, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    TaxID = models.CharField(max_length=100)
    Phone = models.CharField(max_length=100)
    NAICS = models.CharField(max_length=100)    
    HasBeenProfitable = models.BooleanField()
    HasBankruptedInLast7Years = models.BooleanField()
    InceptionDate = models.DateTimeField()


class AddressModel(models.Model):
    business = models.ForeignKey(BusinessModel, null=True, on_delete=models.CASCADE)
    Address1 = models.CharField(max_length=100)
    Address2 = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Zip = models.CharField(max_length=100)

class SelfReportedCashFlowModel(models.Model):
    business = models.ForeignKey(BusinessModel, null=True, on_delete=models.CASCADE)
    AnnualRevenue = models.FloatField()
    MonthlyAverageBankBalance = models.FloatField()
    MonthlyAverageCreditCardVolume = models.FloatField()

class OwnersModel(models.Model):
    loanapplication = models.ForeignKey(LoanApplication, null=True, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100)
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    DateOfBirth = models.DateTimeField()
    HomePhone = models.CharField(max_length=100)
    SSN = models.CharField(max_length=100)
    PercentageOfOwnership = models.FloatField()


class HomeAddressModel(models.Model):
    owner = models.ForeignKey(OwnersModel, null=True, on_delete=models.CASCADE)
    Address1 = models.CharField(max_length=100)
    Address2 = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Zip = models.CharField(max_length=100)

class CFApplicationDataModel(models.Model):
    loanapplication = models.ForeignKey(LoanApplication, null=True, on_delete=models.CASCADE)
    RequestedLoanAmount = models.CharField(max_length=100)
    StatedCreditHistory = models.IntegerField()
    LegalEntityType = models.CharField(max_length=100)
    FilterID = models.CharField(max_length=100)

