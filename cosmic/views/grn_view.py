from ..forms import *
from ..models import *
from django.shortcuts import render, redirect,get_object_or_404
from django.forms import formset_factory
from django.http import JsonResponse

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
