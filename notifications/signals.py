from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, WebhookSubscription
from .tasks import dispatch_webhook

@receiver(post_save, sender=Notification)
def trigger_webhook_dispatch(sender, instance, created, **kwargs) -> None:
    if created:
        subscriptions = WebhookSubscription.objects.filter(is_active=True)
        for subscription in subscriptions:
            dispatch_webhook.delay(str(instance.id), str(subscription.id))