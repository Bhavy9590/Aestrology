from django.db import models
class KundliRequest(models.Model):
 name=models.CharField(max_length=120)
 dob=models.DateField()
 tob=models.TimeField()
 place=models.CharField(max_length=180)
 latitude=models.FloatField()
 longitude=models.FloatField()
 timezone=models.CharField(max_length=80,default="Asia/Kolkata")
 created_at=models.DateTimeField(auto_now_add=True)
