# Generated by Django 4.1.5 on 2023-01-23 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookings", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="guests",
            field=models.PositiveBigIntegerField(default=1),
        ),
    ]
