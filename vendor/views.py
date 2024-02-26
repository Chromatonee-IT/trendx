from django.shortcuts import render,redirect,HttpResponse
from store.models import *
from .models import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Avg, Sum
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from django.http import JsonResponse
from datetime import date
from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib import messages


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
def vendor_profile(request):
    user = request.user
    address_ins = address.objects.get(isactive=True,username = user)
    cust_ins = customer.objects.get(user=user)
    store_ins = store_details.objects.get(store_vendor=user)
    if request.method=="POST":
        if 'profile_update' in request.POST:
            name= request.POST.get('name')
            birthday= request.POST.get('birthday')
            user_email= request.POST.get('user_email')
            user_phone= request.POST.get('user_phone')
            abline1= request.POST.get('adrline1')
            abline2= request.POST.get('adrline2')
            abline3= request.POST.get('adrline3')
            city= request.POST.get('city')
            district= request.POST.get('district')
            state= request.POST.get('state')
            postal= request.POST.get('postal')

            cust_ins.name = name
            cust_ins.email = user_email
            cust_ins.phone_number = user_phone
            cust_ins.birthday = birthday

            if 'profile_photo' in request.FILES:
                cust_ins.cusstomer_image = request.FILES['profile_photo']
            

            address_ins.abline1 = abline1
            address_ins.abline2 = abline2
            address_ins.abline3 = abline3
            address_ins.city = city
            address_ins.district = district
            address_ins.state = state
            address_ins.zip = postal
            cust_ins.save()
            address_ins.save()

            return redirect('store_details')
        
        if 'store_update' in request.POST:
            store_name= request.POST.get('store_name')
            store_email= request.POST.get('store_email')
            store_abline1= request.POST.get('store_abline1')
            store_abline2= request.POST.get('store_abline2')
            store_abline3= request.POST.get('store_abline3')
            city= request.POST.get('city')
            district= request.POST.get('district')
            # state= request.POST.get('state')
            zip= request.POST.get('zip')
            store_facebook= request.POST.get('store_facebook')
            store_instagram= request.POST.get('store_instagram')
            store_twitter= request.POST.get('store_twitter')

            store_ins.store_name=store_name
            store_ins.store_email=store_email
            store_ins.abline1=store_abline1
            store_ins.abline2=store_abline2
            store_ins.abline3=store_abline3
            store_ins.city=city
            store_ins.district=district
            # store_ins.state=state
            store_ins.store_facebook=store_facebook
            store_ins.store_instagram=store_instagram
            store_ins.store_twitter=store_twitter
            store_ins.zip=zip
            if 'store_logo' in request.FILES:
                store_ins.store_logo = request.FILES['store_logo']
            store_ins.save()
            messages.success(request,"Store details updated.")
            return redirect('store_details')
        if 'update_user' in request.POST:
            username= request.POST.get('username')
            password= request.POST.get('password')
            user = User.objects.filter(username=username).first()
            print(user)
            user.set_password(password)
            user.save()
            messages.success(request,"Login credentials changed.")
            return redirect('v_login')



    cur_date = date.today() 
    age = cur_date.year - cust_ins.birthday.year
    context={'navbar':'store_details','user':user,'address_ins':address_ins,'store_ins':store_ins,'age':age}
    return render(request,'vendor_profile.html',context)


@vendor_requirded(login_url='v_login')
def all_products(request):
    categories = category.objects.all()
    product = products.objects.filter(vendoraddedby = request.user.customer.id)
    get_cat_id = request.GET.get('category')
    get_rating = request.GET.get('rating')

    if get_cat_id:
        product = products.objects.filter(itmclass=get_cat_id, vendoraddedby = request.user.customer.id)

    if get_rating:
        min_rating_value = float(get_rating)

        # Annotate average rating for products
        products_queryset = product.annotate(
            get_average_rating=Avg('reviews__rating')
        )

        # Filter products based on minimum rating
        product = products_queryset.filter(
            get_average_rating__gte=min_rating_value
        )

    
    
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
def add_product_variant(request,id):
    product_ins = products.objects.get(id=id)
    variant = product_variants()
    varient_name = request.POST.get('varient_name')
    color_code = request.POST.get('color_code')
    quantity = request.POST.get('quantity')
    variant.product_id=product_ins
    variant.varient_name = varient_name
    variant.color_code = color_code
    variant.quantity = quantity
    variant.save()
    return JsonResponse({'success': True})


