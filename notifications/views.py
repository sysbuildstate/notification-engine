from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .models import WebhookSubscription, Notification
from .serializers import WebhookSubscriptionSerializer, NotificationSerializer

class WebhookSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = WebhookSubscription.objects.all()
    serializer_class = WebhookSubscriptionSerializer
    permission_classes = [IsAuthenticated]

class NotificationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]