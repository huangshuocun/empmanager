from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=32,null=False,unique=True,db_index=True)
    name=models.CharField(max_length=32,db_index=True)
    pwd=models.CharField(max_length=128)
    age=models.IntegerField() #可以用booleanfield
    sex=models.CharField(max_length=2,db_index=True)
    phone=models.CharField(max_length=15)

    class Meta:
        db_table='user'
