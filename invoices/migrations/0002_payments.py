# Generated by Django 2.1 on 2018-08-21 06:34

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField(default=django.utils.timezone.now)),
                ('amount', models.FloatField(default=0.0)),
                ('payment_mode', models.CharField(choices=[('Cash', 'Cash'), ('NEFT/RTGS/IMPS', 'NEFT/RTGS/IMPS'), ('Bank Deposit', 'Bank Deposit'), ('Cheque', 'Cheque')], max_length=200)),
                ('notes', models.CharField(blank=True, max_length=250, null=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.Invoice')),
            ],
        ),
    ]