from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class puzzle(models.Model):
	photo = models.ImageField(blank=False)
	solution = models.CharField(blank=False,max_length=300)

	def __str__(self):
		return self.solution



class user_level(models.Model):
	user = models.ForeignKey(User)
	level = models.IntegerField(blank = True, null=False)
	Time = models.DateTimeField(default = datetime.datetime.now)
	def __str__(self):
		return self.user.username