from django.shortcuts import render, redirect,get_object_or_404
from django.conf import settings
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required,user_passes_test
from django.forms import formset_factory,modelformset_factory
from django.db.models import Sum
from django.http import JsonResponse,HttpResponse
from django.template.loader import get_template
from django.contrib.auth.models import User, auth
from num2words import num2words
from django.contrib import messages

import os
# Create your views here.

def is_admin(user):
    return user.is_superuser

def create_customer(request):
    if request.method == 'POST':
        email = request.POST['email']
        form = CustomerForm(request.POST)
        if form.errors:
            print(form.errors)
        if customer_profile.objects.filter(email = email). exists():
            messages.error(request, 'Email Already exists')
            return redirect('create_customer')
        # elif customer_profile.objects.filter(name = name). exists():
        #     messages.error(request, 'Email Already exists')
        #     return redirect('create_customer')
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Successfully Submitted')
            except Exception as e:
                print(f"Error: {e}")
            return redirect('create_customer')
    else:
        
        form = CustomerForm()
    return render(request, 'create_customer.html', {'form': form })

def display_customers(request):
    if request.method == 'GET':
        customers = customer_profile.objects.all()
        context = {
                    'my_customer': customers,
                }
          
        return render(request, 'display_customer.html', context)

def display_customer_profile(request, customer_name):
    if request.method == 'GET':
        # customer_name = request.GET['customer_name']
        
        customers = customer_profile.objects.get(customer_name= customer_name)
         
        context = {
                        
                        'my_customer': customers,
                        
                    }
    return render(request, 'customer_profile.html', context)   

# def delete_customer(request, customer_name):
#     name = customer_profile.objects.get(customer_name = customer_name)
#     if request.method == 'POST':
#         name.delete()
#     return redirect('display_customers')

def delete_customer_profile(request):

    name = request.GET['customer_name']
    print("names,",name)
    customer_instance = get_object_or_404(customer_profile, customer_name = name)
    print(customer_instance,"instance")
    customer_instance.delete()

    return render(request, 'display_customer.html')

def delete_supplier_profile(request):

    name = request.GET['supplier_name']
    print("names,",name)
    supplier_instance = get_object_or_404(supplier_profile, supplier_name = name)
    print(supplier_instance,"instance")
    supplier_instance.delete()

    return render(request, 'display_supplier.html')
    


def edit_customer(request):
    if request.method == 'GET':
        name = request.GET.get('customer_name')
        print(name,"name")
        customer_instance = get_object_or_404(customer_profile, customer_name = name)
        
        form = CustomerForm(instance = customer_instance)
        
    if request.method == 'POST':
        
        name = request.POST.get('customer_name')
        print("names,",name)
        customer_instance = get_object_or_404(customer_profile, customer_name = name)
        print('instance',customer_instance)
        form = CustomerForm(request.POST, instance=customer_instance)

        if form.errors:
            print(form.errors,"err")
        if form.is_valid():
            print("valid")
            form.save()

            return (render(request,"edit_customer.html"))
    
    context = {
                
                'my_customer': customer_instance,
            } 

    return render(request, 'edit_customer.html', context)     

def create_supplier(request):
    
    if request.method == 'POST':
        form = SupplierForm(request.POST)
       
        if form.is_valid():
            form.save()
            return redirect('create_supplier')
    
    else:
        
        form = SupplierForm()
    return render(request, 'create_supplier.html', {'form': form })

def display_supplier(request):
    if request.method == 'GET':
        customers = supplier_profile.objects.all()
        context = {
                    'my_supplier': customers,
                }
          
        return render(request, 'display_supplier.html', context)

def display_supplier_profile(request, supplier_name):
    if request.method == 'GET':
        # name = request.GET['supplier_name']
        
        suppliers = supplier_profile.objects.get(supplier_name= supplier_name)
         
        context = {
                        
                        'my_supplier': suppliers,
                    }
    return render(request, 'supplier_profile.html', context) 

