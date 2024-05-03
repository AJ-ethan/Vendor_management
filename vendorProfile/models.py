from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

class VendorProfile(models.Model):
    name = models.CharField(max_length=100)
    contract_details = models.TextField()
    address = models.TextField()
    vendor_code= models.CharField(max_length=50,unique=True)

    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_average = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50,unique=True)
    vendor = models.ForeignKey(VendorProfile,on_delete=models.CASCADE,
                               related_name="vendor_po")
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status =  models.CharField(max_length=50)
    delivered_date = models.DateTimeField(null=True)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    achnowledgment_date = models.DateTimeField(null=True)

class HistoricalPeformanceModel(models.Model):
    vendor = models.ForeignKey(VendorProfile,on_delete=models.CASCADE,related_name="vendor_log")
    date = models.DateTimeField(auto_now_add=True)
    
    on_time_delivery_rate = models.FloatField()
    quality_rating_average = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


@receiver(post_save, sender=VendorProfile)
def log_performance(sender, instance, created, ** kwargs) :
    d = {
        "vendor":instance,
        "on_time_delivery_rate":instance.on_time_delivery_rate,
        "quality_rating_average":instance.quality_rating_average,
        "average_response_time": instance.average_response_time,
        "fulfillment_rate":instance.fulfillment_rate,
    }
    HistoricalPeformanceModel.objects.create(**d)

