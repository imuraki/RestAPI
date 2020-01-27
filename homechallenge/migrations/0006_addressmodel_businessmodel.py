# Generated by Django 2.2.9 on 2020-01-24 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homechallenge', '0005_requestheader_loanapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('TaxID', models.CharField(max_length=100)),
                ('Phone', models.CharField(max_length=100)),
                ('NAICS', models.CharField(max_length=100)),
                ('HasBeenProfitable', models.BooleanField()),
                ('HasBankruptedInLast7Years', models.BooleanField()),
                ('InceptionDate', models.DateTimeField()),
                ('loanapplication', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homechallenge.LoanApplication')),
            ],
        ),
        migrations.CreateModel(
            name='AddressModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Address1', models.CharField(max_length=100)),
                ('Address2', models.CharField(max_length=100)),
                ('City', models.CharField(max_length=100)),
                ('State', models.CharField(max_length=100)),
                ('Zip', models.CharField(max_length=100)),
                ('business', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homechallenge.BusinessModel')),
            ],
        ),
    ]
