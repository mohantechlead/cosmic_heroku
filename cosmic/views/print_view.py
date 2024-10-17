from django.shortcuts import render
from ..forms import *
from ..models import *
from num2words import num2words

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

def print_purchase(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
            
        except cosmic_order.DoesNotExist:
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
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
                        # 'shipping':shipping,
                    }
            return render(request, 'print_purchase.html', context)
       
        context = {
                        
                        'my_order': orders,
                        'num': num,
                        'number':number,
                        # 'shipping':shipping,
                    }
       
    return render(request, 'print_purchase.html', context)

def commercial_invoice(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        inv_no = request.GET['invoice_num']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
        except cosmic_order.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                shipping = shipping_info.objects.get(order_no = pr_no)
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
                print(pr_items)
            except cosmic_purchase.DoesNotExist:
                order = None
                # Handle the case where the object doesn't exist in either table.
            order = None 
        try:
            
            shipping = shipping_info.objects.get(order_no = pr_no, invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping = None
        
        try:
            
            shipping_items = invoice_item.objects.all()
            shipping_items = shipping_items.filter(invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping_items = None

        if hasattr(shipping, 'final_price'):
            number = shipping.final_price
            print("yes",number)
        else:
            number = shipping.final_price
            print(shipping.final_price)
        dicts = {1:"TEN",2:"TWENTY",3:"THIRTY",4:"FORTY",5:"FIFTY",6:"SIXTY",7:"SEVENTY",8:"EIGHTY",9:"NINTY"}
        if shipping:
            if orders.freight_price:
                print(number,orders.freight_price,"try")
                number += float(orders.freight_price)
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
      
        num = num.replace(' AND', '')
        num += dec 
        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'my_order': orders,
                        'shipping': shipping,
                        'num': num,
                        'number':number,
                        'shipping_items': shipping_items
                    }
            return render(request, 'commercial_invoice.html', context)
        context = {
                        
                        'my_order': orders,
                        'shipping': shipping,
                        'num': num,
                        'shipping_items': shipping_items,
                        'number':number,
                    }
    return render(request, 'commercial_invoice.html', context)

def bill_of_lading(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        inv_no = request.GET['invoice_num']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
            print(pr_items)
        except cosmic_order.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
                print(pr_items)
            except cosmic_purchase.DoesNotExist:
                order = None
                # Handle the case where the object doesn't exist in either table.
            order = None 
        try:
            
            shipping = shipping_info.objects.get(order_no = pr_no, invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping = None
        try:
            
            shipping_items = invoice_item.objects.all()
            shipping_items = shipping_items.filter(invoice_num=inv_no)
        except invoice_item.DoesNotExist:
            shipping_items = None
       
        if pr_items.exists():
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items':shipping_items,
                    }
            return render(request, 'bill_of_lading.html', context)
        context = {
                        
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items': shipping_items,
                    }
    return render(request, 'bill_of_lading.html', context)
def truck_waybill(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        inv_no = request.GET['invoice_num']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
            print(pr_items)
        except cosmic_order.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
                print(pr_items)
            except cosmic_purchase.DoesNotExist:
                order = None
                # Handle the case where the object doesn't exist in either table.
            order = None 
        try:
            
            shipping = shipping_info.objects.get(order_no = pr_no, invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping = None
        try:
            
            shipping_items = invoice_item.objects.all()
            shipping_items = shipping_items.filter(invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping_items = None

        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items': shipping_items,
                    }
            return render(request, 'truck_waybill.html', context)
        context = {
                        
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items': shipping_items,
                    }
    return render(request, 'truck_waybill.html', context)


def packing_list(request):
    if request.method == 'GET':
        pr_no = request.GET['order_no']
        inv_no = request.GET['invoice_num']
        try:
            orders = cosmic_order.objects.get(order_no=pr_no)
            pr_items = order_item.objects.all()
            pr_items = pr_items.filter(order_no=pr_no)
            print(pr_items)
        except cosmic_order.DoesNotExist:
            # If it's not found in purchase_orders, try searching in import_PR
            try:
                orders = cosmic_purchase.objects.get(purchase_no=pr_no)
                shipping = shipping_info.objects.get(order_no = pr_no)
                pr_items = purchase_item.objects.all()
                pr_items = pr_items.filter(purchase_no=pr_no)
                print(pr_items)
            except cosmic_purchase.DoesNotExist:
                order = None
            order = None 
        try:
            
            shipping = shipping_info.objects.get(order_no = pr_no, invoice_num=inv_no)
        except shipping_info.DoesNotExist:
            shipping = None
        try:
            
            shipping_items = invoice_item.objects.all()
            shipping_items = shipping_items.filter(invoice_num=inv_no)
        except invoice_item.DoesNotExist:
            shipping_items = None
        print(orders)
        print("no")
        if pr_items.exists():
            print(pr_items,"yes")
            context = {
                        'pr_items': pr_items,
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items':shipping_items,
                    }
            return render(request, 'packing_list.html', context)
        context = {
                        
                        'my_order': orders,
                        'shipping': shipping,
                        'shipping_items':shipping_items,
                    }
    return render(request, 'packing_list.html', context)

def index_home(request):
    return render(request,'index_home.html')

def sales_contract(request):
    return render(request,'sales_contract.html')