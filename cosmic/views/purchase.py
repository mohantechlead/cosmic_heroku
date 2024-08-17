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

def display_purchase(request):
    if request.method == 'GET':
        orders = cosmic_purchase.objects.all()
        orders = orders.order_by('purchase_no')

        print("ord")
        orders_data = []
        print(orders)
        for order in orders:
            # Fetch all order items related to each cosmic order
            order_items = purchase_item.objects.filter(purchase_no=order.purchase_no)
            print(purchase_item.objects.all())
            # Create a dictionary containing order details and items
            order_data = {
                'purchase_no': order.purchase_no,
                'date': order.date,  # Assuming 'date' is a field in CosmicOrder
                'order_items': order_items,  # Assuming a related name 'order_items' on CosmicOrder pointing to OrderItem
                'before_vat': order.before_vat,  # Assuming 'PR_before_vat' is a field in CosmicOrder
                'total_quantity': order.total_quantity,  # Assuming 'total_quantity' is a field in CosmicOrder
                'supplier_name': order.supplier_name,  # Assuming 'customer_name' is a field in CosmicOrder
                'status': order.status, 
                'ref_no':order.ref_no,
                  # Assuming 'status' is a field in CosmicOrder
            }
            orders_data.append(order_data)
            print(orders_data)
    context = {
        'my_purchase': orders_data,
    }
    return render(request, 'display_purchase.html', context)

def create_purchase_items(request):
    
    if request.method == 'POST':
        formset = formset_factory(PurchaseItemForm, extra=1, min_num=1)
        
        formset = formset(request.POST or None,prefix="items")
        #print(formset.data,"r")
      
        if formset.errors:
            print(formset.errors)   
        
        # Check if 'PR_no' field is empty in each form within the formset
        for form in formset:
            print(form,"form")
        non_empty_forms = [form for form in formset if form.cleaned_data.get('item_name')]
        pr_no = request.POST.get('purchase_no')
        print(pr_no,"pr_no")
        if non_empty_forms:
            if formset.is_valid():
                final_quantity = 0.0
                final_price = 0.00
                pr = cosmic_purchase.objects.get(purchase_no=pr_no)
                print(pr,"printing")
                for form in non_empty_forms:
                    form.instance.remaining = form.cleaned_data['quantity']
                    form.instance.purchase_no = pr
                    items = form.cleaned_data['item_name']
                    form.instance.item_name = items
                    item = item_codes.objects.all()
                    item = item.filter(item_name = items).first()
                    code = item.hs_code
                    form.instance.hs_code = code
                    final_quantity += form.cleaned_data['quantity']
                    final_price += float(form.cleaned_data['before_vat'])
                    
                    form.save()
                
                pr.before_vat = final_price
                pr.total_quantity = final_quantity
                pr.remaining = final_quantity
                pr.save()
                #message.success("successful!")
            else:
                print(formset.data,"nval")
                errors = dict(formset.errors.items())
                return JsonResponse({'form_errors': errors}, status=400)
        
            pr_form = CosmicPurchaseForm(prefix="orders")
            formset = formset_factory(PurchaseItemForm, extra=1)
            formset = formset(prefix="items")

            context = {
                'pr_form': pr_form,
                'formset': formset,
                # 'message':success_message,
            }
            return render(request, 'create_purchase.html', context)
    else:
       
        formset = formset_factory(OrderItemForm, extra=1)
        formset = formset(prefix="items")

    context = {
        'formset': formset,
    }
    return render(request, 'create_order.html', context)

def display_single_purchase(request, purchase_no):
    purchase= cosmic_purchase.objects.get(purchase_no = purchase_no)
    if request.method == 'GET':
        pr_items = purchase_item.objects.all()
        pr_items = pr_items.filter(purchase_no=purchase_no)
        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'pr_items': pr_items,
                        'my_order': purchase,
                        'purchase_no': purchase_no,
                    }
            return render(request, 'display_single_purchase.html', context)
        context = {
                        
                        'my_order': purchase,
                        'purchase_no': purchase_no
                    }
    return render(request, 'display_single_purchase.html', context)

