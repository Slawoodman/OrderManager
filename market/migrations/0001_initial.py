# Generated by Django 4.0.6 on 2023-06-06 23:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=250, null=True)),
                ("postal_code", models.CharField(blank=True, max_length=20, null=True)),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "created",
                    models.DateTimeField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                (
                    "updated",
                    models.DateTimeField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
                (
                    "file",
                    models.FileField(blank=True, default="", null=True, upload_to=""),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Undecided", "UNDECIDED"),
                            ("Paid", "PAID"),
                            ("Completed", "COMPLETED"),
                        ],
                        default="Undecided",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=150, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "discounted_price",
                    models.DecimalField(
                        blank=True,
                        decimal_places=2,
                        default=None,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        blank=True, default=django.utils.timezone.now, null=True
                    ),
                ),
            ],
        ),
    ]
