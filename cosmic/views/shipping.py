from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from ..forms import *
from ..models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms import formset_factory,modelformset_factory
from django.db.models import Sum
from django.http import JsonResponse,HttpResponse
from django.template.loader import get_template
from django.contrib.auth.models import User, auth
from num2words import num2words
from django.contrib import messages
import os

def is_admin(user):
    return user.is_superuser

def create_shipping(request):
    if request.method == 'POST':
        ship_form = ShippingForm(request.POST)
        number = request.POST.get('order_no') 
        if ship_form.errors:
            print(ship_form.errors) 
        if ship_form.is_valid():
            
            order = cosmic_order.objects.get(order_no=number)
            
            # try:
            
            #     customer = customer_profile.objects.get(customer_name=notify_party_new)
            #     ship_form.instance.notify_party3 = customer
            # except customer_profile.DoesNotExist:
            #     customer = None
                
            ship_form.instance.order_no = order
            ship_form.instance.final_price = 0.00
            #print(purchase.vendor_name,"name")
            ship_form.save()
            messages.success(request,'Shipping added successfully')
            return render(request,'display_order.html')  # Redirect to the list of purchases or any other desired view
        else:
            print(ship_form.data,"nval")
    
        
    form = ShippingForm()
    formset = formset_factory(OrderItemForm, extra=1)
    formset = formset(prefix="items")

    # Render the form with the supplier choices
    customers = customer_profile.objects.all()
    return render(request, 'shipping_details.html', {'form': form, 'formset': formset, 'customers': customers})

def edit_order(request):

    if request.method == 'GET':
        order_no = request.GET.get('order_no')
        cosmic_order_instance = get_object_or_404(cosmic_order, order_no=order_no)
        items = order_item.objects.all()
        item = items.filter(order_no=cosmic_order_instance)
        item_names = []
        for name in item:
            item_names.append(name.item_name)
        print(item_names,"item")
        form = EditOrderForm(instance=cosmic_order_instance)  # Initialize the form with the instance data
      

        ship_form = ShippingForm(prefix="ship")
        customers = customer_profile.objects.all()
        # last_shipping_info = shipping_info.objects.order_by('-invoice_num').first()
        # print(last_shipping_info)
        # last_number = int(last_shipping_info.invoice_num.split('/')[1]) if last_shipping_info else 0
        # new_number = last_number + 1
        # generated_invoice_num = f"CCFZE/{new_number:03d}/2024"
        
    if request.method == 'POST':
        form = CosmicOrderForm(request.POST)
        

        order_no = request.POST.get('order_no')
        cosmic_order_instance = get_object_or_404(cosmic_order, order_no=order_no)
        refs_no = request.POST.get('ref_no')
        cosmic_order_instance.ref_no = refs_no
        cosmic_order_instance.measurement_type = request.POST.get('measurement_type')
        cosmic_order_instance.shipment_type = request.POST.get('shipment_type')
        cosmic_order_instance.freight = request.POST.get('freight')
        cosmic_order_instance.payment_type = request.POST.get('payment_type')
        cosmic_order_instance.transporation = request.POST.get('transporation')
        cosmic_order_instance.country_of_origin = request.POST.get('country_of_origin')
        cosmic_order_instance.final_destination = request.POST.get('final_destination')
        cosmic_order_instance.port_of_discharge = request.POST.get('port_of_discharge')
        cosmic_order_instance.port_of_loading = request.POST.get('port_of_loading')
        cosmic_order_instance.freight_price = request.POST.get('freight_price')
        consignees = request.POST.get('consignee')
        consignee = customer_profile.objects.get(customer_name=consignees)
        cosmic_order_instance.consignee = consignee
        print(cosmic_order_instance.consignee,"instance")
        notify_partys = request.POST.get('notify_party')
        notify_party = customer_profile.objects.get(customer_name=notify_partys)
        cosmic_order_instance.notify_party = notify_party
        notify_party2s = request.POST.get('notify_party2')
        try:
        
            notify_party2 = customer_profile.objects.get(customer_name=notify_party2s)
            cosmic_order_instance.notify_party2 = notify_party2
        except customer_profile.DoesNotExist:
            cosmic_order_instance.notify_party2  = None
        
        
        # cosmic_order_instance.save()
       
        my_customers = request.POST.get('customer_name')
        suppliers = request.POST.get('supplier_name')
        customer = customer_profile.objects.get(customer_name=my_customers)
        cosmic_order_instance.customer_name = customer
        supplier = supplier_profile.objects.get(supplier_name=suppliers)
        cosmic_order_instance.supplier_name = supplier
        # print(cosmic_order_instance.dict) 
        cosmic_order_instance.save()
        messages.success(request, 'Successfully Submitted')
        return redirect('display_order') 
     
    formset = formset_factory(InvoiceItemForm, extra=1)
    formset = formset(prefix="items")

    context = {
                'form': form, 
               'formset':formset, 
               'ship_form': ship_form,
                'cosmic_order_instance': cosmic_order_instance, 
                'item_names':item_names,
                'customers': customers, 
                'item':item
                }
    
    return render(request, 'shipping_details.html', context)