def edit_purchase(request):
      
    if request.method == 'GET':
        print("in")
        purchase_no = request.GET.get('purchase_no')
        print(purchase_no)
        try:
            cosmic_purchase_instance = cosmic_purchase.objects.get(purchase_no = purchase_no)
            items = purchase_item.objects.all()
            item = items.filter(purchase_no=cosmic_purchase_instance)
            item_names = []
            for name in item:
                item_names.append(name.item_name)
            print("l")
            
        except cosmic_purchase.DoesNotExist:
            print("h")
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                cosmic_purchase_instance = cosmic_purchase.objects.get(purchase_no = purchase_no)
                print(cosmic_purchase_instance,"inst")
                items = purchase_item.objects.all()
                item = items.filter(purchase_no=cosmic_purchase_instance)
                item_names = []
                for name in item:
                    item_names.append(name.item_name)
                
            except cosmic_purchase.DoesNotExist:
                purchase = None
            purchase = None 
        
        
        form = EditPurchaseForm(instance=cosmic_purchase_instance)  # Initialize the form with the instance data
      
        
        customers = customer_profile.objects.all()
        
        
    if request.method == 'POST':
        form = CosmicPurchaseForm(request.POST)
        purchase_no = request.POST.get('purchase_no')
        try:
            cosmic_purchase_instance = cosmic_purchase.objects.get(purchase_no = purchase_no)
            
        except cosmic_purchase.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                cosmic_purchase_instance = cosmic_purchase.objects.get(purchase_no = purchase_no)
                
            except cosmic_purchase.DoesNotExist:
                order = None
            order = None 
        
        refs_no = request.POST.get('ref_no')
        cosmic_purchase_instance.ref_no = refs_no
        cosmic_purchase_instance.measurement_type = request.POST.get('measurement_type')
        cosmic_purchase_instance.shipment_type = request.POST.get('shipment_type')
        cosmic_purchase_instance.freight = request.POST.get('freight')
        cosmic_purchase_instance.payment_type = request.POST.get('payment_type')
        cosmic_purchase_instance.transportation = request.POST.get('transportation')
        cosmic_purchase_instance.country_of_origin = request.POST.get('country_of_origin')
        cosmic_purchase_instance.final_destination = request.POST.get('final_destination')
        cosmic_purchase_instance.port_of_discharge = request.POST.get('port_of_discharge')
        cosmic_purchase_instance.port_of_loading = request.POST.get('port_of_loading')
        cosmic_purchase_instance.conditions = request.POST.get('conditions')
        consignees = request.POST.get('consignee')
        notify_partys = request.POST.get('notify_party')
        notify_party2s = request.POST.get('notify_party2')
        
        
        try:
        
            consignee = customer_profile.objects.get(customer_name=consignees)
            cosmic_purchase_instance.consignee = consignee
        except customer_profile.DoesNotExist:
            cosmic_purchase_instance.notify_party  = None
           
        try:
        
            notify_party = customer_profile.objects.get(customer_name=notify_partys)
            cosmic_purchase_instance.notify_party = notify_party
        except customer_profile.DoesNotExist:
            cosmic_purchase_instance.notify_party  = None

        try:
        
            notify_party2 = customer_profile.objects.get(customer_name=notify_party2s)
            cosmic_purchase_instance.notify_party2 = notify_party2
        except customer_profile.DoesNotExist:
            cosmic_purchase_instance.notify_party2  = None
        
        
        cosmic_purchase_instance.save()
       
        my_customers = request.POST.get('customer_name')
        suppliers = request.POST.get('supplier_name')
        customer = customer_profile.objects.get(customer_name=my_customers)
        cosmic_purchase_instance.customer_name = customer
        supplier = supplier_profile.objects.get(supplier_name=suppliers)
        cosmic_purchase_instance.supplier_name = supplier
        print(cosmic_purchase_instance.__dict__) 
        cosmic_purchase_instance.save()
        return render(request, 'edit_purchase.html')  # Redirect to a success page or another URL
    
        print(cosmic_purchase_instance.order_no,"d")
    
    return render(request, 'edit_purchase.html', {'form': form,'cosmic_purchase_instance': cosmic_purchase_instance, 
                                               'customers': customers})

