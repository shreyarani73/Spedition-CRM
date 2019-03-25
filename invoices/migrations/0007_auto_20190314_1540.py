# Generated by Django 2.0.7 on 2019-03-14 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0006_invoice_balance_due'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='balance_due',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]