def create_orders(request):
    if request.method == 'POST':
        form = CosmicOrderForm(request.POST)
        print(form.data)
        if form.errors:
            print(form.errors) 

        if form.is_valid():
            print(form.data,"val")
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
            form.save()
            return redirect('create_orders')  # Redirect to the list of purchases or any other desired view
        else:
            print(form.data,"nval")
           # print(form_errors,"ers")
            errors = dict(form.errors.items())
            print(errors,"errors")
            return JsonResponse({'form_errors': errors}, status=400)
        
    form = CosmicOrderForm()
    formset = formset_factory(OrderItemForm, extra=1)
    formset = formset(prefix="items")

    # Render the form with the supplier choices
    customers = customer_profile.objects.all()
    suppliers = supplier_profile.objects.all()

    return render(request, 'create_order.html', {'form': form, 'formset': formset, 'customers': customers,'suppliers':suppliers})

 
def display_order(request):
    if request.method == 'GET':
        orders = cosmic_order.objects.all()
        orders = orders.order_by('order_no')

        orders_data = []
        for order in orders:
            # Fetch all order items related to each cosmic order
            order_items = order_item.objects.filter(order_no=order.order_no)

            # Create a dictionary containing order details and items
            order_data = {
                'order_no': order.order_no,
                'date': order.date,  # Assuming 'date' is a field in CosmicOrder
                'order_items': order_items,  # Assuming a related name 'order_items' on CosmicOrder pointing to OrderItem
                'PR_before_vat': order.PR_before_vat,  # Assuming 'PR_before_vat' is a field in CosmicOrder
                'total_quantity': order.total_quantity,  # Assuming 'total_quantity' is a field in CosmicOrder
                'customer_name': order.customer_name,  # Assuming 'customer_name' is a field in CosmicOrder
                'status': order.status,  # Assuming 'status' is a field in CosmicOrder
            }
            orders_data.append(order_data)

    context = {
        'my_order': orders_data,
    }
    return render(request, 'display_order.html', context)

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

def create_order_items(request):
    
    if request.method == 'POST':
        formset = formset_factory(OrderItemForm, extra=1, min_num=1)
        
        formset = formset(request.POST or None,prefix="items")
        #print(formset.data,"r")
      
        if formset.errors:
            print(formset.errors)   
        
        # Check if 'PR_no' field is empty in each form within the formset
        for form in formset:
            print(form,"form")
        non_empty_forms = [form for form in formset if form.cleaned_data.get('item_name')]
        pr_no = request.POST.get('order_no')
        if non_empty_forms:
            if formset.is_valid():
                final_quantity = 0.0
                final_price = 0.00
                pr = cosmic_order.objects.get(order_no=pr_no)
                for form in non_empty_forms:
                    form.instance.remaining = form.cleaned_data['quantity']
                    form.instance.order_no = pr
                    items = form.cleaned_data['item_name']
                    item = item_codes.objects.all()
                    item = item.filter(item_name = items).first()
                    code = item.hs_code
                    form.instance.hs_code = code
                    final_quantity += form.cleaned_data['quantity']
                    final_price += float(form.cleaned_data['before_vat'])
                    
                    form.save()
                
                pr.PR_before_vat = final_price
                pr.total_quantity = final_quantity
                pr.remaining = final_quantity
                pr.save()
                #message.success("successful!")
            else:
                print(formset.data,"nval")
                errors = dict(formset.errors.items())
                return JsonResponse({'form_errors': errors}, status=400)
        
            pr_form = CosmicOrderForm(prefix="orders")
            formset = formset_factory(OrderItemForm, extra=1)
            formset = formset(prefix="items")

            context = {
                'pr_form': pr_form,
                'formset': formset,
                # 'message':success_message,
            }
            return render(request, 'create_order.html', context)
    else:
        formset = formset_factory(OrderItemForm, extra=1)
        formset = formset(prefix="items")

    context = {
        'formset': formset,
    }
    return render(request, 'create_order.html', context)

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

