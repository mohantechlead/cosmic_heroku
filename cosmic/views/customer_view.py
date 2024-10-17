from ..forms import *
from ..models import *
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

def create_customer(request):
    if request.method == 'POST':
        email = request.POST['email']
        form = CustomerForm(request.POST)
        if form.errors:
            print(form.errors)
        if customer_profile.objects.filter(email = email). exists():
            messages.error(request, 'Email Already exists')
            return redirect('create_customer')
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