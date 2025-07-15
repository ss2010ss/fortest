from django.db import models

# Create your models here.
class textsfortest(models.Model):
    text = models.CharField(max_length=1000, default='')

    parenttext = models.CharField(max_length=200, default='')

    count = models.IntegerField(default=0)

    like = models.IntegerField(default=0)

    dislike = models.IntegerField(default=0)

    weight = models.IntegerField(default=0)

  