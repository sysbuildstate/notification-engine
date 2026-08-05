import hmac
import hashlib
import json
import requests
from celery import shared_task
from django.utils import timezone
from .models import Notification, WebhookSubscription, WebhookDeliveryLog


@shared_task(bind=True, max_retries=5)
def dispatch_webhook(self, notification_id: str, subscription_id: str) -> None:
    notification = Notification.objects.get(id=notification_id)
    subscription = WebhookSubscription.objects.get(id=subscription_id)

    payload_bytes = json.dumps(notification.payload).encode('utf-8')
    secret_bytes = subscription.secret_key.encode('utf-8')
    signature = hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'X-Webhook-Signature': signature
    }

    log = WebhookDeliveryLog.objects.create(
        notification=notification,
        subscription=subscription,
        attempt_count=self.request.retries + 1
    )

    try:
        response = requests.post(subscription.target_url, json=notification.payload, headers=headers, timeout=10)
        log.status_code = response.status_code
        log.response_body = response.text[:2000]
        log.save()

        if response.status_code >= 400:
            log.next_retry_at = timezone.now() + timezone.timedelta(seconds=2 ** self.request.retries)
            log.save()
            raise self.retry(countdown=2 ** self.request.retries)
    except requests.exceptions.RequestException as e:
        log.response_body = str(e)[:2000]
        log.next_retry_at = timezone.now() + timezone.timedelta(seconds=2 ** self.request.retries)
        log.save()
        raise self.retry(exc=e, countdown=2 ** self.request.retries)