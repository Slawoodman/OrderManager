from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal
from users.models import User


class Product(models.Model):
    name = models.CharField(max_length=150, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discounted_price = models.DecimalField(
        default=None, max_digits=10, decimal_places=2, blank=True, null=True
    )
    created = models.DateTimeField(
        auto_now_add=False, blank=True, null=True, default=timezone.now
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.created and self.created.date() < timezone.now().date() - timedelta(
            days=30
        ):
            self.discounted_price = self.price * Decimal(0.8)
        else:
            self.discounted_price = None
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    STATUS_CHOICES = (
        ("Undecided", "UNDECIDED"),
        ("Paid", "PAID"),
        ("Completed", "COMPLETED"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=250, default="")
    postal_code = models.CharField(max_length=20, default="")
    city = models.CharField(max_length=100, default="")
    created = models.DateTimeField(
        auto_now_add=False, blank=True, null=True, default=timezone.now
    )
    updated = models.DateTimeField(
        auto_now_add=False, blank=True, null=True, default=timezone.now
    )
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    file = models.FileField(default="", null=True, blank=True)
    is_paid = models.BooleanField(default=False, null=True, blank=True)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="Undecided"
    )

    def __str__(self):
        return "{}".format(self.id)

    def save(self, *args, **kwargs):
        if self.product.discounted_price:
            self.price = self.product.discounted_price
        else:
            self.price = self.product.price
        return super().save(*args, **kwargs)

    def paid(self):
        self.is_paid = True
        self.save()

    def mark_as_paid(self):
        self.status = "Paid"
        self.save()

