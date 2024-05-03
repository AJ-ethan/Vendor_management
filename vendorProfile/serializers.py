
from rest_framework import serializers


from .models import *
from django.utils import timezone
from django.db import transaction

from django.db.models import (Q, Avg, F, 
                              ExpressionWrapper, 
                              fields, Sum)

from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)
    confirm_password = serializers.CharField(max_length=100)

    def create(self, validated_data):
        if (validated_data["password"]!=validated_data["confirm_password"]):
            raise serializers.ValidationError("Password and Confirm Password not Matched")
        try:
            obj = User.objects.create_user(username=validated_data['username'],
                                           password=validated_data["password"])
        except Exception as e:
            raise serializers.ValidationError(e)
        obj.set_password(validated_data["password"])
        obj.save()
        return validated_data

def calculate_on_time_delivery(vendor_id):
    queryset = PurchaseOrder.objects.filter(vendor_id__id=vendor_id)
    total_purchases = queryset.count()
    on_time_purchases = queryset.filter(
                    Q(delivered_date__isnull=False) &
                    Q(delivered_date__lte = F('delivery_date'))
                    ).count()
    ans = 0
    
    try:
        ans = on_time_purchases*100/total_purchases
    except:
        pass
    return ans

def calculate_quality_rating(vendor_id):
    total_count = PurchaseOrder.objects.filter(
                    Q(quality_rating__isnull=False) 
                    & Q(vendor_id__id=vendor_id)
                    )
    count = total_count.count()
    curr_sum = total_count.aggregate(Sum('quality_rating'))["quality_rating__sum"]
    ans = 0
    try:
        ans = (curr_sum*5)/(count*5)
    except:
        pass

    return ans

def calculate_average_response_time(vendor_id):
    """work in mysql and postgresql"""
    # total_count = PurchaseOrder.objects.filter(
    #     Q(achnowledgement_date__isnull=False)
    #       & Q(vendor_id__id=2)).aggregate(
    #           average_time=Avg(
    #               ExpressionWrapper(
    #                   F('achnowledgs ment_date')-F('issue_date'),
    #                   output_field=models.DateTimeField()
    #                   )
    #     ))
    queryset = PurchaseOrder.objects.filter(
        Q(achnowledgment_date__isnull=False) 
        & Q(vendor_id__id=vendor_id))

    val =queryset.aggregate(
        total_time_diff=Avg(
            ExpressionWrapper(F('achnowledgment_date') - F('issue_date'),
                              output_field=fields.DurationField()))
        )['total_time_diff']
    try:
        val = val.total_seconds()/60
        return val
    except:
        return 0

def calculate_fulfillment_rate(vendor_id):
    queryset = PurchaseOrder.objects.filter(vendor_id__id=vendor_id)
    total_purchases = queryset.count()
    completed_purchases = queryset.filter(
                        status ="Completed"
                    ).count()
    ans = 0
    
    try:
        ans = completed_purchases*100/total_purchases
    except:
        pass
    return ans

def calculate_vendor_stats(vendor_id):

    instance = VendorProfile.objects.get(pk=vendor_id)
    instance.on_time_delivery_rate = calculate_on_time_delivery(vendor_id)
    instance.quality_rating_average = calculate_quality_rating(vendor_id)
    instance.average_response_time  = calculate_average_response_time(vendor_id)
    instance.fulfillment_rate = calculate_fulfillment_rate(vendor_id)
    instance.save()



class VendorProfileSerialzier(serializers.ModelSerializer):

    class Meta:
        model = VendorProfile
        fields = ("name","contract_details",
                  "address","vendor_code")


class PurchaseOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = "__all__"
    
    def validate(self, attrs):

        order_date = timezone.now()
        delivery_date = None
        if(self.instance):
            order_date = self.instance.order_date
            delivery_date = self.instance.delivery_date
        delivery_date = attrs.get("delivery_date",delivery_date)

        if(delivery_date and delivery_date<order_date):
            raise serializers.ValidationError("Delivery date must place in future")
        
        rating = attrs.get("quality_rating",None)
        if (rating and (rating<=5 or rating>=0)):
            raise serializers.ValidationError("Rating must be less than 5 and grater than zero")

        
        return super().validate(attrs)

    def create(self,validated_data):
        obj  =None
        with transaction.atomic():
            obj = PurchaseOrder.objects.create(**validated_data)
            calculate_vendor_stats(obj.vendor_id)
        if obj:
            return obj
        raise serializers.ValidationError()
    
    def update(self,instance,validated_data):
        obj = None
        status = validated_data.get("status",None)
        if status and (status=='Completed' and instance.status!="Completed"):
            validated_data["delivered_date"] = timezone.now()
        with transaction.atomic():
            for i,j in validated_data.items():
                setattr(instance,i,j)
            instance.save()
            obj = instance
            calculate_vendor_stats(instance.vendor_id)
        if obj:
            return obj
        raise serializers.ValidationError()
    

class VendorPerformanceMatricsSerializer(serializers.ModelSerializer):

    class Meta:
        model = VendorProfile
        exclude = ("id","name","contract_details",
                  "address","vendor_code")

class PerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = HistoricalPeformanceModel
        fields = "__all__"