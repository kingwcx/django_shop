# Generated by Django 2.1.5 on 2019-02-16 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_usermessage'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='usermessage',
            table='message',
        ),
    ]
