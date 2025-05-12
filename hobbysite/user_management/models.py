from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=63, default="")
    email = models.EmailField(max_length=255)

    def __str__(self):
        # return '{}'.format(self.name)
        return self.name if self.name else self.user.username
    
    def get_absolute_url(self):
        return reverse('profile', args=[str(self.id)])