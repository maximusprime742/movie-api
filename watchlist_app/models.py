from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=50)
    release_date = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
