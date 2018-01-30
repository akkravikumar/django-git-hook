from django.db import models

# Create your models here.
class Bugs(models.Model):
	bugId = models.CharField(max_length=100)
	desc = models.CharField(max_length=200)
