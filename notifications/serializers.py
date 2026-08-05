from rest_framework import serializers
from .models import WebhookSubscription, Notification, WebhookDeliveryLog

class WebhookSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookSubscription
        fields = ['id', 'target_url', 'secret_key', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'secret_key', 'created_at', 'updated_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'event_type', 'payload', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']