# Generated by Django 2.2.4 on 2022-03-30 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_worker_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_detail',
            name='amount_paid',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
