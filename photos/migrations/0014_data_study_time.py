# Generated by Django 2.1 on 2020-03-21 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0013_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='study_time',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
