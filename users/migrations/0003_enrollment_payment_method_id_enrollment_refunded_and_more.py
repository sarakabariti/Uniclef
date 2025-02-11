# Generated by Django 4.2.6 on 2023-11-13 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_enrollment_refund_paymentmethod_paymenthistory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='payment_method_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='users.paymentmethod'),
        ),
        migrations.AddField(
            model_name='enrollment',
            name='refunded',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='PaymentHistory',
        ),
    ]