def display_single_order(request, order_no):
    if request.method == 'GET':
        # pr_no = request.GET['order_no']

        # print(pr_no,"nada")
            
        orders = cosmic_order.objects.get(order_no=order_no)
        pr_items = order_item.objects.all()
        pr_items = pr_items.filter(order_no=order_no)
        print(pr_items)
       
            
        try:
            
            invoices = shipping_info.objects.all()
            invoices = invoices.filter(order_no = order_no)
        except shipping_info.DoesNotExist:
            try:
                print("trial")
                invoices = shipping_info.objects.all()
                invoices = invoices.filter(order_no = order_no)
            except shipping_info.DoesNotExist:
                invoices = None
            invoices = None
        print(orders)
        print("no")
        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                        'the_invoices':invoices,
                    }
            return render(request, 'display_single_order.html', context)
        context = {
                        
                        'my_order': orders,
                        'the_invoices':invoices
                    }
    return render(request, 'display_single_order.html', context)

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

@login_required 
@user_passes_test(is_admin)
def order_approval(request):
    # Your custom logic here (e.g., fetching data)
    if not is_admin(request.user):
        # User is not authenticated to access this view
        messages.error(request, "You are not authorized to access this page.")
        return redirect('admin')

    pending_orders = cosmic_order.objects.filter(status='Pending')
    pending_orders = pending_orders.order_by('order_no')
    # Handle form submission
    
    if request.method == 'POST':
        form = approvalForm(request.POST)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            action = form.cleaned_data['action']
            approval_name = form.cleaned_data['approval']
            
            if action == 'approve':
                for pr_no in form.cleaned_data['selected_orders']:
                    stats = request.POST.get(f"{pr_no}_status")
                    purchase_order = cosmic_order.objects.get(order_no=pr_no.order_no)
                    purchase_order.status = 'approved'
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
            elif action == 'reject':
                for pr_no in form.cleaned_data['selected_orders']:
                    purchase_order = cosmic_order.objects.get(order_no=pr_no.order_no)
                    purchase_order.status = 'rejected'
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
            return redirect('order_approval')

    else:
        form = approvalForm()

    context = {
        'pending_orders': pending_orders,
        'form': form,
    }
    return render(request, 'order_approval.html', context)

@login_required 
@user_passes_test(is_admin)
def purchase_approval(request):
    # Your custom logic here (e.g., fetching data)
    if not is_admin(request.user):
        # User is not authenticated to access this view
        messages.error(request, "You are not authorized to access this page.")
        return redirect('admin')

    pending_orders = cosmic_purchase.objects.filter(status='Pending').order_by('purchase_no')
    # Handle form submission
    
    if request.method == 'POST':
        form = PurchaseApprovalForm(request.POST)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            action = form.cleaned_data['action']
            approval_name = form.cleaned_data['approval']
            
            if action == 'approve':
                for pr_no in form.cleaned_data['selected_orders']:
                    stats = request.POST.get(f"{pr_no}_status")
                    purchase_order = cosmic_purchase.objects.get(purchase_no=pr_no.purchase_no)
                    purchase_order.status = 'approved'
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
            elif action == 'reject':
                for pr_no in form.cleaned_data['selected_orders']:
                    purchase_order = cosmic_purchase.objects.get(purchase_no=pr_no.purchase_no)
                    purchase_order.status = 'rejected'
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
            return redirect('purchase_approval')

    else:
        form = PurchaseApprovalForm()

    context = {
        'pending_orders': pending_orders,
        'form': form,
    }
    return render(request, 'purchase_approval.html', context)

