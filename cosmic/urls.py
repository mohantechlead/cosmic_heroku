from django.contrib import admin
from django.urls import path, include
from cosmic import views
from .views import *
from django.conf.urls.static import  static,settings
from .views.approval_view import *
from .views.customer_view import *
from .views.dn_view import *
from .views.grn_view import *
from .views.item_view import *
from .views.print_view import *
from .views.purchase_view import *
from .views.sales_view import *
from .views.shipping_view import *
from .views.supplier_view import *

urlpatterns = [
    path('create_customer', create_customer, name='create_customer'),
    path('create_supplier', create_supplier, name='create_supplier'),
    path('display_items', display_items, name='display_items'),
    path('display_customers', display_customers, name='display_customers'),
    path('create_dn', create_dn, name='create_dn'),
    path('display_dn', display_dn, name='display_dn'),
    path('edit_customer', edit_customer, name='edit_customer'),
    # path('delete_customer/<str:customer_name>', delete_customer, name="delete_customer"),
    path('delete_customer_profile', delete_customer_profile, name='delete_customer_profile'),
    path('delete_supplier_profile', delete_supplier_profile, name='delete_supplier_profile'),
    path('display_customer_profile/<str:customer_name>', display_customer_profile, name='display_customer_profile'),
    path('display_supplier', display_supplier, name='display_supplier'),
    path('display_order', display_order, name='display_order'),
    path('display_purchase', display_purchase, name='display_purchase'),
    path('display_supplier_profile/<str:supplier_name>', display_supplier_profile, name='display_supplier_profile'),
    path('create_purchase', create_purchase, name='create_purchase'),
    path('create_grn', create_grn, name='create_grn'),
    path('display_grn', display_grn, name='display_grn'),
    path('create_shipping', create_shipping, name='create_shipping'),
    path('order_approval', order_approval, name='order_approval'),
    path('purchase_approval', purchase_approval, name='purchase_approval'),
    path('order_status', order_status, name='order_status'),
    path('purchase_status', purchase_status, name='purchase_status'),
    path('edit_order', edit_order, name='edit_order'),
    path('edit_purchase', edit_purchase, name='edit_purchase'),
    path('commercial_invoice', commercial_invoice, name='commercial_invoice'),
    path('print_order', print_order, name='print_order'),
    path('bill_of_lading', bill_of_lading, name='bill_of_lading'),
    path('rejected_orders', rejected_orders, name='rejected_orders'),
    path('packing_list', packing_list, name='packing_list'),
    path('truck_waybill', truck_waybill, name='truck_waybill'),
    path('indexs', index_home, name='indexs'),
    path('create_order_items', create_order_items, name='create_order_items'),
    path('create_purchase_items', create_purchase_items, name='create_purchase_items'),
    path('create_grn_items', create_grn_items, name='create_grn_items'),
    path('create_invoice_items', create_invoice_items, name='create_invoice_items'),
    path('display_single_order/<str:order_no>', display_single_order, name='display_single_order'),
    path('display_single_purchase/<str:purchase_no>', display_single_purchase, name='display_single_purchase'),
    path('sales_contract', sales_contract, name='sales_contract'),
    path('update_order', update_order, name='update_order'),
    path('update_purchase', update_purchase, name='update_purchase'),
    path('update_shipping', update_shipping, name='update_shipping'),
    path('edit_shipping', edit_shipping, name='edit_shipping'),
    path('create_orders', create_orders, name='create_orders'),
    path('completed_orders', completed_orders, name='completed_orders'),
    path('get_item_data/<str:item_id>/', get_item_data, name='get_item_data'),
    path('edit_order_only', edit_order_only, name='edit_order_only'),
    
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
