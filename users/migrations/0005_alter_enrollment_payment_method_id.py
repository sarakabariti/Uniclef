# Generated by Django 4.2.6 on 2023-11-13 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_paymentmethod_cvv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='payment_method_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.paymentmethod'),
        ),
    ]
