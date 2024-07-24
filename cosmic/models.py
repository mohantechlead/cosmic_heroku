from django.db import models
from django.forms import ModelForm
import uuid
# Create your models here.
class customer_profile(models.Model):
    #customer_id = models.AutoField(primary_key=True)
    customer_name = models.TextField(blank=True,primary_key=True)
    customer_address = models.TextField(blank=True)
    contact_person = models.TextField(blank=True)
    phone_number = models.CharField(blank=True, null=True)  # This field type is a guess.
    email = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)

class supplier_profile(models.Model):
    #supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.TextField(primary_key=True)
    supplier_address = models.TextField(blank=True)
    contact_person = models.TextField(blank=True)
    phone_number = models.CharField(blank=True, null=True)  # This field type is a guess.
    email = models.TextField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

class cosmic_order(models.Model):
    customer_name = models.ForeignKey('customer_profile', related_name='orders_related_to_customer',on_delete=models.CASCADE, db_column='customer_name',blank=False, null=True)
    order_no = models.TextField(primary_key=True)
    notify_party = models.ForeignKey('customer_profile', related_name='notify_party_one',on_delete=models.CASCADE, blank=True, null=True,db_column='notify_party')
    consignee = models.ForeignKey('customer_profile', related_name='consignee',on_delete=models.CASCADE, blank=True, null=True,db_column='consignee')
    notify_party2 = models.ForeignKey('customer_profile', related_name='orders_related_to_bank', on_delete=models.CASCADE, db_column='notify_party2',blank=True, null=True)
    date = models.DateField(blank=False)
    freight = models.TextField(blank=True, null=True)
    freight_price = models.FloatField(blank=True, null=True)
    payment_type = models.TextField(blank=True, null=True)
    measurement_type = models.TextField(blank=True, null=True)
    transportation = models.TextField(blank=True, null=True)
    shipment_type = models.TextField(blank=True, null=True)
    approved_by = models.TextField(blank=True, null=True)
    PR_before_vat = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True, default="Pending")
    status_remark = models.TextField(blank=True, null=True)
    ref_no = models.TextField(blank=False, null=True)
    total_quantity = models.FloatField(blank=True, null=True)
    remaining =  models.FloatField(blank=True, null=True)
    supplier_name = models.ForeignKey('supplier_profile', related_name='orders_related_to_supplier',on_delete=models.CASCADE, blank=False, null=True,db_column='supplier_name')
    port_of_loading = models.TextField(blank=False, null=True)
    port_of_discharge = models.TextField(blank=True, null=True)
    final_destination = models.TextField(blank=True, null=True)
    country_of_origin = models.TextField(blank=False, null=True)
    
class cosmic_purchase(models.Model):
    customer_name = models.ForeignKey('customer_profile', related_name='purchase_related_to_customer',on_delete=models.CASCADE, db_column='customer_name',blank=False, null=True)
    supplier_name = models.ForeignKey('supplier_profile', on_delete=models.CASCADE, db_column='supplier_name',blank=True, null=True)
    purchase_no = models.TextField(primary_key=True)
    notify_party = models.ForeignKey('customer_profile', related_name='purchase_notify_party_one',on_delete=models.CASCADE, blank=True, null=True,db_column='notify_party')
    consignee = models.ForeignKey('customer_profile', related_name='purchase_consignee',on_delete=models.CASCADE, blank=True, null=True,db_column='consignee')
    notify_party2 = models.ForeignKey('customer_profile', related_name='purchase_related_to_bank', on_delete=models.CASCADE, db_column='notify_party2',blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    freight = models.TextField(blank=True, null=True)
    freight_price = models.FloatField(blank=True, null=True)
    measurement_type = models.TextField(blank=True, null=True)
    transportation = models.TextField(blank=True, null=True)
    shipment_type = models.TextField(blank=True, null=True)
    payment_type = models.TextField(blank=True, null=True)
    approved_by = models.TextField(blank=True, null=True)
    before_vat = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True, default="Pending")
    status_remark = models.TextField(blank=True, null=True)
    ref_no = models.TextField(blank=False, null=True)
    remaining = models.FloatField(blank=True, null=True)
    total_quantity = models.FloatField(blank=True, null=True)
    port_of_loading = models.TextField(blank=False, null=True)
    port_of_discharge = models.TextField(blank=True, null=True)
    final_destination = models.TextField(blank=True, null=True)
    country_of_origin = models.TextField(blank=False, null=True)
    conditions = models.TextField(blank=True, null=True)

