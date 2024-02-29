from django.shortcuts import render,redirect,HttpResponse
from store.models import *
from .models import *
from .utils import *
from django.conf import settings
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
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@csrf_exempt
def vendor_requirded(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

@vendor_requirded(login_url='v_login')
def dashboard(request):
    try:
        # order_list = orders.objects.all() 
        if products.objects.filter(vendoraddedby = request.user.customer.id):
            product = products.objects.filter(vendoraddedby = request.user.customer.id)
        else:
            product = []
        if orders.objects.filter(vendor_id = request.user.id).exists():
            order_list = orders.objects.filter(vendor_id = request.user.id)
        else:
            order_list =[]
    except Exception as e:
        print(e)
    
    context={'navbar':'dashboard','products':product,'order_list':order_list}
    return render(request,'dashboard.html',context)

@vendor_requirded(login_url='v_login')
def vendor_profile(request):
    user = request.user
    last_login = LastLogin.objects.get(user=user)
    if address.objects.filter(isactive=True,username = user).exists():
        address_ins = address.objects.get(isactive=True,username = user)
    else:
        address_ins = []
    if customer.objects.filter(user=user).exists():
        cust_ins = customer.objects.get(user=user)
    else:
        cust_ins = []
    if store_details.objects.filter(store_vendor=user).exists():
        store_ins = store_details.objects.get(store_vendor=user)
    else:
        store_ins = []
    if request.method=="POST":
        if 'profile_update' in request.POST:
            try:
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
                cust_ins.save()

                if not address.objects.filter(username=request.user):
                    address.objects.create(username=request.user,name=name,email=user_email,phone=user_phone,abline1=abline1,abline2=abline2,abline3=abline3,city=city,state=state,zip=postal,isactive=True)
                    messages.success(request,"Address added successfully.")
                    return redirect('store_details')
                elif address.objects.filter(name=name,zip=postal).exists():
                    messages.error(request,"Address already exists!")
                    return redirect('store_details')
                else:
                    address.objects.create(username=request.user,name=name,email=user_email,phone=user_phone,abline1=abline1,abline2=abline2,abline3=abline3,city=city,state=state,zip=postal)

                return redirect('store_details')
            except Exception as e:
                messages.error(request,e)
                return redirect('store_details')
        
        if 'store_update' in request.POST:
            try:
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
                if not store_details.objects.filter(store_vendor = request.user):
                    store_details.objects.create(store_vendor = request.user,store_name=store_name,store_email=store_email,abline1=store_abline1,abline2=store_abline2,abline3=store_abline3,city=city,district=district,store_facebook=store_facebook,store_instagram=store_instagram,store_twitter=store_twitter,zip=zip,store_logo = request.FILES['store_logo'])
                    messages.success(request,"Store created.")
                    return redirect('store_details')
                elif store_details.objects.filter(store_vendor = request.user).exists():
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
                else:
                    store_details.objects.create(store_vendor = request.user,store_name=store_name,store_email=store_email,abline1=store_abline1,abline2=store_abline2,abline3=store_abline3,city=city,district=district,store_facebook=store_facebook,store_instagram=store_instagram,store_twitter=store_twitter,zip=zip,store_logo = request.FILES['store_logo'])
                    return redirect('store_details')
            
            except Exception as e:
                print(e)
                messages.success(request,e)
                return redirect('store_details')
        

        if 'update_user' in request.POST:
            try:
                username= request.POST.get('username')
                password= request.POST.get('password')
                user = User.objects.filter(username=username).first()
                print(user)
                user.set_password(password)
                user.save()
                messages.success(request,"Login credentials changed.")
                return redirect('v_login')
            except Exception as e:
                messages.success(request, str(e))
                return redirect('v_login')



    cur_date = date.today() 
    if cust_ins.birthday is not None:
        age = cur_date.year - cust_ins.birthday.year
    else:
        age = ''
    context={'navbar':'store_details','user':user,'last_login':last_login,'address_ins':address_ins,'store_ins':store_ins,'age':age}
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
    try:
        varient_name = request.POST.get('varient_name')
        color_code = request.POST.get('color_code')
        quantity = request.POST.get('quantity')
        variant.product_id=product_ins
        variant.varient_name = varient_name
        variant.color_code = color_code
        variant.quantity = quantity
        variant.save()
    except Exception as e:
        print(e)
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
        try:
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

            if not products.objects.filter(itmname=product_name,itmtitle=product_title,vendoraddedby = request.user.customer,itm_old_price=old_price,itm_new_price=new_price,sku_no=product_sku,itm_tags=product_tag).exists():
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
        except Exception as e:
            print(e)
        return redirect('products')

    categories = category.objects.all() 
    sub_categories = subcategory.objects.all()
    context={'navbar':'products','categories':categories,'sub_categories':sub_categories}
    return render(request,'product_add.html',context)

@vendor_requirded(login_url='v_login')
def product_details(request,id):
    if request.method=='POST':
        try:
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
        
        except Exception as e:
            print(e)


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
    store_details_ins = store_details.objects.filter(store_vendor=request.user).first()
    order_list = orders.objects.filter(vendor_id = store_details_ins)
    print(order_list.first())
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
        try:
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
        except Exception as e:
            messages.error(request,e)
            return redirect('/coupon_edit/'+ str(id))
    
    context = {'navbar': 'sales_promotions', 'categories': categories, 'coupon': coupon}
    return render(request, 'coupon_edit.html', context)

@vendor_requirded(login_url='v_login')
def coupon_add(request):
    categories = category.objects.all()
    if request.method == 'POST':
        try:
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
        except Exception as e:
            print(e)
            messages.error(request,e)
            return redirect('/coupon_add/')
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
def vendor_login(request):
    if request.method == "POST":
        try:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request,username = username, password=password)
            login(request,user)
            store_document_ins = store_document.objects.filter(store_vendor=request.user.id).exists()
            if user is None:
                messages.error(request,"Enter correct credintials!")
                return redirect('v_login')
            elif user.is_staff == True:
                return redirect('v_dashboard')
            elif store_document_ins == False:
                messages.error(request,"Please verify your documents.")
                return redirect('v_register_type')
            else:
                messages.error(request,"You are not verified yet.")
                return redirect('v_login')
        except Exception as e:
            messages.error(request,e)
            return redirect('v_login')

    context={}
    return render(request,'v_login.html',context)

