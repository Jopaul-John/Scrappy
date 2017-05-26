
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.forms import forms,ModelForm
from datetime import datetime,timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    is_dealer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=True)
    ph_no = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    city = models.CharField(max_length= 20)
    street = models.CharField(max_length=25,null=True)
    state = models.CharField(max_length=25)
    reg_image = models.ImageField()
    landmark = models.CharField(max_length=30)
    reg_id = models.CharField(max_length=20)
    ratings = models.IntegerField(null=True)
    verify = models.CharField(max_length=6,default='')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    pname = models.CharField(max_length=20)
    baseprice =models.IntegerField()
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.pname


class Ads(models.Model):
    pname = models.ForeignKey(Product,on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile, null=True)
    date = models.DateTimeField(default=datetime.now, blank=True)
    quantity = models.IntegerField()
    price = models.IntegerField()
    is_actibe = models.BooleanField(default= True)
    club_friend = models.BooleanField(default=False)
    is_bidded = models.BooleanField(default=False)
    expires = models.DateTimeField(default=datetime.now()+timedelta(days=7))
    is_new = models.BooleanField(default=True)

    def __str__(self):
        return '%s %s %s' %(format(self.pk),self.pname,self.username)


class Expired_Ad(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,unique=False)
    ad = models.OneToOneField(Ads,on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' %(self.user,self.ad)

class Bid(models.Model):
    ad_id = models.ForeignKey(Ads,on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    bid_time = models.DateTimeField(default=datetime.now,null = True)
    bidded_by = models.ForeignKey(UserProfile,on_delete=models.CASCADE,)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return 'bid for ad( no.%s) by %s is %srs' %(format(self.ad_id),format(self.bidded_by),format(self.bid_amount))

class Bid_Detail(models.Model):
    seller_name = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    ad = models.OneToOneField(Ads,on_delete=models.CASCADE)
    bid_detail = models.OneToOneField(Bid,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,)
    amount = models.IntegerField()
    bidder_name = models.CharField(max_length=30,)

    def __str__(self):
        return '%s %s %s %s'%(self.seller_name,self.ad,self.bid_detail,self.product)


class ContactUs(models.Model):
    Name = models.CharField(max_length=30)
    place = models.CharField(max_length=30)
    mobile = models.CharField(max_length=10)
    message = models.CharField(max_length=500)
    email = models.EmailField()
    status = models.BooleanField(default=True)
    reply = models.CharField(max_length=500,default='')

    def __str__(self):
        return '%s %s' %(self.Name,self.mobile)

class Cart(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    product =models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    ads = models.ForeignKey(Ads,on_delete=models.CASCADE)
    bid = models.ForeignKey(Bid,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return '%s %s %s'%(self.user,self.product,self.ads)

class Wallet(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return '%s %s' %(format(self.user),self.amount)

class Transactions(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    ad = models.OneToOneField(Ads,on_delete=models.CASCADE)
    is_rated = models.BooleanField(default=False)
    bid_detail = models.OneToOneField(Bid_Detail,on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s %s' %(format(self.user),self.ad,format(self.id))


class ProductProfit(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    sell_price = models.IntegerField()

    def __str__(self):
        return '%s %s' %(format(self.product),self.user)

class Profit(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    product = models.OneToOneField(ProductProfit,on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return format(self.user)

