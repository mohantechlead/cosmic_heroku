from ..forms import *
from ..models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory,modelformset_factory
from django.http import JsonResponse, HttpResponseRedirect

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

def update_order(request):     
    if request.method == "POST":
        print(request.POST)
        order_no = request.POST.get('order_no')
        cosmic_order_instance = get_object_or_404(cosmic_order, order_no=order_no)
        OrderItemFormSet = modelformset_factory(order_item, form=OrderItemForm, extra=0)

    if request.method == "POST":
        formset = OrderItemFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            
            # Calculate the total price from the submitted form data
            final_price = 0
            for form in formset:
                before_vat = form.cleaned_data.get('before_vat', 0)  # Get the 'before_vat' value from the form
                if before_vat is not None:
                    final_price += before_vat  # Add to final price

            # Process each instance and assign it to the correct order
            for instance in instances:
                instance.order_no = cosmic_order_instance
                instance.save()

            # Update the cosmic_order instance with the final price calculated from the form input
            cosmic_order_instance.PR_before_vat = final_price
            cosmic_order_instance.save()

            # Redirect after saving
            return HttpResponseRedirect(f'?order_no={order_no}')
    else:
        order_no = request.GET.get('order_no')
        cosmic_order_instance = get_object_or_404(cosmic_order, order_no=order_no)

        order_item_formset = modelformset_factory(order_item, form=OrderItemForm, extra=0)
        queryset = order_item.objects.filter(order_no=cosmic_order_instance)
        formset = order_item_formset(queryset=queryset)
    
    for form in formset.forms:
        if form.errors:
            print(form.errors)
    mycustomer = customer_profile.objects.all()
    mysupplier = supplier_profile.objects.all()
    context = {
        "formset": formset,
        'cosmic_order_instance': cosmic_order_instance, 
        'customers': mycustomer,
        'suppliers': mysupplier,
    }
    return render(request, "order_update.html", context)

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
            }
            return render(request, 'create_order.html', context)
    else:
        formset = formset_factory(OrderItemForm, extra=1)
        formset = formset(prefix="items")

    context = {
        'formset': formset,
    }
    return render(request, 'create_order.html', context)


def display_single_order(request, order_no):
    if request.method == 'GET':
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