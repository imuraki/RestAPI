# Generated by Django 2.2.9 on 2020-01-24 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homechallenge', '0006_addressmodel_businessmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='OwnersModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('FirstName', models.CharField(max_length=100)),
                ('LastName', models.CharField(max_length=100)),
                ('Email', models.CharField(max_length=100)),
                ('DateOfBirth', models.DateTimeField()),
                ('HomePhone', models.CharField(max_length=100)),
                ('SSN', models.CharField(max_length=100)),
                ('PercentageOfOwnership', models.IntegerField()),
                ('loanapplication', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homechallenge.LoanApplication')),
            ],
        ),
        migrations.CreateModel(
            name='HomeAddressModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Address1', models.CharField(max_length=100)),
                ('Address2', models.CharField(max_length=100)),
                ('City', models.CharField(max_length=100)),
                ('State', models.CharField(max_length=100)),
                ('Zip', models.CharField(max_length=100)),
                ('owners', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homechallenge.OwnersModel')),
            ],
        ),
    ]
