# Generated by Django 2.2.9 on 2020-01-23 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homechallenge', '0003_auto_20200123_1839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanapplication',
            name='requestHeader',
        ),
    ]