def print_purchase(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
            
        except cosmic_order.DoesNotExist:
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
            except cosmic_purchase.DoesNotExist:
                orders = None
        
        
        if hasattr(orders, 'PR_before_vat'):
            number = float(orders.PR_before_vat)
            print("yes")
        else:
            number = float(orders.before_vat)
            print(orders.before_vat)

        if orders.freight_price:
            number += float(orders.freight_price)
        #print(shipping.freight_amount,"fr")
        dicts = {1:"TEN",2:"TWENTY",3:"THIRTY",4:"FORTY",5:"FIFTY",6:"SIXTY",7:"SEVENTY",8:"EIGHTY",9:"NINTY"}
        
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
        print(decimal_part,dec)
        num = num.replace(' AND', '')
        num += dec 
        print(orders, num)
        print("no")
        
        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                        'num': num,
                        'number':number,
                        # 'shipping':shipping,
                    }
            return render(request, 'print_purchase.html', context)
       
        context = {
                        
                        'my_order': orders,
                        'num': num,
                        'number':number,
                        # 'shipping':shipping,
                    }
       
    return render(request, 'print_purchase.html', context)

def create_purchase(request):
    if request.method == 'POST':
        form = CosmicPurchaseForm(request.POST)
        if form.errors:
            print(form.errors) 
        if form.is_valid():
            print(form.data,"val")
            # Save the form, and link the purchase to the selected supplier
            customers_name = request.POST.get('customer_name') 
            notify_party = request.POST.get('notify_party') 
            suppliers_name = request.POST.get('supplier_name') 

            customer = customer_profile.objects.get(customer_name=customers_name)
            if notify_party:
                notify_1 = customer_profile.objects.get(customer_name=notify_party)
                form.instance.notify_party = notify_1
            supplier = supplier_profile.objects.get(supplier_name=suppliers_name)
            form.instance.customer_name = customer
            form.instance.supplier_name = supplier
            #print(purchase.vendor_name,"name")
            form.save()
            return redirect('create_purchase')  # Redirect to the list of purchases or any other desired view
        else:
            print(form.data,"nval")
            errors = dict(form.errors.items())
            return JsonResponse({'form_errors': errors}, status=400)
        
   
        
    form = CosmicPurchaseForm()
    formset = formset_factory(PurchaseItemForm, extra=1)
    formset = formset(prefix="items")
    # Render the form with the supplier choices
    
    customers = customer_profile.objects.all()
    suppliers = supplier_profile.objects.all()
    return render(request, 'create_purchase.html', {'form': form, 'formset': formset ,'suppliers': suppliers,'customers':customers})

def update_purchase(request):
     
    if request.method == "POST":
        print(request.POST)
        purchase_no = request.POST.get('purchase_no')
        cosmic_purchase_instance = get_object_or_404(cosmic_purchase, purchase_no=purchase_no)
        purchase_item_formset = modelformset_factory(purchase_item, form=PurchaseItemForm, extra=0)
     
        formset = purchase_item_formset(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            if instances:
                final_price = 0
            else:
                final_price = cosmic_purchase_instance.before_vat
            for instance in instances:
                final_price += instance.before_vat
                
                print("Field names:", instance.__dict__.keys())
                instance.purchase = cosmic_purchase_instance
                print(final_price,"price")
                instance.save()
            cosmic_purchase_instance.PR_before_vat = final_price
            cosmic_purchase_instance.save()
            # Redirect to another page after saving all instances
            return render(request, "create_purchase.html")
    else:
        purchase_no = request.GET.get('purchase_no')
        cosmic_purchase_instance = get_object_or_404(cosmic_purchase, purchase_no=purchase_no)

        purchase_item_formset = modelformset_factory(purchase_item, form=PurchaseItemForm, extra=0)
        queryset = purchase_item.objects.filter(purchase_no=cosmic_purchase_instance)
        formset = purchase_item_formset(queryset=queryset)
    
    for form in formset.forms:
        if form.errors:
            print(form.errors)
    
    context = {
        "formset": formset,
        'cosmic_purchase_instance': cosmic_purchase_instance, 
    }
    return render(request, "purchase_update.html", context)
