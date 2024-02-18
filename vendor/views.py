from django.shortcuts import render,redirect
from store.models import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Avg, Sum
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from django.http import JsonResponse


@csrf_exempt
def vendor_requirded(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

@vendor_requirded(login_url='v_login')
def dashboard(request):
    # order_list = orders.objects.all() 
    product = products.objects.filter(vendoraddedby = request.user.customer.id)
    order_list = orders.objects.filter(vendor_id = request.user.id)
    
    context={'navbar':'dashboard','products':product,'order_list':order_list}
    return render(request,'dashboard.html',context)

@vendor_requirded(login_url='v_login')
def store_details(request):
    context={'navbar':'store_details'}
    return render(request,'store_details.html',context)

@vendor_requirded(login_url='v_login')
def all_products(request):
    categories = category.objects.all()
    product = products.objects.filter(vendoraddedby = request.user.customer.id)
    get_cat_id = request.GET.get('category')
    get_rating = request.GET.get('rating')
    if get_cat_id:
        product = products.objects.filter(itmclass=get_cat_id, vendoraddedby = request.user.customer.id)

    # if get_rating:
    #     product = products.objects.annotate(average_rating=Avg('reviews__rating')).filter(average_rating__lt=get_rating)
    # else:
    #     return product
    
    if request.method == 'GET':
        search_attr = request.GET.get('search', '')
        if search_attr:
            product = products.objects.filter(itmname__icontains=search_attr,vendoraddedby = request.user.customer.id)
    page = request.GET.get('page',1)
    paginator = Paginator(product,10)
    try:
        product = paginator.page(page)
    except PageNotAnInteger:
        product = paginator.page(1)
    except EmptyPage:
        product = paginator.page(paginator.num_pages)

    context={'navbar':'products','categories':categories,'products':product,'paginator':page}
    return render(request,'products.html',context)

@vendor_requirded(login_url='v_login')
def toggle_product(request, product_id):
    product = get_object_or_404(products, id=product_id)
    product.itm_isactive = not product.itm_isactive
    product.save()
    return JsonResponse({'success': True, 'is_active': product.itm_isactive})

@vendor_requirded(login_url='v_login')
def product_add(request):
    categories = category.objects.all() 
    context={'navbar':'products','categories':categories}
    return render(request,'product_add.html',context)

@vendor_requirded(login_url='v_login')
def product_details(request,id):
    categories = category.objects.all()
    sub_categories = subcategory.objects.all()
    product = products.objects.filter(id=id)
    pro_id = product.first().id
    coupon = discount.objects.filter(if_on_product = pro_id,vendor_by = request.user).first()
    variants = product_variants.objects.filter(product_id=id)
    print(product)
    context={'navbar':'products','product':product,'categories':categories,'sub_categories':sub_categories,'variants':variants,'coupon':coupon}
    return render(request,'product_details.html',context)

@vendor_requirded(login_url='v_login')
def all_orders(request):
    order_list = orders.objects.filter(vendor_id = request.user.id)
    context={'navbar':'orders','order_list':order_list}
    return render(request,'orders.html',context)


@vendor_requirded(login_url='v_login')
def order_details(request,id):
    order_detail = get_object_or_404(orders, pk=id)
    customer_instance = order_detail.cutomer_id
    user_instance = customer_instance.user
    user_address = address.objects.filter(username=user_instance,isactive = True)
    context={'navbar':'orders','order_detail':order_detail,'user_address':user_address}
    return render(request,'order_details.html',context)





@vendor_requirded(login_url='v_login')
def customers(request):
    order_list = orders.objects.filter(vendor_id = request.user.id)
    customer_instances = []
    for order in order_list:
        customer_instance = order.cutomer_id
        customer_instances.append(customer_instance)
    context={'navbar':'customers','customer_instances':customer_instances}
    return render(request,'customers.html',context)

@vendor_requirded(login_url='v_login')
def customer_details(request,id):
    customers = customer.objects.filter(id = id)
    customer_instance = customer.objects.filter(id=id).first()
    if customer_instance:
        user_instance = customer_instance.user
        user_address = address.objects.filter(username=user_instance, isactive=True)

    all_order_customer = orders.objects.filter(cutomer_id = customer_instance,vendor_id = request.user.id)
    context={'navbar':'customers','customers':customers,'user_address':user_address,'all_order_customer':all_order_customer}
    return render(request,'customer_details.html',context)

@vendor_requirded(login_url='v_login')
def sales_promotions(request):
    cupons = discount.objects.filter(vendor_by = request.user)
    context={'navbar':'sales_promotions','cupons':cupons}
    return render(request,'sales_promotions.html',context)

@vendor_requirded(login_url='v_login')
def coupon_edit(request,id):
    coupon = discount.objects.filter(id=id)
    categories = category.objects.all() 
    context={'navbar':'sales_promotions','categories':categories,'coupon':coupon}
    return render(request,'coupon_edit.html',context)

@vendor_requirded(login_url='v_login')
def coupon_add(request):
    categories = category.objects.all() 
    context={'navbar':'sales_promotions','categories':categories}
    return render(request,'coupon_add.html',context)

@vendor_requirded(login_url='v_login')
def create_invoice(request):
    context={'navbar':'create_invoice'}
    return render(request,'invoice.html',context)

@vendor_requirded(login_url='v_login')
def all_report(request):
    context={'navbar':'all_report'}
    return render(request,'all_reports.html',context)

@vendor_requirded(login_url='v_login')
def help(request):
    context={'navbar':'help'}
    return render(request,'help.html',context)
@csrf_exempt
def v_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username = username, password=password)
        if user.is_staff == True:
            login(request,user)
            return redirect('v_dashboard')
        else: 
            return redirect('v_login')

    context={}
    return render(request,'v_login.html',context)

def vendor_logout(request):
    logout(request)
    return redirect('v_dashboard')
