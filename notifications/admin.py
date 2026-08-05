from django.contrib import admin
from .models import WebhookSubscription, Notification, WebhookDeliveryLog

@admin.register(WebhookSubscription)
class WebhookSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'target_url', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('target_url',)
    readonly_fields = ('id', 'secret_key', 'created_at', 'updated_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_type', 'status', 'created_at')
    list_filter = ('status', 'event_type')
    search_fields = ('id', 'event_type')
    readonly_fields = ('id', 'created_at')

@admin.register(WebhookDeliveryLog)
class WebhookDeliveryLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'notification', 'subscription', 'status_code', 'attempt_count', 'next_retry_at')
    list_filter = ('status_code',)
    search_fields = ('notification__id', 'subscription__target_url')
    readonly_fields = ('id', 'created_at')