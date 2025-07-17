from django.db import models
from bookings.models import Booking

# Create your models here.

class Payment(models.Model):
    class Status(models.TextChoices):
        SUCCESS = ("success", "Success")
        PENDING = ("pending", "Pending")
        FAILED = ("failed", "Failed")

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Payment #{self.booking} - ${self.amount_paid}"