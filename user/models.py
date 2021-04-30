from django.db import models

# Create your models here.
class Closet(models.Model):
    #id=models.CharField(max_length=50)
    brand=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    cover=models.ImageField()
    price=models.IntegerField()

    class Meta:
        db_table='user'

    def __str__(self):
        return self.name

