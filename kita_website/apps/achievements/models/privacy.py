from django.db import models
from django.contrib.auth.models import User

class Privacy(models.Model):
    user = models.ForeignKey(User)

    public_achievements = models.BooleanField(default=False)

    class Meta:
        app_label = 'achievements'