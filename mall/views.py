from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from .models import Cart, Category, Order, Product, SubCategory
from accounts.models import Address
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from PayTm import Checksum
from django.conf import settings

# register = template.Library()

# Create your views here.
category = Category.objects.all()
subcategory = SubCategory.objects.all()
# cats = '{ "data":[] }'
# for i in category:
#     subcat = SubCategory.objects.filter(subcat_cat=i)
#     cat_data = json.loads(cats)
#     cat_data["data"].append({"cat":i, "subcat":[subcat]})
#     json.dumps(cat_data, cats)
# print(cats)




def index(request):
    try:
        allProd = []
        subcats = SubCategory.objects.values('id')
        for i in subcats:
            products = Product.objects.filter(product_subcat=i['id'], product_quantity__range=[1,100000000])
            if products:
                allProd.append(products)
        params = {'allProds':allProd, 'category':category, 'subcategory':subcategory}
    except Exception as e:
        print(e)
    return render(request, 'index.html', params)


def about(request):
    pass

def contact(request):
    pass

def search(request):
    pass

def productView(request, product_slug):
    p = Product.objects.filter(product_slug=product_slug)
    inCart = False
    for i in p:
        off = (i.product_mrp - i.product_price)/i.product_mrp
        off = int(off*100)
    
    if request.user.id:
        if Cart.objects.filter(cart_product=p[0].id, cart_user=request.user):
            inCart = True
    prod = {"prod":p,"off":off, "incart":inCart}
    return render(request, 'productView.html', prod)

def order_details(request):
    if request.GET.get('order_id'):
        order_id = request.GET['order_id']

        orders = Order.objects.filter(order_id=order_id)
        order_item = ""
        if request.GET.get('item_id'):
            item_id = request.GET['item_id']
            order_item = orders.filter(id=item_id)[0]
    
    params = {'orders':orders, 'item':order_item}
    return render(request, 'order_details.html', params)

@login_required
def cart(request):
    if request.method=='POST' and request.is_ajax():
        if request.POST['name']=='addToCart':
            prod = request.POST["product_id"]
            quantity = request.POST["quantity"]
            user_id = request.user

            Cart.objects.create(cart_product=Product.objects.get(id=prod), cart_user=user_id, cart_product_quantity=quantity)

            return JsonResponse({"success":True }, status=200)

        elif request.POST['name']=='removeProd':
            prod = request.POST["product_id"]
            user_id = request.user
            Cart.objects.filter(cart_product=prod, cart_user=user_id).delete()
            return JsonResponse({"success":True }, status=200)
        
        elif request.POST['name']=='updateCart':
            prod = request.POST["product_id"]
            quantity = request.POST["quantity"]
            user_id = request.user
            Cart.objects.filter(cart_product=prod, cart_user=user_id).update(cart_product_quantity=quantity)
            return JsonResponse({"success":True }, status=200)
        
        return JsonResponse({"success":False }, status=400)
        

    carts = Cart.objects.filter(cart_user=request.user.id)
    prods = {"prod":carts}
    return render(request, 'cart.html', prods)