@vendor_requirded(login_url='v_login')
def update_product_variant(request):
    # Extract data from the POST request
    variant_id = request.POST.get('variant_id')
    varient_name = request.POST.get('varient_name')
    color_code = request.POST.get('color_code')
    quantity = request.POST.get('quantity')

    try:
        variant = product_variants.objects.get(id=variant_id)
        variant.varient_name = varient_name
        variant.color_code = color_code
        variant.quantity = quantity
        variant.save()

        # Optionally, you can return a success message or any other data
        return JsonResponse({'success': True, 'message': 'Variant updated successfully'})
    except product_variants.DoesNotExist:
        # Variant with the given ID does not exist
        return JsonResponse({'success': False, 'message': 'Variant not found'}, status=404)
    except Exception as e:
        # Handle other exceptions
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

@vendor_requirded(login_url='v_login')
def delete_variant(request,id):
    variant = get_object_or_404(product_variants,id=id)
    product_id= variant.product_id.id
    variant.delete()
    return redirect('/product_details/'+str(product_id))


@vendor_requirded(login_url='v_login')
def product_add(request):
    if request.method=='POST':
        product = products()
        product_image = product_images()
        product_name = request.POST.get('product_name')
        product_title = request.POST.get('product_title')
        product_desc = request.POST.get('product_desc')
        old_price = request.POST.get('old_price')
        new_price = request.POST.get('new_price')
        product_status = request.POST.get('product_status')
        product_category = request.POST.get('product_category')
        product_subcategory = request.POST.get('product_subcategory')
        product_sku = request.POST.get('product_sku')
        product_tag = request.POST.get('product_tag')

        if not products.objects.get(itmname=product_name,itmtitle=product_title,vendoraddedby = request.user.customer,itm_old_price=old_price,itm_new_price=new_price,sku_no=product_sku,itm_tags=product_tag):
            product.vendoraddedby = request.user.customer
            product.itmname=product_name
            product.itmtitle=product_title
            product.itmdesc=product_desc
            product.itm_old_price=old_price
            product.itm_new_price=new_price
            product.itm_isactive=product_status
            product.sku_no=product_sku
            product.itm_tags=product_tag
            if product_category:
                cat_ins = category.objects.get(id=product_category)
                product.itmclass=cat_ins
            if product_subcategory:
                subcat_ins = subcategory.objects.get(id=product_subcategory)
                product.itmsubclass=subcat_ins
            product.save()
            product = products.objects.get(itmname=product_name,itmtitle=product_title,vendoraddedby = request.user.customer)

            product_image.product_id = product
            if 'image1' in request.FILES:
                product_image.image1 = request.FILES['image1']
            if 'image2' in request.FILES:
                product_image.image2 = request.FILES['image2']
            if 'image3' in request.FILES:
                product_image.image3 = request.FILES['image3']
            if 'image4' in request.FILES:
                product_image.image4 = request.FILES['image4']
            if 'image5' in request.FILES:
                product_image.image5 = request.FILES['image5']
            product_image.save()
            return redirect('products')

        return redirect('products')

    categories = category.objects.all() 
    sub_categories = subcategory.objects.all()
    context={'navbar':'products','categories':categories,'sub_categories':sub_categories}
    return render(request,'product_add.html',context)

