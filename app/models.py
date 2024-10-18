from django.db import models

# Create your models here.

class stockPricesData(models.Model):
    symbol = models.CharField(max_length=10)
    date = models.DateField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    low_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    volume = models.BigIntegerField(null=True,blank=True)
    type = models.CharField(max_length=1,default="A")

    class Meta:
        unique_together = ('symbol', 'date')
        indexes = [
            models.Index(fields=['symbol', 'date']),
        ]
