from django.shortcuts import render
from django.http import Http404
# models
from .models import *
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import (VendorProfileSerialzier,
                          PurchaseOrderSerializer,
                          VendorPerformanceMatricsSerializer,
                          calculate_vendor_stats,
                          UserRegisterSerializer,
                          PerformanceSerializer)

from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


class UserRegister(APIView):

    def post(self,requset):
        data = requset.data
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Status":"Account Created with username: {}".format(
                    serializer.data["username"])},
                    status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)

class VendorProfileView(APIView):

    permission_classes = (IsAuthenticated,)
    
    def get(self,request):

        obj = VendorProfile.objects.all()

        serializer = VendorProfileSerialzier(obj,many=True)

        return Response(serializer.data)
    
    def post(self,request):

        data = request.data
        serializer = VendorProfileSerialzier(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
    

class VendorDetailsView(APIView):

    permission_classes = (IsAuthenticated,)
    
    def get_object(self, pk):
        try:
            return VendorProfile.objects.get(pk=pk)
        except VendorProfile.DoesNotExist:
            raise Http404

    def get(self,request,vendor_id):
        obj = self.get_object(vendor_id)
        serializer = VendorProfileSerialzier(obj)
        return Response(serializer.data)
    
    def put(self,request,vendor_id):
        obj = self.get_object(vendor_id)
        data = request.data
        serializer = VendorProfileSerialzier(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,vendor_id):
        obj = self.get_object(vendor_id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderView(APIView):

    permission_classes = (IsAuthenticated,)
    
    def get(self,request):

        obj = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(obj,many=True)

        return Response(serializer.data)
    
    def post(self,request):

        permission_classes = (IsAuthenticated,)

        data = request.data
        serializer = PurchaseOrderSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
    
class PurchaseOrderDetailsView(APIView):

    permission_classes = (IsAuthenticated,)
    
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(pk=pk)
        except PurchaseOrder.DoesNotExist:
            raise Http404

    def get(self,request,po_id):
        obj = self.get_object(po_id)
        serializer = PurchaseOrderSerializer(obj)
        return Response(serializer.data)
    
    def put(self,request,po_id):
        obj = self.get_object(po_id)
        data = request.data
        serializer = PurchaseOrderSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,po_id):
        obj = self.get_object(po_id)
        calculate_vendor_stats(obj.vendor_id)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorProfileMatricsView(APIView):
    
    permission_classes = (IsAuthenticated,)

    def get(self,request,vendor_id):
        try:
            obj = VendorProfile.objects.get(pk=vendor_id)
        except VendorProfile.DoesNotExist:
            raise Http404

        serializer = VendorPerformanceMatricsSerializer(obj)

        return Response(serializer.data)
    
class AchnowledgeView(APIView):

    permission_classes = (IsAuthenticated,)

    def post(self,request,po_id):
        date  = timezone.now()
        try:
            obj = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            raise Http404
        data = {}
        data['achnowledgment_date'] = date
        serializer = PurchaseOrderSerializer(obj,data=data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
class PerformanceView(APIView):

    def get(self,request,vendor_id):
        obj = HistoricalPeformanceModel.objects.filter(vendor=vendor_id)

        obj = PerformanceSerializer(obj,many=True)

        return Response(obj.data)