@vendor_requirded(login_url='v_login')
def product_details(request,id):
    if request.method=='POST':
        product = products.objects.get(id=id)
        product_image = product_images.objects.get(product_id=product)
        product_name = request.POST.get('product_name')
        product_title = request.POST.get('product_title')
        product_desc = request.POST.get('product_desc')
        old_price = request.POST.get('old_price')
        new_price = request.POST.get('new_price')
        product_coupon = request.POST.get('product_coupon')
        product_status = request.POST.get('product_status')
        product_category = request.POST.get('product_category')
        product_subcategory = request.POST.get('product_subcategory')
        product_sku = request.POST.get('product_sku')
        product_tag = request.POST.get('product_tag')
        
        if product_coupon == 'No Discount' or product_coupon == '' :
            if discount.objects.filter(vendor_by=request.user,if_on_product=product):
                discount.objects.filter(vendor_by=request.user,if_on_product=product).update(if_on_product = None)
            else:
                pass
        else:
            discount.objects.filter(offer=product_coupon,vendor_by=request.user).update(if_on_product=product)
            
        product.itmname=product_name
        product.itmtitle=product_title
        product.itmdesc=product_desc
        product.itm_old_price=old_price
        product.itm_new_price=new_price
        product.itm_isactive=product_status
        product.sku_no=product_sku
        product.itm_tags=product_tag

        if product_category:
            cat_ins = category.objects.get(id=product_category)
            product.itmclass=cat_ins
        if product_subcategory:
            subcat_ins = subcategory.objects.get(id=product_subcategory)
            product.itmsubclass=subcat_ins
        product.save()

        if 'image1' in request.FILES:
            product_image.image1 = request.FILES['image1']
        if 'image2' in request.FILES:
            product_image.image2 = request.FILES['image2']
        if 'image3' in request.FILES:
            product_image.image3 = request.FILES['image3']
        if 'image4' in request.FILES:
            product_image.image4 = request.FILES['image4']
        if 'image5' in request.FILES:
            product_image.image5 = request.FILES['image5']
        product_image.save()
        return redirect('products')
        



    categories = category.objects.all()
    sub_categories = subcategory.objects.all()
    product = products.objects.filter(id=id)
    pro_id = product.first().id
    coupon = discount.objects.filter(if_on_product = pro_id,vendor_by = request.user).first()
    variants = product_variants.objects.filter(product_id=id)
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
def coupon_edit(request, id):
    coupon = discount.objects.filter(id=id)
    categories = category.objects.all()
    
    if request.method == 'POST':
        coupon = discount.objects.get(id=id)
        coupon_status = request.POST.get('couponsstatus')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        coupon_code = request.POST.get('coupon_name')
        discount_category_id = request.POST.get('discount_category')
        coupon_type_id = request.POST.get('couponstype')
        discount_value = request.POST.get('discount_value')
        
        discount_type_ins = discount_type.objects.get(id=coupon_type_id)
        # Update the attributes of the coupon object
        coupon.offer = coupon_code
        coupon.offer_cat = discount_type_ins
        if discount_category_id:
            discount_category_ins = category.objects.get(id=discount_category_id)
            coupon.if_on_category = discount_category_ins
        else:
            coupon.if_on_category = None
        coupon.discount_value = discount_value
        coupon.is_active = coupon_status
        coupon.start_date = start_date
        coupon.end_date = end_date
        
        # Save the updated object to the database
        coupon.save()
        
        return redirect('sales_promotions')
    
    context = {'navbar': 'sales_promotions', 'categories': categories, 'coupon': coupon}
    return render(request, 'coupon_edit.html', context)

