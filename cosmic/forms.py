from django import forms
from django.forms import ModelForm
from .models import *
from django.forms import inlineformset_factory

class CustomerForm(forms.ModelForm):
    
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'phone_number form-control' }))
    customer_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'customer_address form-control'}))

    customer_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter e-mail'}),
    )
    
    class Meta:
   
        model = customer_profile
        fields = ['customer_name','customer_address','email','phone_number','contact_person','comments']

class SupplierForm(forms.ModelForm):
    #phone_number = 
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'phone_number form-control' }))
    supplier_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'customer_address form-control'}))

    supplier_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'}),
    )
    email = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter e-mail'}),
    )
    
    class Meta:
   
        model = supplier_profile
        fields = ['supplier_name','supplier_address','email','phone_number','contact_person','comments']

class CosmicOrderForm(forms.ModelForm):
    
    order_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'order_no form-control'}))
    freight_price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'freight_price form-control'}), required=False)
    
    class Meta:
   
        model = cosmic_order
        fields = ['freight_price','customer_name','supplier_name','order_no','date','payment_type','measurement_type','approved_by','PR_before_vat','total_quantity','transportation','shipment_type','freight','ref_no','notify_party','country_of_origin','final_destination','port_of_discharge','port_of_loading','notify_party2','consignee']
        
class OrderItemForm(forms.ModelForm):
   
    before_vat = forms.DecimalField(
        label='Total Price',
        required=False,
        widget=forms.TextInput(attrs={'class': 'before_vat form-control'})
    )
    measurement = forms.CharField(widget=forms.TextInput(attrs={'class': 'measurement form-control'}), required=False)
    quantity = forms.FloatField(widget=forms.TextInput(attrs={'class': 'quantity form-control' }))
    price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'price form-control'}))

    item_name = forms.ModelChoiceField(
        queryset=item_codes.objects.all(),
        empty_label="Item Name", 
        widget=forms.Select(attrs={'class': 'item_name form-control'}),
        to_field_name='item_name'
    )
    hs_code = forms.CharField(label='HS CODE', required=False, widget=forms.TextInput(attrs={'class': 'hs_codes form-control'}))
    
    
    class Meta:
   
        model = order_item
        fields = [ 'item_name','hs_code','price','quantity','before_vat','measurement']

class PurchaseItemForm(forms.ModelForm):
   
    item_name = forms.ModelChoiceField(
        queryset=item_codes.objects.all().order_by('item_name'),
        empty_label="Item Name", 
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='item_name'
    )
    
    before_vat = forms.DecimalField(
        label='Total Price',
        required=False,
        widget=forms.TextInput(attrs={'class': 'before_vat form-control', 'readonly': 'readonly'})
    )
    measurement = forms.CharField(widget=forms.TextInput(attrs={'class': 'measurement form-control'}), required=False)
    quantity = forms.FloatField(widget=forms.TextInput(attrs={'class': 'quantity form-control' }))
    price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'price form-control'}))
    
        
    
    
    class Meta:
   
        model = purchase_item
        fields = [ 'item_name','price','quantity','before_vat','measurement']
        
class CosmicPurchaseForm(forms.ModelForm):
    
    purchase_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'purchase_no form-control'}))

    class Meta:
   
        model = cosmic_purchase
        fields = ['freight_price','customer_name','supplier_name','purchase_no','date','payment_type','measurement_type','approved_by','before_vat','total_quantity','transportation','shipment_type','freight','ref_no','notify_party','country_of_origin','final_destination','port_of_discharge','port_of_loading','notify_party2','consignee','conditions']
        
class ShippingForm(forms.ModelForm):
    
    class Meta:
   
        model = shipping_info
        fields = [ 'invoice_num','final_price','waybill_remark','packing_remark','lading_remark', 'invoice_remark','customer_no','invoice_date','vessel','container_no','truck_waybill_no']

class EditShippingForm(forms.ModelForm):
    
    class Meta:
   
        model = shipping_info
        fields = [ 'invoice_num','final_price','waybill_remark','packing_remark','lading_remark', 'invoice_remark','customer_no','invoice_date','vessel','container_no','truck_waybill_no']
        exclude = ['invoice_num']

