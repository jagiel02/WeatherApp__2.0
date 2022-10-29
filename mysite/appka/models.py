from django.db import models

class City (models.Model):
    name = models.CharField(max_length=25, blank=False, default='')
    city_id = models.AutoField(primary_key=True)


    def __str__(self):
        return self.name



