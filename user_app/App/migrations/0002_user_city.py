# Generated by Django 4.1.5 on 2023-01-27 13:20

from django.db import migrations , models


class Migration ( migrations.Migration ):
    dependencies = [
        ('App' , '0001_initial') ,
    ]

    operations = [
        migrations.AddField (
            model_name='user' ,
            name='city' ,
            field=models.CharField ( max_length=20 , null=True ) ,
        ) ,
    ]
