from django.urls import path

from .views import *


urlpatterns = [
    path('vendors/', VendorProfileView.as_view()),
    path('vendors/<int:vendor_id>',VendorDetailsView.as_view()),

    path('purchase_orders/',PurchaseOrderView.as_view()),
    path('purchase_orders/<int:po_id>',PurchaseOrderDetailsView.as_view()),

    path('vendors/<int:vendor_id>/performance',VendorProfileMatricsView.as_view()),
    path('purchase_order/<int:po_id>/achnowledgment',AchnowledgeView.as_view()),
    path('vendor/performance/<int:vendor_id>/log',PerformanceView.as_view()),

]