@vendor_requirded(login_url='v_login')
def coupon_add(request):
    categories = category.objects.all()
    if request.method == 'POST':
        coupon_status = request.POST.get('couponsstatus')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        coupon_code = request.POST.get('coupon_name')
        discount_category_id = request.POST.get('discount_category')
        coupon_type_id = request.POST.get('couponstype')
        discount_value = request.POST.get('discount_value')
        
        discount_type_ins = discount_type.objects.get(id=coupon_type_id)
        if discount_category_id:
            discount_category_ins = category.objects.get(id=discount_category_id)
        else:
            discount_category_ins = None
        
        discount.objects.create(vendor_by=request.user,offer=coupon_code,offer_cat=discount_type_ins,if_on_category=discount_category_ins,discount_value=discount_value,is_active=coupon_status,start_date=start_date,end_date=end_date)
        return redirect('sales_promotions')
    context={'navbar':'sales_promotions','categories':categories}
    return render(request,'coupon_add.html',context)

def coupon_delete(request,id):
    del_ind = discount.objects.get(id=id)
    del_ind.delete()
    return redirect('sales_promotions')

@vendor_requirded(login_url='v_login')
def create_invoice(request):
    context={'navbar':'create_invoice'}
    return render(request,'create_invoice.html',context)


@vendor_requirded(login_url='v_login')
def update_invoice(request,id):
    invoice_ins = order_invoices.objects.get(id=id)
    vendor_ins = User.objects.get(id=invoice_ins.order_id.vendor_id.store_vendor.id)
    context={'navbar':'create_invoice','invoice_ins':invoice_ins,'vendor_ins':vendor_ins}
    return render(request,'update_invoice.html',context)

@vendor_requirded(login_url='v_login')
def all_invoices(request):
    order_list = orders.objects.filter(vendor_id = request.user.id)
    invoice_list = []
    for order in order_list:
        invoices = order_invoices.objects.get(order_id = order)
        invoice_list.append(invoices)
    context={'navbar':'create_invoice','invoice_list':invoice_list}
    return render(request,'invoice.html',context)


def render_to_pdf(template,data={}):
    template = get_template(template)
    html = template.render(data)
    results = BytesIO()
    pdf  = pisa.pisaDocument(html.encode("UTF-8"),results)
    if not pdf.err:
        return HttpResponse(results.getvalue(),content_type="application/pdf")
    return None


def generate_invoice(request,id):
    try:
        order_detail = orders.objects.get(id=id,vendor_id=request.user.id)
    except:
        return HttpResponse('Invoice Not Found')
    data = {
        'order_id':order_detail.id,
        'name':order_detail.cutomer_id.name,
        'paymentid':order_detail.paymentid,
    }
    pdf = render_to_pdf('generate_invoice.html',data)
    return HttpResponse(pdf,content_type='application/pdf')
    # return render(request,'generate_invoice.html')


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


        user = authenticate(request,username = username, password=password)
        if user is None:
            messages.error(request,"Enter correct credintials!")
            return redirect('v_login')
        if user.is_staff == True:
            login(request,user)

            return redirect('v_dashboard')
        else:
            messages.error(request,"Enter correct credintials!")
            return redirect('v_login')

    context={}
    return render(request,'v_login.html',context)

@csrf_exempt
def v_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone']
        terms_and_conditions = request.POST.get('termsandconditions', False)
        phone_number = request.POST.get('phone', '')

        if len(phone_number) >= 10 and not phone_number.isdigit():
            messages.error(request,"Phone number must be 10 digits!")
            return redirect('v_register')
        if terms_and_conditions:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already exists!")
                return redirect('v_register')
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already exists!")
                return redirect('v_register')
            if customer.objects.filter(phone_number=phone_number):
                messages.info(request,"Phone Number already exists!")
                return redirect('v_register')
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.first_name = name
            user.email = email
            user.save()
            # Create a user profile
            customer.objects.create(user=user, name = username, email=email, phone_number=phone_number)
            # Authenticate the user and log them in
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request,"Kindly agree to the Terms & Conditions.")
            return redirect('v_register')

    context={}
    return render(request,'v_register.html',context)

def vendor_logout(request):
    logout(request)
    return redirect('v_login')
