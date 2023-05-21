from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Property(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    subscription_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('property_detail', args=[str(self.id)])
