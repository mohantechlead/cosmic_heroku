from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import cosmic_order,cosmic_purchase,order_item,customer_profile,supplier_profile,shipping_info, order_item, purchase_item,cosmic_income
from .models import invoice_item, item_codes,cosmic_expense
# Register your models here.
admin.site.register(cosmic_order)
admin.site.register(cosmic_purchase)
admin.site.register(order_item)
admin.site.register(customer_profile)
admin.site.register(supplier_profile)
admin.site.register(shipping_info)
admin.site.register(purchase_item)
admin.site.register(invoice_item)
admin.site.register(item_codes)
admin.site.register(cosmic_income)
admin.site.register(cosmic_expense)

