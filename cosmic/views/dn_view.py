from django.shortcuts import render, redirect
from ..forms import *
from ..models import *

def create_dn(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('create_dn')
        
        if form.errors:
            print(form.errors)
    else:
        form = DeliveryForm()
    return render(request, 'create_dn.html')

def display_dn(request):
    return render(request, 'display_dn.html')

