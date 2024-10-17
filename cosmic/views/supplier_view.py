from ..forms import *
from ..models import *
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

def delete_supplier_profile(request):

    name = request.GET['supplier_name']
    print("names,",name)
    supplier_instance = get_object_or_404(supplier_profile, supplier_name = name)
    print(supplier_instance,"instance")
    supplier_instance.delete()

    return render(request, 'display_supplier.html')

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
              
        suppliers = supplier_profile.objects.get(supplier_name= supplier_name)
         
        context = {            
                        'my_supplier': suppliers,
                  }
    return render(request, 'supplier_profile.html', context) 