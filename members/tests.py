from django.test import TestCase
from datetime import datetime
from .models import reservation

# Create your tests here.
class RecoTest(TestCase):
    def setup(cls):
     cls.reserv=reservation.objects.create(
        first_name="John",
        last_name='mcdonald'
    )
    def test_fields(self):
        self.assertIsInstance(self.reserv.first_name,str)
        self.assertIsInstance(self.reserv.last_name,str)