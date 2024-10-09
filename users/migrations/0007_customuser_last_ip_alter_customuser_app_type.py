# Generated by Django 4.2.7 on 2024-10-09 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_vendor_service_line_vendorserviceline'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_ip',
            field=models.CharField(default='127.0.0.1', max_length=100),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='app_type',
            field=models.CharField(choices=[('bazar', 'Bazar'), ('myket', 'Myket'), ('googleplay', 'Googleplay'), ('appstore', 'Appstore'), ('web', 'Web'), ('test', 'Test')], default='bazar', max_length=20),
        ),
    ]
