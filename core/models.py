from django.db import models
from accounts.models import User


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=150, verbose_name='title')
    description = models.CharField(max_length=500, verbose_name='description')
    date = models.DateField(verbose_name='date')
    owner = models.ForeignKey(User, related_name='my_events', on_delete=models.CASCADE, verbose_name='owner')
    participants = models.ManyToManyField(User, related_name='signup_events', blank=True, null=True)

    def participants_count(self):
        return self.participants.count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
