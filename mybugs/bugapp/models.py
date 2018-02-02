from django.db import models

# Create your models here.

class User(models.Model):
	username = models.CharField(max_length=100, primary_key=True)
	password = models.CharField(max_length=100)

class Bugs(models.Model):
	bugId = models.CharField(max_length=100)
	desc = models.CharField(max_length=200)
