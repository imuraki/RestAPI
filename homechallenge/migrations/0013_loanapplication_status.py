# Generated by Django 2.2.9 on 2020-01-24 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homechallenge', '0012_auto_20200124_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='Status',
            field=models.CharField(default='Submitted', max_length=100),
        ),
    ]
