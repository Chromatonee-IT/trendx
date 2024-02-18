from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Sum
from .models import *
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='login')
def home(request):
    home_offer = home_offers.objects.all()
    cur_user  = request.user if request.user.is_authenticated else None
    categories = category.objects.all()
    context = {'cur_user':cur_user,'categories':categories,'home_offers':home_offer}
    return render(request,'store/home.html',context)

@login_required(login_url='login')
def all_products(request):
    all_product = products.objects.all()
    cur_user  = request.user if request.user.is_authenticated else None
    categories = category.objects.all()
    context = {'all_product':all_product,'categories':categories,'cur_user':cur_user}
    return render(request,'store/all_products.html',context)

@login_required(login_url='login')
def cart(request):
    context = {}
    return render(request,'store/cart.html',context)
@login_required(login_url='login')
def checkout(request):
    context = {}
    return render(request,'store/checkout.html',context)

@login_required(login_url='login')
def all_stores(request):
    cur_user  = request.user if request.user.is_authenticated else None
    categories = category.objects.all()
    context = {'cur_user':cur_user,'categories':categories}
    return render(request,'store/all_stores.html',context)
@csrf_exempt
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info("Enter correct Login info.")
            return redirect('login')
    context = {}
    return render(request,'store/login.html',context)
@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone']

        # validation
        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already exists!")
            return redirect('register')
        if customer.objects.filter(phone_number=phone_number):
            messages.info(request,"Phone Number already exists!")
            return redirect('register')

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
        return redirect('home')
    context = {}
    return render(request,'store/register.html',context)

def forgotpass(request):
    context = {}
    return render(request,'store/forgotpassword.html',context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request,'Logout successful.')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    customer_instance = get_object_or_404(customer,user=request.user)
    if request.method == 'POST':
        customer_instance.name = request.POST['name']
        customer_instance.email = request.POST['email']
        customer_instance.phone_number = request.POST['phone']
        if customer.objects.filter(user=request.user).exists():
            customer_instance.save()
            messages.success(request,'Profile Updated.')
            return redirect('dashboard')
        else:
            messages.info(request,"some error.")
            return redirect('dashboard')
            
    cur_user  = customer.objects.filter(user=request.user)
    context = {'cur_user':cur_user}
    return render(request,'store/account_details.html',context)

@login_required(login_url='login')
def orders_user(request):
    cur_user  = customer.objects.filter(user=request.user)
    context = {'cur_user':cur_user}
    return render(request,'store/orders.html',context)

@login_required(login_url='login')
def address_user(request):
    if request.method == 'POST':
        if 'address_addbtn' in request.POST:
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            addln1 = request.POST['adrline1']
            addln2 = request.POST['adrline2']
            addln3 = request.POST['adrline3']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            postal = request.POST['zip']

            if not address.objects.filter(username=request.user):
                address.objects.create(username=request.user,name=name,email=email,phone=phone,abline1=addln1,abline2=addln2,abline3=addln3,city=city,state=state,country=country,zip=postal,isactive=True)
                messages.success(request,"Address added successfully.")
                return redirect('address')
            elif address.objects.filter(name=name,zip=postal).exists():
                messages.error(request,"Address already exists!")
                return redirect('address')
            else:
                address.objects.create(username=request.user,name=name,email=email,phone=phone,abline1=addln1,abline2=addln2,abline3=addln3,city=city,state=state,country=country,zip=postal)
                messages.success(request,"Address added successfully.")
                return redirect('address')
        if 'address_editbtn' in request.POST:
            name = request.POST['name_edit']
            phone = request.POST['phone_edit']
            email = request.POST['email_edit']
            addln1 = request.POST['adrline1_edit']
            addln2 = request.POST['adrline2_edit']
            addln3 = request.POST['adrline3_edit']
            city = request.POST['city_edit']
            state = request.POST['state_edit']
            country = request.POST['country_edit']
            postal = request.POST['zip_edit']
            if address.objects.filter(name=name,zip=postal).exists():
                print("success!!!")
                address.objects.filter(username=request.user,name=name,email=email,phone=phone,abline1=addln1,abline2=addln2,abline3=addln3,city=city,state=state,country=country,zip=postal).update(username=request.user,name=name,email=email,phone=phone,abline1=addln1,abline2=addln2,abline3=addln3,city=city,state=state,country=country,zip=postal)
                messages.success(request,'Address updated.')
                return redirect('address')
            else:
                print("success!!!")
                messages.error(request,'Error updating address.')
                return redirect('address')
        
    addresses = address.objects.filter(username=request.user)
    active_address = address.objects.filter(isactive=True)
    cur_user=customer.objects.filter(user=request.user)
    context = {'addresses':addresses,'active_address':active_address,'cur_user':cur_user}
    return render(request,'store/address.html',context)

@login_required(login_url='login')
def payment_method(request):
    context = {}
    return render(request,'store/payment_method.html',context)

@login_required(login_url='login')
def my_reviews(request):
    my_reviews = reviews.objects.filter(username=request.user)
    print(my_reviews)
    context = {'my_reviews':my_reviews}
    return render(request,'store/my_reviews.html',context)

@login_required(login_url='login')
def my_favourites(request):
    Products = products.objects.all()
    context = {'products':Products}
    return render(request,'store/my_favourites.html',context)

@login_required(login_url='login')
def product_single(request,id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review = request.POST.get('review')
        if not reviews.objects.filter(username = request.user,product_id = id):
            reviews.objects.create(username = request.user,product_id = id,rating = rating, review = review)
            messages.success(request,'Review submitted.')
            return redirect('product_single',id=id)
        else:
            messages.error(request,'Already reviewed this product.')
            return redirect('all_products')
    single_product = products.objects.filter(id=id)
    all_reviews = reviews.objects.filter(product = id)
    if reviews.objects.filter(product_id = id):
        review_stats = reviews.objects.filter(product_id = id).aggregate(
            total_reviews=Count('id'),
            average_rating=Avg('rating')
        )
        total_reviews = review_stats['total_reviews']
        average_rating = review_stats['average_rating']
    else:
        total_reviews = '0'
        average_rating = '0'
    cur_user  = request.user if request.user.is_authenticated else None
    categories = category.objects.all()
    context = {'cur_user':cur_user,'products':single_product,'reviews':all_reviews,'total_reviews':total_reviews,'average_rating':round(int(average_rating)),'categories':categories}
    return render(request,'store/product_single.html',context)

def category_detail(request,category_name):
    new_arrival = products.objects.filter(itmclass__classname = category_name).order_by('-itm_datecreated')
    cur_user  = request.user if request.user.is_authenticated else None
    categories = category.objects.all()
    sub_categories = subcategory.objects.filter(itmclass__classname = category_name)
    for sub_category in sub_categories:
        print(sub_category.classname,sub_category.get_product_total)
    context = {'cur_user':cur_user,'categories':categories,'new_arrival':new_arrival,'cur_category':category_name,'sub_categories':sub_categories}
    if category.objects.filter(classname = category_name):
        return render(request,'store/category_page.html',context)
    else:
        return redirect('/')

def subcategory_detail(request,category_name,subcategory_name):
    new_arrival = products.objects.filter(itmsubclass__classname = subcategory_name).order_by('-itm_datecreated')
    cur_user  = request.user if request.user.is_authenticated else None
    categories = category.objects.all()
    sub_categories = subcategory.objects.filter(itmsubclass__classname = subcategory_name)
    context = {'cur_user':cur_user,'categories':categories,'new_arrival':new_arrival,'cur_category':category_name,'sub_categories':sub_categories}
    return render(request,'store/subcategory_page.html',context)