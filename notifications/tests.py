from django.test import TestCase
from django.apps import apps

class NotificationAppTests(TestCase):
    def test_app_config(self):
        self.assertEqual(apps.get_app_config('notifications').name, 'notifications')