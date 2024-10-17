from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from ..forms import *
from ..models import * 

def is_admin(user):
    return user.is_superuser

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

