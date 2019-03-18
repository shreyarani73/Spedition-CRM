# Generated by Django 2.0.7 on 2019-03-17 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0007_auto_20190314_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceitem',
            name='cgst',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='igst',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='sgst',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='invoiceitem',
            name='sub_total',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