@login_required 
@user_passes_test(is_admin)
def order_status(request):
    # Your custom logic here (e.g., fetching data)
    if not is_admin(request.user):
        # User is not authenticated to access this view
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')

    pending_orders = cosmic_order.objects.exclude(status='complete').order_by('order_no')
    # Handle form submission
    
    if request.method == 'POST':
        form = approvalForm(request.POST)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            action = form.cleaned_data['action']
            approval_name = form.cleaned_data['approval']
            
            if action == 'approve':
                for pr_no in form.cleaned_data['selected_orders']:
                    pr_no = pr_no.order_no
                    stats = request.POST.get(f"{pr_no}_status")
                    remarks = request.POST.get(f"{pr_no}_status_remark")
                    purchase_order = cosmic_order.objects.get(order_no=pr_no)
                    
                    purchase_order.status = stats
                    purchase_order.status_remark = remarks
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
            if action == 'complete':
                for pr_no in form.cleaned_data['selected_orders']:
                    pr_no = pr_no.order_no
                    purchase_order = cosmic_order.objects.get(order_no=pr_no)
                    
                    purchase_order.status = "complete"
                    purchase_order.save()
            return redirect('order_status')

    else:
        form = approvalForm()

    context = {
        'pending_orders': pending_orders,
        'form': form,
    }

   
    return render(request, 'admin/order_status.html', context)

@login_required 
@user_passes_test(is_admin)
def completed_orders(request):
    # Your custom logic here (e.g., fetching data)
    if not is_admin(request.user):
        # User is not authenticated to access this view
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')

    pending_orders = cosmic_order.objects.filter(status='complete').order_by('order_no')
    # Handle form submission
    
    if request.method == 'POST':
        form = approvalForm(request.POST)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            action = form.cleaned_data['action']
            approval_name = form.cleaned_data['approval']
            
            if action == 'approve':
                for pr_no in form.cleaned_data['selected_orders']:
                    pr_no = pr_no.order_no
                    stats = request.POST.get(f"{pr_no}_status")
                    remarks = request.POST.get(f"{pr_no}_status_remark")
                    purchase_order = cosmic_order.objects.get(order_no=pr_no)
                    
                    purchase_order.status = stats
                    purchase_order.status_remark = remarks
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
            if action == 'complete':
                for pr_no in form.cleaned_data['selected_orders']:
                    pr_no = pr_no.order_no
                    purchase_order = cosmic_order.objects.get(order_no=pr_no)
                    
                    purchase_order.status = "complete"
                    purchase_order.save()
            return redirect('completed_orders')

    else:
        form = approvalForm()

    context = {
        'pending_orders': pending_orders,
        'form': form,
    }

   
    return render(request, 'admin/completed_orders.html', context)