def commercial_invoice(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        inv_no = request.GET['invoice_num']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
        except cosmic_order.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                shipping = shipping_info.objects.get(order_no = pr_no)
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
                print(pr_items)
            except cosmic_purchase.DoesNotExist:
                order = None
                # Handle the case where the object doesn't exist in either table.
            order = None 
        try:
            
            shipping = shipping_info.objects.get(order_no = pr_no, invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping = None
        
        try:
            
            shipping_items = invoice_item.objects.all()
            shipping_items = shipping_items.filter(invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping_items = None

        if hasattr(shipping, 'final_price'):
            number = shipping.final_price
            print("yes",number)
        else:
            number = shipping.final_price
            print(shipping.final_price)
        dicts = {1:"TEN",2:"TWENTY",3:"THIRTY",4:"FORTY",5:"FIFTY",6:"SIXTY",7:"SEVENTY",8:"EIGHTY",9:"NINTY"}
        if shipping:
            if orders.freight_price:
                print(number,orders.freight_price,"try")
                number += float(orders.freight_price)
        print(number)

        whole_part, decimal_part = str(number).split('.')
        number_in_words = num2words(whole_part)
        number_in_words = number_in_words.replace(',', '')
        number_in_words = number_in_words.replace('-', ' ')
        num = number_in_words.upper()
        if int(decimal_part) in dicts:
            dec = " AND " + str(dicts[int(decimal_part)]) + " CENTS ONLY"
        elif decimal_part == "0":
            dec = " ONLY"
        else:
            dec = " AND " + num2words(decimal_part) + " CENTS ONLY"
      
        num = num.replace(' AND', '')
        num += dec 
        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'my_order': orders,
                        'shipping': shipping,
                        'num': num,
                        'number':number,
                        'shipping_items': shipping_items
                    }
            return render(request, 'commercial_invoice.html', context)
        context = {
                        
                        'my_order': orders,
                        'shipping': shipping,
                        'num': num,
                        'shipping_items': shipping_items,
                        'number':number,
                    }
    return render(request, 'commercial_invoice.html', context)

def bill_of_lading(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        inv_no = request.GET['invoice_num']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
            print(pr_items)
        except cosmic_order.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
                print(pr_items)
            except cosmic_purchase.DoesNotExist:
                order = None
                # Handle the case where the object doesn't exist in either table.
            order = None 
        try:
            
            shipping = shipping_info.objects.get(order_no = pr_no, invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping = None
        try:
            
            shipping_items = invoice_item.objects.all()
            shipping_items = shipping_items.filter(invoice_num=inv_no)
        except invoice_item.DoesNotExist:
            shipping_items = None
       
        if pr_items.exists():
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items':shipping_items,
                    }
            return render(request, 'bill_of_lading.html', context)
        context = {
                        
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items': shipping_items,
                    }
    return render(request, 'bill_of_lading.html', context)
def truck_waybill(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        inv_no = request.GET['invoice_num']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
            print(pr_items)
        except cosmic_order.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
                print(pr_items)
            except cosmic_purchase.DoesNotExist:
                order = None
                # Handle the case where the object doesn't exist in either table.
            order = None 
        try:
            
            shipping = shipping_info.objects.get(order_no = pr_no, invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping = None
        try:
            
            shipping_items = invoice_item.objects.all()
            shipping_items = shipping_items.filter(invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping_items = None

        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items': shipping_items,
                    }
            return render(request, 'truck_waybill.html', context)
        context = {
                        
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items': shipping_items,
                    }
    return render(request, 'truck_waybill.html', context)


def packing_list(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        inv_no = request.GET['invoice_num']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
            print(pr_items)
        except cosmic_order.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                shipping = shipping_info.objects.get(order_no = pr_no)
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
                print(pr_items)
            except cosmic_purchase.DoesNotExist:
                order = None
            order = None 
        try:
            
            shipping = shipping_info.objects.get(order_no = pr_no, invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping = None
        try:
            
            shipping_items = invoice_item.objects.all()
            shipping_items = shipping_items.filter(invoice_num=inv_no)
        except invoice_item.DoesNotExist:
            shipping_items = None
        print(orders)
        print("no")
        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items':shipping_items,
                    }
            return render(request, 'packing_list.html', context)
        context = {
                        
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items':shipping_items,
                    }
    return render(request, 'packing_list.html', context)

def create_invoice_items(request):
    
    if request.method == 'POST':
        formset = formset_factory(InvoiceItemForm, extra=1, min_num=1)
        
        formset = formset(request.POST or None,prefix="items")
        #print(formset.data,"r")
      
        if formset.errors:
            print(formset.errors)   
        
        # Check if 'PR_no' field is empty in each form within the formset
        for form in formset:
            print(form,"form")
        non_empty_forms = [form for form in formset if form.cleaned_data.get('item_name')]
        pr_no = request.POST.get('order_no')
        invoice_no = request.POST.get('invoice_num')
        bags = request.POST.get('bags')
        pr = cosmic_order.objects.get(order_no = pr_no)
        invoice = shipping_info.objects.get(invoice_num = invoice_no)
        if non_empty_forms:
            print("yes")
            if formset.is_valid():
                final_price = 0.00
                total_bags = 0
                for form in non_empty_forms:
                    #form.instance.remaining = form.cleaned_data['quantity']
                    form.instance.order_no = pr
                    form.instance.invoice_num = invoice
                    items = form.cleaned_data['item_name']
                    item = item_codes.objects.all()
                    item = item.filter(item_name = items).first()
                    
                    form.instance.hs_code = item.hs_code
                    #final_quantity += form.cleaned_data['quantity']
                    final_price += float(form.cleaned_data['before_vat'])
                    total_bags += int(form.cleaned_data['bags'])
                    print(total_bags)
                    print(form.cleaned_data['before_vat'])
                    form.save()
                    # messages.success(request,"successful!")
                    # return redirect('display_order')
                
                invoice.final_price = final_price
                invoice.total_bags = total_bags
                #pr.total_quantity = final_quantity
                #pr.remaining = final_quantity
                invoice.save()
                pr.save()
                
            else:
                print(formset.data,"nval")
                # errors = dict(formset.errors.items())
                # return JsonResponse({'form_errors': errors}, status=400)
        
            
            context = {
                'formset': formset,
                # 'message':success_message,
            }
            return render(request, 'shipping_details.html', context)
    else:
       
        formset = formset_factory(InvoiceItemForm, extra=1)
        
        formset = formset(prefix="items")

    context = {
        'formset': formset,
    }
    return render(request, 'shipping_details.html', context)

def edit_shipping(request):
      
    if request.method == 'GET':
        order_no = request.GET.get('invoice_num')
       
        try:
            shipping_instance = shipping_info.objects.get(invoice_num = order_no)
            items = purchase_item.objects.all()
           
            
        except shipping_info.DoesNotExist:
            
            order = None 
        
        
        form = EditShippingForm(instance=shipping_instance)  # Initialize the form with the instance data
        
    if request.method == 'POST':
    
        order_no = request.POST.get('invoice_num')
        try:
            shipping_instance = shipping_info.objects.get(invoice_num = order_no)
            
        except shipping_info.DoesNotExist:
            
            order = None 
        shipping_instance = shipping_info.objects.get(invoice_num=order_no)
        form = EditShippingForm(request.POST, instance=shipping_instance)
        
        if form.is_valid():
            form.save()

            return (render(request,"shipping_update.html"))

        
        return render(request, 'shipping_update.html')  # Redirect to a success page or another URL
    
    
    return render(request, 'shipping_update.html', {'form': form,'shipping_instance': shipping_instance})


def update_shipping(request):
     
    if request.method == "POST":
        print(request.POST)
        invoice_no = request.POST.get('invoice_num')
        shipping_instance = get_object_or_404(shipping_info, invoice_num=invoice_no)
        invoice_item_formset = modelformset_factory(invoice_item, form=InvoiceItemForm, extra=0)  
        print(shipping_instance.invoice_date,"date")
        formset = invoice_item_formset(request.POST)
        if formset.is_valid():
            print("valid")
            # instances = formset.save(commit=False)
            final_price = 0
            total_bags = 0
            for instance in formset:
                print("here")
                total_bags += int(instance.cleaned_data['bags'])
                final_price += float(instance.cleaned_data['before_vat'])
                print("Field names:", instance.__dict__.keys())
                instance.invoice_num = shipping_instance
                print(final_price,"price")
                print(instance,"instance")
                
                instance.save()
            shipping_instance.final_price = final_price
            shipping_instance.total_bags = total_bags
            shipping_instance.save()
            # Redirect to another page after saving all instances
            return render(request, "create_order.html")
    else:
        invoice_no = request.GET.get('invoice_num')
        shipping_instance = get_object_or_404(shipping_info, invoice_num=invoice_no)
        shipping_instance.final_price = 0.0
        date = shipping_instance.invoice_date
        date = str(date)
        invoice_item_formset = modelformset_factory(invoice_item, form=InvoiceItemForm, extra=0)
        queryset = invoice_item.objects.filter(invoice_num=shipping_instance)
        formset = invoice_item_formset(queryset=queryset)
        print(shipping_instance.invoice_date,"date")
    
    for form in formset.forms:
        if form.errors:
            print(form.errors)
    print(date,"datess")
    context = {
        "formset": formset,
        'shipping_instance': shipping_instance, 
        "date":date
    }
    return render(request, "shipping_update.html", context)