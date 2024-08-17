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
