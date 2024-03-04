from django.db import models
from django.contrib.auth.models import User
from django.db.models import  Sum,Avg,Count
from vendor.models import *
from vendor.utils import *



# Create your models here.
class customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=15,null=True)
    email = models.EmailField(max_length=200, null=True)
    email_verification_code = models.CharField(max_length=100, blank=True)
    email_isverified = models.BooleanField(default=False)
    vendor_active_email = models.BooleanField(default=False)
    birthday = models.DateField(blank=True,null=True)
    code = models.CharField(max_length=12,blank=True)
    referred_by_user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='referred_by')
    cusstomer_image = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    user_datecreated = models.DateTimeField(auto_now_add=True)
    user_dateupdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_recoended_by(self, *args, **kwargs):
        pass
    
    def save(self, *args, **kwargs):
        if self.code == "" or self.email_verification_code == "":
            code = generate_ref_code()
            email_code = generate_email_verification_code()
            self.code = code
            self.email_verification_code = email_code
        super().save(*args,**kwargs)

    def total_order(self):
        total = 0
        for order in orders.objects.filter(cutomer_id = self.id):
            total += 1
        return total
    
class LastLogin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    browser_name = models.CharField(max_length=50,null=True, blank=True)
    device_name = models.CharField(max_length=50,null=True, blank=True)
    last_login_timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return str(self.user)

class address(models.Model):
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null =True)
    name = models.CharField(max_length=50, null= True)
    email = models.CharField(max_length=50, null = True)
    phone = models.IntegerField(null=True)
    abline1 = models.CharField(max_length=200, null=True)
    abline2 = models.CharField(max_length=200, null=True)
    abline3 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    district = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    zip = models.IntegerField(null=False)
    isactive = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class category(models.Model):
    itmclass = models.CharField(max_length=50,null=True)
    classname = models.CharField(max_length=50,null=True)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.classname

class subcategory(models.Model):
    itmclass = models.ForeignKey(category,on_delete=models.SET_NULL,null=True)
    itmsubclass = models.CharField(max_length=50,null=True)
    classname = models.CharField(max_length=50,null=True)
    isactive = models.BooleanField(default=True)

    def __str__(self):
        return self.classname

    @property
    def get_product_total(self):
        sub_product = products.objects.filter(itmsubclass = self.id).aggregate(
            total_product = Sum('pk')
        )
        total_product = sub_product['total_product']
        if total_product:
            return total_product
        else:
            return 0

    

class products(models.Model):
    itmname = models.CharField(max_length=100, null=True)
    itmtitle = models.CharField(max_length=100,null=True)
    itmdesc = models.CharField(max_length=500, null=True)
    itm_old_price = models.IntegerField(null=True)
    itm_new_price = models.IntegerField(null=True)
    itmclass = models.ForeignKey(category,on_delete=models.SET_NULL,null = True)
    itmsubclass = models.ForeignKey(subcategory,on_delete=models.SET_NULL,null = True)
    vendoraddedby = models.ForeignKey(customer,on_delete=models.SET_NULL,null = True)
    itm_isactive = models.BooleanField(default = True)
    sku_no = models.CharField(max_length=10,null=True,blank=True)
    itm_tags = models.CharField(max_length=10,null=True,blank=True)
    itm_barcode = models.CharField(max_length=10,null=True,blank=True)
    itm_datecreated = models.DateTimeField(auto_now_add=True)
    itm_dateupdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.itmname+str(self.id))

    @property
    def get_variants(self):
        product_variant = product_variants.objects.filter(product_id = self.id)
        return product_variant
    
    @property
    def total_review(self):
        if reviews.objects.filter(product_id = self.id):
            review_stats = reviews.objects.filter(product_id = self.id).aggregate(
                total_reviews=Count('id')
            )
            total_reviews = review_stats['total_reviews']
        else:
            total_reviews = '0'
        return total_reviews
    
    @property
    def average_rating(self):
        if reviews.objects.filter(product_id = self.id):
            review_stats = reviews.objects.filter(product_id = self.id).aggregate(
                average_rating=Avg('rating')
            )
            average_rating = review_stats['average_rating']
        else:
            average_rating = '0'
        return round(int(average_rating))
    
    @total_review.setter
    def get_average_rating(self,value):
        if reviews.objects.filter(product_id = self.id):
            review_stats = reviews.objects.filter(product_id = self.id).aggregate(
                average_rating=Avg('rating')
            )
            average_rating = review_stats['average_rating']
        else:
            average_rating = '0'
        return round(int(average_rating))


