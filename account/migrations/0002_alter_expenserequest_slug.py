# Generated by Django 4.1.7 on 2023-03-28 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenserequest',
            name='slug',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