class shipping_info(models.Model):
    invoice_date = models.DateField(blank=True, null=True)
    order_no = models.ForeignKey('cosmic_order', on_delete=models.CASCADE, db_column='order_no',blank=True, null=True)
    invoice_num = models.TextField(primary_key=True)
    container_no = models.TextField(blank=True, null=True)
    truck_waybill_no = models.TextField(blank=True, null=True)
    customer_no = models.TextField(blank=True, null=True)
    freight_amount = models.FloatField(blank=True, null=True)
    vessel = models.TextField(blank=True, null=True)
    total_net_weight = models.FloatField(blank=True, null=True)
    total_gross_weight = models.FloatField(blank=True, null=True)
    reference_no = models.TextField(blank=True, null=True)
    total_bags = models.FloatField(blank=True, null=True)
    total_net_weight = models.FloatField(blank=True, null=True)
    total_gross_weight = models.FloatField(blank=True, null=True)
    invoice_remark = models.TextField(blank=True, null=True)
    lading_remark = models.TextField(blank=True, null=True)
    waybill_remark = models.TextField(blank=True, null=True)
    packing_remark = models.TextField(blank=True, null=True)
    final_price = models.FloatField(blank= True, null=True)
    
class order_item(models.Model):
    order_no = models.ForeignKey('cosmic_order', on_delete=models.CASCADE, db_column='order_no',blank=True, null=True)
    id_numeric = models.AutoField(primary_key=True)
    hs_code = models.TextField(blank=True, null=True)
    item_name = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    before_vat = models.FloatField(blank=True, null=True)
    quantity =  models.FloatField(blank=True, null=True)
    measurement = models.TextField(blank=True, null=True)

class purchase_item(models.Model):
    purchase_no = models.ForeignKey('cosmic_purchase', on_delete=models.CASCADE, db_column='purchase_no',blank=True, null=True)
    id_numeric = models.AutoField(primary_key=True)
    hs_code = models.TextField(blank=True, null=True)
    item_name = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    before_vat = models.FloatField(blank=True, null=True)
    quantity =  models.FloatField(blank=True, null=True)
    measurement = models.TextField(blank=True, null=True)
    remaining = models.TextField(blank= True, null=True)

class invoice_item(models.Model):
    #invoice_num = models.ForeignKey('shipping_info', on_delete=models.CASCADE, db_column='invoice_num',blank=True, null=True, to_field='invoice_num')
    invoice_num = models.ForeignKey('shipping_info', on_delete=models.CASCADE, db_column='invoice_num',blank=True, null=True, to_field='invoice_num')
   
    id_numeric = models.AutoField(primary_key=True)
    hs_code = models.TextField(blank=True, null=True)
    item_name = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    before_vat = models.FloatField(blank=True, null=True)
    quantity =  models.FloatField(blank=True, null=True)
    measurement = models.TextField(blank=True, null=True)
    net_weight = models.FloatField(blank=True, null=True)
    gross_weight = models.FloatField(blank=True, null=True)
    bags = models.FloatField(blank=True, null=True)

class item_codes(models.Model):
    hs_code = models.TextField(blank=True, null=True)
    item_name = models.TextField(blank=True, null=True)
    new_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    def __str__(self):
        return self.item_name
   # item_id = models.TextField(primary_key = True)

class cosmic_income(models.Model):
    serial_no = models.TextField(blank=False, null=False, primary_key=True)
    amount = models.FloatField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    reference = models.TextField(blank=True, null=True)
    payment_type = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    date = models.DateField(blank=False)


class cosmic_expense(models.Model):
   serial_no = models.TextField(blank=False, null=False, primary_key=True)
   date = models.DateField(blank=False)
   amount = models.FloatField(blank=True, null=True)
   purpose = models.TextField(blank=True, null=True)
   reference = models.TextField(blank=True, null=True)
   attachement = models.FileField(blank=True, null=True, upload_to="media/")

class GRN(models.Model):
    GRN_no = models.TextField(primary_key=True)
    grn_date = models.DateField(blank=True, null=True)
    recieved_from = models.TextField(blank=True, null=True)
    transporter_name = models.TextField(blank=True, null=True)
    truck_no = models.TextField(blank=True, null=True)
    store_name =  models.TextField(blank=True, null=True) # This field type is a guess.
    store_keeper = models.TextField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'GRN'

class GRNItem(models.Model):
    id = models.AutoField(primary_key=True)
    quantity = models.FloatField(null=True, blank=True)
    item_name = models.CharField(null=True, blank=True)
