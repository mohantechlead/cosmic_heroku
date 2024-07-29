from django.contrib import admin
from django.urls import path, include
from cosmic import views
from .views import *
from django.conf.urls.static import  static,settings

urlpatterns = [
    path('create_customer', views.create_customer, name='create_customer'),
    path('create_supplier', views.create_supplier, name='create_supplier'),
    path('display_items', views.display_items, name='display_items'),
    path('display_customers', views.display_customers, name='display_customers'),
    path('create_dn', views.create_dn, name='create_dn'),
    path('display_dn', views.display_dn, name='display_dn'),
    path('edit_customer', views.edit_customer, name='edit_customer'),
    # path('delete_customer/<str:customer_name>', views.delete_customer, name="delete_customer"),
    path('delete_customer_profile', views.delete_customer_profile, name='delete_customer_profile'),
    path('delete_supplier_profile', views.delete_supplier_profile, name='delete_supplier_profile'),
    path('display_customer_profile/<str:customer_name>', views.display_customer_profile, name='display_customer_profile'),
    path('display_supplier', views.display_supplier, name='display_supplier'),
    path('display_order', views.display_order, name='display_order'),
    path('display_purchase', views.display_purchase, name='display_purchase'),
    path('display_supplier_profile/<str:supplier_name>', views.display_supplier_profile, name='display_supplier_profile'),
    path('create_purchase', views.create_purchase, name='create_purchase'),
    path('create_grn', views.create_grn, name='create_grn'),
    path('display_grn', views.display_grn, name='display_grn'),
    path('create_shipping', views.create_shipping, name='create_shipping'),
    path('order_approval', views.order_approval, name='order_approval'),
    path('purchase_approval', views.purchase_approval, name='purchase_approval'),
    path('order_status', views.order_status, name='order_status'),
    path('purchase_status', views.purchase_status, name='purchase_status'),
    path('edit_order', views.edit_order, name='edit_order'),
    path('edit_purchase', views.edit_purchase, name='edit_purchase'),
    path('commercial_invoice', views.commercial_invoice, name='commercial_invoice'),
    path('print_order', views.print_order, name='print_order'),
    path('bill_of_lading', views.bill_of_lading, name='bill_of_lading'),
    path('rejected_orders', views.rejected_orders, name='rejected_orders'),
    path('packing_list', views.packing_list, name='packing_list'),
    path('truck_waybill', views.truck_waybill, name='truck_waybill'),
    path('indexs', views.index_home, name='indexs'),
    path('create_order_items', views.create_order_items, name='create_order_items'),
    path('create_purchase_items', views.create_purchase_items, name='create_purchase_items'),
    path('create_grn_items', views.create_grn_items, name='create_grn_items'),
    path('create_invoice_items', views.create_invoice_items, name='create_invoice_items'),
    path('display_single_order/<str:order_no>', views.display_single_order, name='display_single_order'),
    path('display_single_purchase/<str:purchase_no>', views.display_single_purchase, name='display_single_purchase'),
    path('sales_contract', views.sales_contract, name='sales_contract'),
    path('update_order', views.update_order, name='update_order'),
    path('update_purchase', views.update_purchase, name='update_purchase'),
    path('update_shipping', views.update_shipping, name='update_shipping'),
    path('edit_shipping', views.edit_shipping, name='edit_shipping'),
    path('create_orders', views.create_orders, name='create_orders'),
    path('completed_orders', views.completed_orders, name='completed_orders'),
    path('get_item_data/<str:item_id>/', get_item_data, name='get_item_data'),
    path('edit_order_only', views.edit_order_only, name='edit_order_only'),
    
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
