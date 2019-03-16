# Generated by Django 2.1 on 2018-10-26 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0002_quotation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='taxes',
            field=models.FloatField(choices=[(5, '5% GST'), (12, '12% GST'), (18, '18% GST')], default=18.0),
        ),
    ]