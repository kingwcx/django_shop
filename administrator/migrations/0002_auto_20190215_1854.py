# Generated by Django 2.1.5 on 2019-02-15 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartcommoditymid',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='ordercommoditymid',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]