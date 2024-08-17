from django.shortcuts import render, redirect,get_object_or_404
from ..forms import *
from ..models import *
from django.forms import formset_factory,modelformset_factory
from django.http import JsonResponse
from num2words import num2words

def is_admin(user):
    return user.is_superuser

def index_home(request):
    return render(request,'index_home.html')

def sales_contract(request):
    return render(request,'sales_contract.html')

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
