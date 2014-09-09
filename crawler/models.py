from django.db import models
from datetime import datetime

class Query(models.Model):
	Query_text = models.CharField(blank=False,max_length=255)
	Timestamp = models.DateTimeField(blank=False,default=datetime.now())
	Result = models.ForeignKey("Result")
	
class Result(models.Model):
	ResultJSON = models.CharField(max_length=500000)

class Queue(models.Model):
	QueueElements = models.ForeignKey("Query")
	
