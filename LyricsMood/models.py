from django.db import models

# Create your models here.
class Artists(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Polar(models.Model):
    polar = models.CharField(max_length=20)

    def __str__(self):
        return self.polar

class Lyrics(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artists, on_delete=models.CASCADE)
    polar = models.ForeignKey(Polar, on_delete=models.CASCADE)
    chorus = models.TextField()
    hook = models.TextField()
    lead = models.TextField()
    year = models.CharField(max_length=4)

    def __str__(self):
        return self.title
