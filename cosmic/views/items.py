from ..forms import *
from ..models import *
from django.http import JsonResponse
from django.shortcuts import render, redirect

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

def get_item_data(request, item_id):
    print(item_id,"item")
    try:
        item = item_codes.objects.get(item_name=item_id)
        data = {'code': item.hs_code} 
        print(data,"code") 
        return JsonResponse(data)
    except item_codes.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)
    