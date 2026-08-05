from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WebhookSubscriptionViewSet, NotificationViewSet

router = DefaultRouter()
router.register('subscriptions', WebhookSubscriptionViewSet, basename='subscription')
router.register('events', NotificationViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
]