@login_required 
@user_passes_test(is_admin)
def purchase_status(request):
    # Your custom logic here (e.g., fetching data)
    if not is_admin(request.user):
        # User is not authenticated to access this view
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')

    pending_orders = cosmic_purchase.objects.all().order_by('purchase_no')
    # Handle form submission
    
    if request.method == 'POST':
        form = PurchaseApprovalForm(request.POST)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            action = form.cleaned_data['action']
            approval_name = form.cleaned_data['approval']
            
            if action == 'approve':
                for pr_no in form.cleaned_data['selected_orders']:
                    pr_no = pr_no.purchase_no
                    stats = request.POST.get(f"{pr_no}_status")
                    purchase_order = cosmic_purchase.objects.get(purchase_no=pr_no)
                    purchase_order.status = stats
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
          
            return redirect('purchase_status')

    else:
        form = PurchaseApprovalForm()

    context = {
        'pending_orders': pending_orders,
        'form': form,
    }

   
    return render(request, 'admin/purchase_status.html', context)

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
def edit_order_only(request):

    if request.method == 'GET':
        print("in")
        order_no = request.GET.get('order_no')
        print(order_no)
        try:
            cosmic_order_instance = cosmic_order.objects.get(order_no = order_no)
            items = order_item.objects.all()
            item = items.filter(order_no=cosmic_order_instance)
            item_names = []
            for name in item:
                item_names.append(name.item_name)
            print("l")

        except cosmic_order.DoesNotExist:
            print("h")
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                cosmic_order_instance = cosmic_order.objects.get(order_no = order_no)
                print(cosmic_order_instance,"inst")
                items = order_item.objects.all()
                item = items.filter(order_no=cosmic_order_instance)
                item_names = []
                for name in item:
                    item_names.append(name.item_name)

            except cosmic_order.DoesNotExist:
                order = None
            order = None 


        form = EditOrderForm(instance=cosmic_order_instance)  # Initialize the form with the instance data


        customers = customer_profile.objects.all()


    if request.method == 'POST':
        form = CosmicOrderForm(request.POST)
        order_no = request.POST.get('order_no')
        try:
            cosmic_order_instance = cosmic_order.objects.get(order_no = order_no)

        except cosmic_order.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                cosmic_order_instance = cosmic_order.objects.get(order_no = order_no)

            except cosmic_order.DoesNotExist:
                order = None
            order = None 

        refs_no = request.POST.get('ref_no')
        cosmic_order_instance.ref_no = refs_no
        cosmic_order_instance.measurement_type = request.POST.get('measurement_type')
        cosmic_order_instance.shipment_type = request.POST.get('shipment_type')
        cosmic_order_instance.freight = request.POST.get('freight')
        cosmic_order_instance.payment_type = request.POST.get('payment_type')
        cosmic_order_instance.transportation = request.POST.get('transportation')
        cosmic_order_instance.country_of_origin = request.POST.get('country_of_origin')
        cosmic_order_instance.final_destination = request.POST.get('final_destination')
        cosmic_order_instance.port_of_discharge = request.POST.get('port_of_discharge')
        cosmic_order_instance.port_of_loading = request.POST.get('port_of_loading')
        consignees = request.POST.get('consignee')
        notify_partys = request.POST.get('notify_party')
        notify_party2s = request.POST.get('notify_party2')


        try:

            consignee = customer_profile.objects.get(customer_name=consignees)
            cosmic_order_instance.consignee = consignee
        except customer_profile.DoesNotExist:
            cosmic_order_instance.notify_party  = None

        try:

            notify_party = customer_profile.objects.get(customer_name=notify_partys)
            cosmic_order_instance.notify_party = notify_party
        except customer_profile.DoesNotExist:
            cosmic_order_instance.notify_party  = None

        try:

            notify_party2 = customer_profile.objects.get(customer_name=notify_party2s)
            cosmic_order_instance.notify_party2 = notify_party2
        except customer_profile.DoesNotExist:
            cosmic_order_instance.notify_party2  = None


        cosmic_order_instance.save()

        my_customers = request.POST.get('customer_name')
        suppliers = request.POST.get('supplier_name')
        customer = customer_profile.objects.get(customer_name=my_customers)
        cosmic_order_instance.customer_name = customer
        supplier = supplier_profile.objects.get(supplier_name=suppliers)
        cosmic_order_instance.supplier_name = supplier
        print(cosmic_order_instance.__dict__) 
        cosmic_order_instance.save()
        return render(request, 'edit_order_only.html')  # Redirect to a success page or another URL

        print(cosmic_order_instance.order_no,"d")

    return render(request, 'edit_order_only.html', {'form': form,'cosmic_order_instance': cosmic_order_instance, 
                                               'customers': customers})


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

def print_order(request):
    if request.method == 'GET':
        
        if 'order_no' in request.GET:
            pr_no = request.GET['order_no']
        elif 'purchase_no' in request.GET:
            pr_no = request.GET['purchase_no']
        print(pr_no)
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
            proforma_type = "order"
            
        except cosmic_order.DoesNotExist:
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
                proforma_type = "purchase"
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
                        'type': proforma_type,
                        # 'shipping':shipping,
                    }
            return render(request, 'print_order.html', context)
       
        context = {
                        
                        'my_order': orders,
                        'num': num,
                        'number':number,
                        'type': proforma_type,
                        # 'shipping':shipping,
                    }
       
    return render(request, 'print_order.html', context)

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

