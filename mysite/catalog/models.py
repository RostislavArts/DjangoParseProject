from django.db import models

class Videocard(models.Model):
    name = models.CharField(max_length=200)
    image_url = models.CharField(max_length=200)
    credit_value = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_id = models.CharField(max_length=200, unique=True)
    spec_1 = models.CharField(max_length=200)
    spec_2 = models.CharField(max_length=200)
    spec_3 = models.CharField(max_length=200)
    spec_4 = models.CharField(max_length=200)
    spec_5 = models.CharField(max_length=200)
    spec_6 = models.CharField(max_length=200)

    class Meta:
        db_table = 'videocards'

    def __str__(self):
        return self.name
