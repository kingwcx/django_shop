# Generated by Django 2.1.5 on 2019-02-16 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0005_auto_20190216_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextension',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userextension',
            name='sex',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