@login_required 
@user_passes_test(is_admin)
def rejected_orders(request):
    # Your custom logic here (e.g., fetching data)
    if not is_admin(request.user):
        # User is not authenticated to access this view
        messages.error(request, "You are not authorized to access this page.")
        return redirect('login')

    pending_orders = cosmic_order.objects.filter(status='rejected')
    # Handle form submission
    
    if request.method == 'POST':
        form = restoreForm(request.POST)
        if form.errors:
            print(form.errors)
        if form.is_valid():
            action = form.cleaned_data['action']
            approval_name = form.cleaned_data['approval']
            
            if action == 'restore':
                for pr_no in form.cleaned_data['selected_orders']:
                    stats = request.POST.get(f"{pr_no}_status")
                    purchase_order = cosmic_order.objects.get(order_no=pr_no.order_no)
                    purchase_order.status = 'Pending'
                    purchase_order.approved_by = approval_name
                    purchase_order.save()
            elif action == 'delete':
                for pr_no in form.cleaned_data['selected_orders']:
                    purchase_order = cosmic_order.objects.get(order_no=pr_no.order_no)
                    purchase_order.delete()
            return redirect('rejected_orders')

    else:
        form = restoreForm()

    context = {
        'pending_orders': pending_orders,
        'form': form,
    }

   
    return render(request, 'admin/rejected_orders.html', context)

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

def display_items(request):
    if request.method == 'POST':
        form = CosmicItemForm(request.POST)

        if form.errors:
            print(form.errors)

        if form.is_valid():
            form.save()
            return redirect('display_items')
    
    form = CosmicItemForm()
    items = item_codes.objects.all()
    print(items)
    context = {
        'items':items,
        'form':form,
    }

    return render(request,'items_display.html',context)

def index_home(request):
    return render(request,'index_home.html')

def sales_contract(request):
    return render(request,'sales_contract.html')

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


