from django.db import models
import uuid


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='RUB')
    description = models.BooleanField()
    status = models.CharField(max_length=25, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_url = models.URLField(null=True)
    redirect_url = models.URLField(null=True)
    webhook_url = models.URLField(null=True)

    class Meta:
        db_table = 'payments'


class PaymentNotifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=25)

    class Meta:
        db_table = 'payment_notifications'


class DescriptionPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.JSONField()

