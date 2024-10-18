from rest_framework import serializers
from .models import stockPricesData

class stockPricesDataSerializers(serializers.ModelSerializer):

    class Meta:
        model=stockPricesData
        exclude=['type']
        