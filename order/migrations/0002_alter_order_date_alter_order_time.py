# Generated by Django 4.2.7 on 2024-10-01 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