@login_required
def checkout(request):
    if request.method=='POST':
        address = Address.objects.filter(id=request.POST['address'])[0]

        if "cart" in request.POST:
            prod = Cart.objects.filter(cart_user=request.user)
            try:
                totalPrice = 0
                order_id = "OD"+str(randint(10000000,99999999))
                for i in prod:
                    totalPrice += int(i.cart_product.product_price)
                    order = Order(
                        order_id = order_id,
                        order_user = request.user,
                        order_products=i.cart_product, 
                        user_name = address.full_name, 
                        mobile=address.mobile, 
                        amount = i.cart_product.product_price,
                        address = address.address,
                        city = address.city,
                        state = address.state,
                        pincode = address.pincode,
                        prod_quantity = i.cart_product_quantity,
                        orderTime = timezone.now()
                    )
                    order.save()
                    p = Product.objects.filter(id=i.cart_product.id)
                    p.update(product_quantity=int(p[0].product_quantity)-int(i.cart_product_quantity))
                
                Cart.objects.filter(cart_user=request.user).delete()
                # return HttpResponse("Thank you for Shopping. Your OrderId is: "+order_id+".")
            except Exception as e:
                print(e)

        elif "direct" in request.POST:
            prod = Product.objects.filter(id=request.POST['buyProduct'])[0]
            totalPrice = int(prod.product_price) * int(request.POST['quantity'])
            order_id = "OD"+str(randint(10000000,99999999))
            order = Order(
                order_id = order_id,
                order_user = request.user,
                order_products=prod, 
                user_name = address.full_name, 
                mobile=address.mobile, 
                amount = prod.product_price,
                address = address.address,
                city = address.city,
                state = address.state,
                pincode = address.pincode,
                prod_quantity = request.POST['quantity'],
                orderTime = timezone.now()
            )
            order.save()
            p = Product.objects.filter(id=prod.id)
            p.update(product_quantity=int(p[0].product_quantity)-int(request.POST['quantity']))
        
        param_dict={
            'MID': settings.MERCHANT_ID,
            'ORDER_ID': order_id,
            'TXN_AMOUNT': str(totalPrice),
            'CUST_ID': request.user.email,
            'INDUSTRY_TYPE_ID': settings.PAYTM_INDUSTRY_TYPE_ID,
            'WEBSITE': settings.PAYTM_WEBSITE,
            'CHANNEL_ID': settings.PAYTM_CHANNEL_ID,
            'CALLBACK_URL':'http://127.0.0.1:8000/handlepayment/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, settings.MERCHANT_KEY)
        return render(request, "paytm.html", {"param_dict":param_dict})
        

    address = Address.objects.filter(address_user=request.user.id)
    if request.GET['ref']=='cart':
        carts = Cart.objects.filter(cart_user=request.user.id)
        if carts:
            prods = {"prod":carts, "address":address, "ref":"cart"}
            return render(request, 'checkout.html', prods)
    elif request.GET['ref']:
        prod = Product.objects.filter(product_slug=request.GET['ref'])
        if prod:
            prods = {"prod":prod, "address":address, "ref":"direct"}
            return render(request, 'checkout.html', prods)
    return redirect("/")

def product_list_category(request, slug):
    p = Product.objects.filter(product_cat=Category.objects.get(cat_slug=slug), product_quantity__range=[1,100000000])
    max_price = p.order_by("-product_price")[0].product_price
    if request.GET.get('sort-by')!=None:
        if request.GET["sort-by"]=="price-low-to-high":
            p = p.order_by('product_price')
        elif request.GET["sort-by"]=="price-high-to-low":
            p = p.order_by('-product_price')
        elif request.GET["sort-by"]=="newest-first":
            p = p.order_by("product_pub_time")
    
    if request.GET.get('min')!=None or request.GET.get('max')!=None:
        p = p.filter(product_price__range=[int(request.GET.get('min')), int(request.GET.get('max'))])
    
    subcats_in_this_cat = SubCategory.objects.filter(subcat_cat=Category.objects.get(cat_slug=slug))
    
    params = {
        "prod":p,
        'category':category, 
        'subcategory':subcategory, 
        'max_price':max_price, 
        'cat_page':True, 
        'subcats_in_this_cat':subcats_in_this_cat
    }
    return render(request, "product_list_subcategory.html", params)


def product_list_subcategory(request, slug1, slug2):
    p = Product.objects.filter(product_subcat=SubCategory.objects.get(subcat_slug=slug2), product_quantity__range=[1,100000000])
    max_price = p.order_by("-product_price")[0].product_price
    if request.GET.get('sort-by')!=None:
        if request.GET["sort-by"]=="price-low-to-high":
            p = p.order_by('product_price')
        elif request.GET["sort-by"]=="price-high-to-low":
            p = p.order_by('-product_price')
        elif request.GET["sort-by"]=="newest-first":
            p = p.order_by("product_pub_time")
    
    if request.GET.get('min')!=None or request.GET.get('max')!=None:
        p = p.filter(product_price__range=[int(request.GET.get('min')), int(request.GET.get('max'))])
        
    params = {
        "prod":p,
        'category':category, 
        'subcategory':subcategory, 
        'max_price':max_price,  
        'cat_page':False
    }
    
    return render(request, "product_list_subcategory.html", params)


def get_subcategory(request):
    id = request.GET.get('id',"")
    result = list(SubCategory.objects.filter(subcat_cat=int(id)).values('id', 'subcat_name'))
    return HttpResponse(json.dumps(result), content_type="application/json")

@csrf_exempt
def handlepayment(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]
    
    verify = Checksum.verify_checksum(response_dict, settings.MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            for i in Order.objects.filter(order_id=response_dict["ORDERID"]):
                Order.objects.filter(id=i.id).update(order_status="Payment Success")
        else:
            # print(response_dict)
            # print("Order Failed"+response_dict["RESPMSG"])
            for i in Order.objects.filter(order_id=response_dict["ORDERID"]):
                Order.objects.filter(id=i.id).update(order_status="Payment Failed")
                p = Product.objects.filter(id=i.order_products.id)
                p.update(product_quantity=p[0].product_quantity + int(i.prod_quantity))
        
    return redirect("/accounts/orders/")