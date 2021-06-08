from django.test import TestCase, override_settings

from .notifications import task

class TestCelery(TestCase):
    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_notifications_task(self):
        self.assertTrue(task.delay())