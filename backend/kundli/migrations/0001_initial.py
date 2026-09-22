from django.db import migrations,models
class Migration(migrations.Migration):
 initial=True; dependencies=[]
 operations=[migrations.CreateModel(name="KundliRequest",fields=[
 ("id",models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name="ID")),
 ("name",models.CharField(max_length=120)),("dob",models.DateField()),("tob",models.TimeField()),
 ("place",models.CharField(max_length=180)),("latitude",models.FloatField()),("longitude",models.FloatField()),
 ("timezone",models.CharField(default="Asia/Kolkata",max_length=80)),("created_at",models.DateTimeField(auto_now_add=True))
 ])]