class EditOrderForm(forms.ModelForm):
    
    total_quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'total_quantity form-control' }),required=False)
    order_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'order_no form-control'}))

    
    class Meta:
   
        model = cosmic_order
        fields = ['customer_name','supplier_name','order_no','date','payment_type','measurement_type','approved_by','PR_before_vat','total_quantity','transportation','shipment_type','freight','ref_no','notify_party']
        exclude = ['order_no'] 

class EditPurchaseForm(forms.ModelForm):
    
    total_quantity = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'total_quantity form-control' }),required=False)
    purchase_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'purchase_no form-control'}))

    
    class Meta:
   
        model = cosmic_purchase
        fields = ['customer_name','supplier_name','purchase_no','date','payment_type','measurement_type','approved_by','before_vat','total_quantity','transportation','shipment_type','freight','ref_no','notify_party']
        exclude = ['purchase_no'] 

class approvalForm(forms.Form):
    selected_orders = forms.ModelMultipleChoiceField(
        queryset= cosmic_order.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    action = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('reject', 'Reject'), ('complete', 'Complete')],
        widget=forms.RadioSelect,
    )
    approval = forms.CharField(
        widget=forms.TextInput,
        required=True 
    ) 

class PurchaseApprovalForm(forms.Form):
    selected_orders = forms.ModelMultipleChoiceField(
        queryset= cosmic_purchase.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    action = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('reject', 'Reject')],
        widget=forms.RadioSelect,
    )
    approval = forms.CharField(
        widget=forms.TextInput,
        required=True 
    ) 
class InvoiceItemForm(forms.ModelForm):
   
    before_vat = forms.DecimalField(
        label='Total Price',
        required=False,
        widget=forms.TextInput(attrs={'class': 'before_vat form-control', 'readonly': 'readonly'})
    )
    measurement = forms.CharField(widget=forms.TextInput(attrs={'class': 'measurement form-control'}), required=False)
    quantity = forms.FloatField(widget=forms.TextInput(attrs={'class': 'quantity form-control' }))
    price = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'price form-control'}))
    bags = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'bags form-control'}))
    net_weight = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'net_weight form-control'}), label="Net weight")
    gross_weight = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'gross_weight form-control'}), label="Gross weight")
    
    item_name = forms.ModelChoiceField(
        queryset=item_codes.objects.all(),
        empty_label="Item Name", 
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='item_name'
    )
    
    
    class Meta:
   
        model = invoice_item
        fields = ['item_name','price','quantity','before_vat','measurement','bags','net_weight','gross_weight']

class restoreForm(forms.Form):
    selected_orders = forms.ModelMultipleChoiceField(
        queryset= cosmic_order.objects.filter(status='rejected'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    action = forms.ChoiceField(
        choices=[('approve', 'Approve'), ('delete', 'Delete'),('restore', 'Restore')],
        widget=forms.RadioSelect,
    )
    approval = forms.CharField(
        widget=forms.TextInput,
        required=True 
    )

class CosmicItemForm(forms.ModelForm):
    
    item_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'item_name form-control'}))
    hs_code = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'hs_code form-control'}))
    
    class Meta:
   
        model = item_codes
        fields = ['item_name','hs_code']

trialFormset = inlineformset_factory(
    cosmic_order, order_item, form=OrderItemForm, extra=1, can_delete=True, can_delete_extra = True
)   

class CosmicGRNForm(forms.ModelForm):
    class Meta:

        model = cosmic_grn
        fields=['GRN_no','grn_date','recieved_from','transporter_name','truck_no','store_name','store_keeper']

class CosmicGRNItemForm(forms.ModelForm):
    class Meta:
        model = cosmic_grnitem
        fields = ['item_name', 'quantity']

class DeliveryForm(forms.ModelForm):
    delivery_number = forms.IntegerField(required=True)
    class Meta:
        model = cosmic_delivery
        fields = ['delivery_number','delivery_date', 'delivery_quantity','truck_number','driver_name','recipient_name','delivery_comment']