@csrf_exempt
def v_register(request,*args, **kwargs):
    code  = str(kwargs.get('ref_code'))
    if request.method == 'POST':
        try:
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
                if code == "None":
                    customer.objects.create(user=user, name = username, email=email, phone_number=phone_number)
                    
                else:
                    user_ins = customer.objects.get(code = code)
                    customer.objects.create(user=user, name = username, email=email, phone_number=phone_number,referred_by_user=user_ins.user)
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('waiting_email_verification')
            else:
                messages.error(request,"Kindly agree to the Terms & Conditions.")
                return redirect('v_register')
        except Exception as e:
            messages.error(request,e)
            return redirect('v_register')
    context={}
    return render(request,'v_register.html',context)

def waiting_email_verification(request):
    cust_ins = customer.objects.get(user=request.user)
    if cust_ins.email_isverified == True:
        return redirect('v_register_type')
    else:
        subject = 'Please verify your email.'
        from_email = settings.EMAIL_HOST_USER
        to_email = [cust_ins.email]
        # static_image_url = f"{settings.BASE_URL}{settings.STATIC_URL}/images/logo-blue.png"
        base_url = settings.BASE_URL
        html_content = render_to_string('email_verification.html', {'base_url':base_url,'customer_ins': cust_ins})
        email = EmailMultiAlternatives(subject, 'This is a plain text message.', from_email, to_email)
        email.attach_alternative(html_content, "text/html")
        email.send()
    return render(request,'wating_email_verification.html')

def verify_email(request,*args, **kwargs):
    token  = str(kwargs.get('token'))
    cust_ins = customer.objects.get(user=request.user)
    try:
        if token == cust_ins.email_verification_code:
            cust_ins.email_isverified = True
            cust_ins.save()
            return redirect('v_register_type')
    except Exception:
        return redirect('waiting_email_verification')

def v_register_type(request):
    cust_ins = customer.objects.get(user=request.user)
    if cust_ins.email_isverified == False:
        return redirect('verify_email')
    return render(request,'v_register_type.html')

def v_register_gst(request):
    if request.method == 'POST':
        try:
            store_name = request.POST['store_name']
            gst_no = request.POST['gst_no']
            micr_code = request.POST['micr_code']

            if not store_document.objects.filter(store_vendor = request.user):
                if not store_document.objects.filter(gst_no=gst_no).exists():
                    store_details.objects.create(store_vendor = request.user,store_name=store_name)
                    store_document.objects.create(store_vendor=request.user,adhar_card=request.FILES['adhar_card'],cancel_check=request.FILES['cancelled_check'],pan_card=request.FILES['pan_card'],gst_no=gst_no,gst_certificate=request.FILES['gst_certificate'],bank_micr=micr_code)
                    if 'trade_lisence' in request.FILES:
                        store_ins = store_document.objects.get(gst_no=gst_no)
                        store_ins.trade_lisence=request.FILES['trade_lisence']
                else:
                    messages.success(request,"GST already exists!")
                    return redirect('v_register_gst')
                messages.success(request,"We are verifying your account.")
                return redirect('v_login')
            else:
                messages.error(request,"Store already exists!")
                return redirect('v_login')
        except Exception as e:
            messages.error(request,"Fill the form correctly.")
            return redirect('v_register_gst')

    return render(request,'register_gst.html')

def v_register_addhar(request):
    if request.method == 'POST':
        try:
            store_name = request.POST['store_name']
            micr_code = request.POST['micr_code']
            if not store_document.objects.filter(store_vendor = request.user):
                if not store_document.objects.filter(store_vendor = request.user).exists():
                    store_details.objects.create(store_vendor = request.user,store_name=store_name)
                    store_document.objects.create(store_vendor=request.user,adhar_card=request.FILES['adhar_card'],cancel_check=request.FILES['cancelled_check'],pan_card=request.FILES['pan_card'],bank_micr=micr_code)
                else:
                    messages.success(request,"Document already exists!")
                    return redirect('v_register_gst')
                messages.success(request,"We are verifying your account.")
                return redirect('v_login')
            else:
                messages.error(request,"Store already exists!")
                return redirect('v_login')
        except Exception as e:
            print(e)
            messages.error(request,"Fill the form correctly.")
            return redirect('v_register_addhar')
    return render(request,'register_addhar.html')

def vendor_logout(request):
    logout(request)
    return redirect('v_login')


# def send_email_verification(request):
#     email_code = 