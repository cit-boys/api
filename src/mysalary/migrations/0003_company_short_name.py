# Generated by Django 3.1.7 on 2021-05-23 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysalary', '0002_auto_20210508_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='short_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