class product_images(models.Model):
    product_id = models.OneToOneField(products,on_delete=models.SET_NULL,null=True)
    image1 = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    image2 = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    image3 = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    image4 = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    image5 = models.ImageField(upload_to='images/uploads/',null=True,blank=True)
    def __str__(self):
        return str(self.product_id)

class product_variants(models.Model):
    product_id=models.ForeignKey(products,on_delete=models.SET_NULL,null=True,blank=True)
    varient_name = models.CharField(max_length=10,null=True,blank=True)
    color_code = models.CharField(max_length=10,null=True,blank=True)
    quantity = models.CharField(max_length=10,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_id) , str(self.varient_name)
    
class product_metas(models.Model):
    product_id = models.ForeignKey(products,on_delete=models.SET_NULL,null=True,blank=True)
    meta_link = models.CharField(max_length=50,null=True,blank=True)
    meta_title = models.CharField(max_length=50,null=True,blank=True)
    meta_description = models.CharField(max_length=100,null=True,blank=True)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product_id)

class orders(models.Model):
    vendor_id = models.ForeignKey(store_details,on_delete=models.SET_NULL, null=True)
    orderdate = models.DateTimeField(auto_now_add=True)
    shippeddate = models.DateTimeField(null=True)
    deliverydate = models.DateTimeField(null=True)
    items = models.ManyToManyField(products)
    shipto = models.ForeignKey(address,on_delete=models.SET_NULL,null=True)
    cutomer_id = models.ForeignKey(customer,on_delete=models.SET_NULL, null=True)
    paymentid = models.CharField(max_length=50,null = False)
    order_dateupdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def order_total(self):
        total = 0
        for product in self.items.all():
            total += product.itm_new_price
        return total
    
class orderitems(models.Model):
    customer = models.ForeignKey(customer,on_delete=models.CASCADE)
    order = models.ForeignKey(orders,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)
    

class order_invoices(models.Model):
    order_id = models.ForeignKey(orders,on_delete=models.SET_NULL,null=True)
    invoice_amount = models.IntegerField(null=True,blank=True)
    invoice_date = models.DateTimeField(auto_now_add=True)
    if_updated = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.id)





class reviews(models.Model):
    username = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(products, on_delete=models.SET_NULL,null=True)
    rating = models.IntegerField(null=True)
    review = models.CharField(max_length=100,null=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review
    
class home_offers(models.Model):
    offer_title = models.CharField(max_length=50,null=False)
    offer_desc = models.CharField(max_length=100,null=False)
    offer_image = models.ImageField(upload_to='images/uploads/')
    date_created = models.DateTimeField(auto_now=True)

class discount_type(models.Model):
    offer_name = models.CharField(max_length =20,null=True,blank=False)
    date_created= models.DateTimeField(auto_now = True,blank=True)

    def __str__(self):
        return str(self.offer_name)

class discount(models.Model):
    offer = models.CharField(max_length =20,null=True,blank=False)
    offer_cat = models.ForeignKey(discount_type, on_delete=models.SET_NULL,null=True)
    if_on_category = models.ForeignKey(category,on_delete=models.SET_NULL,null=True,blank=True)
    if_on_product = models.ForeignKey(products,on_delete=models.SET_NULL,null=True,blank=True)
    discount_value = models.CharField(max_length=6,null=True,blank=True)
    vendor_by = models.ForeignKey(User,on_delete = models.SET_NULL,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    date_created= models.DateTimeField(auto_now = True,blank=True)
    date_updated = models.DateTimeField(auto_now_add=True,blank=True)

    def __str__(self):
        return str(self.offer)
    



