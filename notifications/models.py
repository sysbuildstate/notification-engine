import uuid
from django.db import models
from django.utils.crypto import get_random_string

def generate_hmac_secret() -> str:
    return get_random_string(64)

class WebhookSubscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    target_url = models.URLField(unique=True)
    secret_key = models.CharField(max_length=64, default=generate_hmac_secret)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'webhook_subscriptions'

class NotificationStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    DELIVERED = 'DELIVERED', 'Delivered'
    FAILED = 'FAILED', 'Failed'

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    status = models.CharField(
        max_length=20,
        choices=NotificationStatus.choices,
        default=NotificationStatus.PENDING,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

class WebhookDeliveryLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='delivery_logs')
    subscription = models.ForeignKey(WebhookSubscription, on_delete=models.CASCADE, related_name='delivery_logs')
    status_code = models.IntegerField(null=True, blank=True)
    response_body = models.TextField(blank=True)
    attempt_count = models.PositiveIntegerField(default=1)
    next_retry_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'webhook_delivery_logs'
        indexes = [
            models.Index(fields=['next_retry_at']),
        ]