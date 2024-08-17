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