def update_order(request):
     
    if request.method == "POST":
        print(request.POST)
        order_no = request.POST.get('order_no')
        cosmic_order_instance = get_object_or_404(cosmic_order, order_no=order_no)
        order_item_formset = modelformset_factory(order_item, form=OrderItemForm, extra=0)
     
        formset = order_item_formset(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            if instances:
                final_price = 0
            else:
                final_price = cosmic_order_instance.PR_before_vat
            for instance in instances:
                final_price += instance.before_vat
                
                print("Field names:", instance.__dict__.keys())
                instance.order_no = cosmic_order_instance
                print(final_price,"price")
                instance.save()
            cosmic_order_instance.PR_before_vat = final_price
            cosmic_order_instance.save()
            # Redirect to another page after saving all instances
            return render(request, "create_order.html")
    else:
        order_no = request.GET.get('order_no')
        cosmic_order_instance = get_object_or_404(cosmic_order, order_no=order_no)

        order_item_formset = modelformset_factory(order_item, form=OrderItemForm, extra=0)
        queryset = order_item.objects.filter(order_no=cosmic_order_instance)
        formset = order_item_formset(queryset=queryset)
    
    for form in formset.forms:
        if form.errors:
            print(form.errors)
    
    context = {
        "formset": formset,
        'cosmic_order_instance': cosmic_order_instance, 
    }
    return render(request, "order_update.html", context)



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
            instances = formset.save(commit=False)
            final_price = 0
            for instance in instances:
                final_price += instance.before_vat
                
                print("Field names:", instance.__dict__.keys())
                instance.invoice_num = shipping_instance
                print(final_price,"price")
                print(instance,"instance")
                instance.save()
            shipping_instance.final_price = final_price
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

def get_item_data(request, item_id):
    print(item_id,"item")
    try:
        item = item_codes.objects.get(item_name=item_id)
        data = {'code': item.hs_code} 
        print(data,"code") # Assuming 'description' field exists
        return JsonResponse(data)
    except item_codes.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    
def create_grn(request):
    if request.method == 'POST':
        form = CosmicGRNForm(request.POST)
        if form.errors:
            print(form.errors)

        if form.is_valid():
            form.save()
                    
            return redirect('create_grn')
        else:
            errors = dict(form.errors.items())
            print(errors, "errors")
            return JsonResponse({'form_errors': errors}, status = 400)
    form = CosmicGRNForm(request.POST)
    formset = formset_factory(CosmicGRNItemForm, extra=1)
    formset = formset(request.POST or None,prefix="items")

    context={
        'form':form,
        'formset':formset,
    }
    return render(request, 'create_grn.html',context)

def create_grn_items(request):
    if request.method == 'POST':
        formset = formset_factory(CosmicGRNItemForm, extra=1, min_num=1)
        formset = formset(request.POST or None,prefix="items")
             
        if formset.errors:
            print(formset.errors)   
        
        # Check if 'PR_no' field is empty in each form within the formset
        for form in formset:
            print(form,"form")

        non_empty_forms = [form for form in formset if form.cleaned_data.get('item_name')]
        grn_no = request.POST.get('GRN_no')
        if non_empty_forms:
            if formset.is_valid():
                final_quantity = 0.0
                # grns = grn.objects.get(GRN_no = grn_no)
                grns = get_object_or_404(cosmic_grn, GRN_no=grn_no)
                for form in non_empty_forms:
                    form.instance.remaining = form.cleaned_data['quantity']
                    form.instance.GRN_no = grns
                    items = form.cleaned_data['item_name']
                    final_quantity += form.cleaned_data['quantity']
                    
                    form.save()
                
                
                grns.total_quantity = final_quantity
                grns.save()
                #message.success("successful!")
            else:
                print(formset.data,"nval")
                errors = dict(formset.errors.items())
                return JsonResponse({'form_errors': errors}, status=400)
        
            grn_form = CosmicGRNItemForm(prefix="orders")
            formset = formset_factory(cosmic_grnitem, extra=1)
            formset = formset(prefix="items")

            context = {
                'grn_form': grn_form,
                'formset': formset,
                # 'message':success_message,
            }
            return render(request, 'create_grn.html', context)
    else:
       
        formset = formset_factory(CosmicGRNItemForm, extra=1)
        formset = formset(prefix="items")

    context = {
        'formset': formset,
    }
    return render(request, 'create_grn.html', context)

def display_grn(request):
     if request.method == 'GET':
        grns = cosmic_grn.objects.all()
        grns = grns.order_by('GRN_no')

        grns_data = []
        for grn in grns:
            # Fetch all order items related to each cosmic order
            grns_items = cosmic_grnitem.objects.filter(GRN_no=cosmic_grn.GRN_no)

            # Create a dictionary containing order details and items
            grn_data = {
                'GRN_no': grn.GRN_no,
                'date': grn.grn_date,  # Assuming 'date' is a field in CosmicOrder
                'grns_items': grns_items,  # Assuming a related name 'order_items' on CosmicOrder pointing to OrderItem
                'total_quantity': grn.total_quantity,  # Assuming 'total_quantity' is a field in CosmicOrder
                'store_no': grn.store_name,  # Assuming 'customer_name' is a field in CosmicOrder
                'plate_no': grn.truck_no,  # Assuming 'status' is a field in CosmicOrder
            }
            grns_data.append(grn_data)

        context = {
            'my_grn': grns_data,
        }
        return render(request, 'display_grn.html',context)

def create_dn(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            # delivery = form
            # delivery_quantity = form.cleaned_data['delivery_quantity']
            # delivery_number = form.cleaned_data['delivery_number']
            form.save()
            
            return redirect('create_dn')
        if form.errors:
            print(form.errors)
    else:
        form = DeliveryForm()
    return render(request, 'create_dn.html')

def display_dn(request):
    return render(request, 'display_dn.html')

