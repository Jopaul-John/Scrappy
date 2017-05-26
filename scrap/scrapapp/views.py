from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import *
from django.template.loader import get_template
from django.template import Context
from django.template.context_processors import request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.core.serializers.json import DjangoJSONEncoder
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import modelformset_factory
from .forms import *
from datetime import datetime,date
from django.apps import *
from django.core.mail import send_mail, BadHeaderError,EmailMultiAlternatives
import random,traceback,json
from django.utils.safestring import mark_safe
from scrapapp.serializers import AdSerializer, ProductSerializer
from rest_framework import serializers
from django.core import serializers
from collections import Counter
import jsonpickle
from django.http import JsonResponse




def My_User(user):
    currentuser = UserProfile.objects.get(user=user)
    return currentuser

def sendmail(user,subject,message):
    html = get_template('scrapapp/email.html')
    try:
        print(user.email)
        currentuser = My_User(user)
        toaddress=[user.email]
        username = Context({'user':currentuser.user})
        htmlcontent = html.render({'username':username,'message':message})

    except:
        toaddress = [user]
        username = user
        htmlcontent = html.render({'username':username,'message':message})
        print("else statement is reached")

    emaildetail = EmailMultiAlternatives(subject,message,'scrappyteam.in@gmail.com',toaddress)
    emaildetail.attach_alternative(htmlcontent,'text/html')
    try:
        emaildetail.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


def validate_user(request):
    username = request.GET.get('username')
    data = {'is_taken':User.objects.filter(username__iexact=username).exists()}
    return JsonResponse(data)

def adminlogin(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect('/home/')
    contact_msg = ContactUs.objects.filter(status=True)
    if request.POST:
        answer = format(request.POST.get('message'))
        print("answer = "+answer)
        id = format(request.POST.get('id'))
        try:
            reply_msg = ContactUs.objects.get(id=id)
            message = answer
            subject = "regarding you enquiry about "+format(reply_msg.message)
            sendmail(format(reply_msg.email),subject,message)
            reply_msg.status = False
            reply_msg.reply = answer
            reply_msg.save()
            print(answer+id)
            status = {'status':"yes"}
            return JsonResponse(status)
        except:
            status = {'status': "no"}
            return JsonResponse(status)
    return render(request,'scrapapp/admin.html',{'messages':contact_msg})

def eeee():
    ads = Bid.objects.all()
    for ad in ads:
        print(ad.bidded_by)

    date = datetime.now()
    newdate = date + timedelta(days=7)
    for ad in ads:
        ad.is_actibe = True
        ad.is_new= True
        ad.expires = newdate
        ad.save()
    return



def home(request):
    #eeee()
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user=request.user)
        except:
            user = User.objects.get(username=request.user)
            if user.is_superuser:
                return HttpResponseRedirect('/adminlogin/')
        if not user.is_active:
            return HttpResponseRedirect('/codeverify/')
        if user.is_seller :
            return HttpResponseRedirect("/sellerlogin/")
        elif user.is_dealer:
            return HttpResponseRedirect("/dealerlogin/")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)

        user = authenticate(username=username, password=password)
        superuser = User.objects.get(username=username)
        if superuser.is_superuser:
            login(request,superuser)
            return HttpResponseRedirect('/adminlogin/')
        if user:
            login(request, user)
            userstatus = UserProfile.objects.get(user=user)
            print(userstatus)
            if userstatus.is_dealer:
                return HttpResponseRedirect('/dealerlogin/')
            else:
                return HttpResponseRedirect('/sellerlogin/')
        else:
            error = "Invalid Credentials"
            return render(request, 'scrapapp/home.html', {'error': error})

    else:
        dealer = '/dealerregister/'
        seller = '/sellerregister/'
        return render(request, 'scrapapp/home.html', {'dealerreg': dealer, 'sellerreg': seller})


def dealerreg(request):
    if request.method == 'POST':
        userformset = userform(request.POST)
        formset = Dealer(request.POST, request.FILES)
        if userformset.is_valid() and formset.is_valid():
            myuser = userformset.save()
            password = request.POST.get('password')
            myuser.set_password(request.POST['password'])
            myuser.save()
            profile = formset.save(commit=False)
            profile.user = myuser
            profile.is_dealer = True
            profile.is_seller = False
            profile.verify = verify()
            try:
                profile.save()
                subject = format(profile.user)+", Welcome to Scrappy Team !"
                message = format(profile.user)+", your Verification Code is : "+format(profile.verify)+" "
                sendmail(profile.user,subject,message)
            except:
                traceback.print_exc()
                return HttpResponse("couldnt register")
            status = 'Registration successful'
            user = authenticate(username=profile.user, password=password)
            if user:
                login(request, user)
            return HttpResponseRedirect('/codeverify/')
            #return render(request, 'scrapapp/register.html', {'status': status, 'form': formset, 'user': userformset})
        else:
            status = 'Registration unsuccessful'
            return render(request, 'scrapapp/register.html', {'status': status, 'form': formset, 'user': userformset})
    else:
        userformset = 'dealer'
        formset = 'dealer'
        return render(request, 'scrapapp/register.html', {'form': formset, 'user': userformset})


def sellerreg(request):
    if request.POST:
        userformset = userform(request.POST)
        formset = Seller(request.POST)
        if userformset.is_valid() and formset.is_valid():
            myuser = userformset.save()
            password = request.POST.get('password')
            print(password)
            myuser.set_password(password)
            myuser.save()
            profile = formset.save(commit=False)
            profile.user = myuser
            profile.verify = verify()
            try:
                profile.save()
                subject = "Welcome to scrappy team"
                message = "Hearty welcome dear "+format(profile.user)+"\n your verfications code is "+format(profile.verify)+""
                sendmail(profile.user,subject,message)
            except:
                print(profile.user)
               # return HttpResponse("unsuccessful seller reg")
                traceback.print_exc()
            status = 'Registration successful'
            user = authenticate(username=profile.user, password=password)
            if user:
                login(request, user)
            print(user)
            return HttpResponseRedirect('/codeverify/')
           # return render(request, 'scrapapp/register.html', {'status': status, 'form': formset, 'user': userformset})
        else:
            status = 'Registration unsuccessful'
            return render(request, 'scrapapp/register.html', {'status': formset.errors, 'form': formset, 'user': userformset})
    else:
        userformset = 'seller'
        formset = 'seller'
        return render(request, 'scrapapp/register.html', {'form': formset, 'user': userformset})



def verify():
   number = format(random.randint(100000,999999))
   return number

@user_passes_test(User, login_url='/home/')
def codeverify(request):
    if not request.user.is_authenticated:
        HttpResponseRedirect('/home/')
    if request.POST:
        code = request.POST.get('code')
        print(code)
        currentuser = My_User(request.user)
        print(currentuser.verify)
        if code == currentuser.verify:
            currentuser.is_active = True
            currentuser.save()
            return HttpResponseRedirect('/home/')
        else:
            return HttpResponse("Invalid code")
    else:
        return render(request,'scrapapp/verfication.html',{'user':request.user})


def check_expiry():
    ads = Ads.objects.all()
    nowdate = date.today()
    print(ads)
    for ad in ads:
        #print(ad)
        if nowdate > datetime.date(ad.expires):
            print("expired ad = ")
            print(ad)
            ad.is_actibe = False
            ad.save()
            expired_ad = Expired_Ad()
            expired_ad.user = ad.username
            expired_ad.id = ad.id
            expired_ad.ad = ad
            expired_ad.save()
    return

@user_passes_test(User, login_url='/home/')
def dealerlogin(request):
    if not request.user.is_authenticated:
        alert = "You must login "
        return HttpResponseRedirect("/home/")


    id = '/logout/'

    check_expiry()

    myuser = UserProfile.objects.get(user=request.user)
    print(myuser.is_dealer)
    if not myuser.is_dealer:
        alert = "You must login "
        return HttpResponseRedirect("/home/")
    if not myuser.is_active:
        return HttpResponseRedirect('/codeverify/')

    user = UserProfile.objects.get(user=request.user)
    dealer_bids = Bid.objects.filter(bidded_by=user)
    items = Cart.objects.filter(user=user)
    total = 0
    basetotal = 0
    for bid in dealer_bids:
        total = total + bid.bid_amount
        basetotal = basetotal + bid.product.baseprice

    print(basetotal)
    differnce = total - basetotal
    if request.POST:
        value = format(request.POST.get('search'))
        pname = value.split()
        num = len(pname)
        print(num)
        message =None
        if num == 1:
            pro = pname[0]
            try:
                product = Product.objects.get(pname__contains=pro)
                ads = Ads.objects.filter(pname=product, is_actibe=True)
            except:
                ads = Ads.objects.filter(username__city__contains=pro,is_actibe=True).order_by('-id')
            if ads == None:
                message ="No results found"
            return render(request, 'scrapapp/dealer.html',
                      {'bids': dealer_bids, 'ads': ads, 'id': id, 'user': user, 'total': total,
                      'baseprice': basetotal,
                     'diff': differnce,
                    'items':items,'message':message})
        elif num == 2:
            pro = pname[0]
            city = pname[1]
            try:
                print("inside elif 2 try")
                ads = Ads.objects.filter(is_actibe=True,pname__pname__contains=pro,username__city__contains=city).order_by('-id')
            except:
                print("inside except of elif")
                pass
            print(ads)
            if not ads:
                print("inside if")
                try:
                    ads = Ads.objects.filter(is_actibe=True, pname__pname__contains=city, username__city__contains=pro).order_by('-id')
                except:
                    message = "No results found"
            return render(request, 'scrapapp/dealer.html',
                              {'bids': dealer_bids, 'ads': ads, 'id': id, 'user': user, 'total': total,
                               'baseprice': basetotal,
                               'diff': differnce,
                               'items': items,'message':message})
        else:
            message = "Wrong Input "
            return render(request, 'scrapapp/dealer.html',
                          {'bids': dealer_bids, 'message': message, 'id': id, 'user': user, 'total': total,
                           'baseprice': basetotal,
                           'diff': differnce,
                           'items': items})


    else:
        ads_list = Ads.objects.filter(is_actibe=True,).order_by('-id')
        paginator = Paginator(ads_list, 9)

        page = request.GET.get('page')
        try:
            ads = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            ads = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            ads = paginator.page(paginator.num_pages)
        return render(request, 'scrapapp/dealer.html',
                      {'bids': dealer_bids, 'ads': ads, 'id': id, 'user': user, 'total': total, 'baseprice': basetotal,
                       'diff': differnce,
                       'items':items})


@user_passes_test(User, login_url='/home/')
def sellerlogin(request):
    if not request.user.is_authenticated:
        alert = "You must login "
        return HttpResponseRedirect("/home/")


    myuser = UserProfile.objects.get(user=request.user)
    print(myuser.is_seller)
    if myuser.is_dealer:
        alert = "You must login "
        return HttpResponseRedirect("/home/")
    if not myuser.is_active:
        return HttpResponseRedirect('/codeverify/')
    userlist = UserProfile.objects.filter(city=myuser.city)

    logout_id = '/logout/'
    bids_id = '/bids/'
    product=""
    if request.POST:
        print("inside post")
        productid = request.POST.get('product')
        print(productid)
        try:

            product = Product.objects.get(id=productid)
            print(product)
            quantity = request.POST.get('quantity')
            price = request.POST.get('price')
            ad = Ads()
            ad.pname = product
            ad.username = myuser
            ad.quantity = quantity
            ad.price = price
            ad.date = datetime.now()
            ad.save()
            print(ad)
            message = "your Ads " + format(ad.pname) + " is sucessfully posted "
            subject = "Scrappy -Thanku you for giving your feedback"
            sendmail(request.user, subject, message)

        except:
            pass

        message = {'message':"success"}
        return JsonResponse(message)


        """
        if adsformset.is_valid():
            adsobj = adsformset.save(commit=False)
            currentuser = UserProfile.objects.get(user=request.user)
            adsobj.username = currentuser
            adsobj.date = datetime.now()
            adsobj.save()
            status = "Ad successfully Posted"

            message = "your Ads "+format(adsobj.pname)+" is sucessfully posted "
            subject = "Scrappy -Thanku you for giving your feedback"
            sendmail(request.user, subject, message)

            return render(request, 'scrapapp/seller.html',
                          {'status': status, 'ads': adsformset, 'user': request.user, 'id': logout_id, 'bids': bids_id})

        else:
            status = "Error in input"
            return render(request, 'scrapapp/seller.html', {'status': status, 'ads': adsformset, 'id': logout_id})
        """
    else:
        product = Product.objects.all()
        jsproducts = ProductSerializer(data=product)
        if jsproducts.is_valid():
            print("jsproducts are valid")
            print(jsproducts.data)

        adsformset = Adsform()
        return render(request, 'scrapapp/seller.html',
                      {'ads': adsformset,'jsproducts':jsproducts, 'id': logout_id, 'bids': bids_id, 'product': product,'userlist':userlist,'expired_ad':""})


@user_passes_test(User, login_url='/home/')
def adsid(request, id):
    if not request.user.is_authenticated:
        alert = "You must login "
        return HttpResponseRedirect("/home/")
    currentuser = My_User(request.user)
    print(currentuser)
    if currentuser.is_seller:
        return HttpResponseRedirect("/home/")
    if not currentuser.is_active:
        return HttpResponseRedirect('/codeverify/')

    print("8888888888888888888888888")
    print(currentuser.is_seller)
    date = datetime.now()
    """
    myuser = UserProfile.objects.get(user=request.user)
    print(myuser.is_seller)
    if myuser.is_seller:
        alert = "You must login "
        return render(request, 'scrapapp/home.html', {'alert': alert})
    """
    bidders_list = Bid.objects.filter(ad_id=id).order_by('-bid_amount')[:5]
    adsobj = get_object_or_404(Ads, id=id)
    adsobj.is_new = False
    adsobj.save()

    try:
        cartobject = Cart.objects.get(ads=adsobj)
    except:
        cartobject = None

    print("befor request.post")
    if request.POST:
        formset = Bidform(request.POST)
        print("inside request.post")
        if formset.is_valid():
            bids = formset.save(commit=False)
            id = Ads.objects.get(pk=id)

            print("inside formset valid")
            user = UserProfile.objects.get(user=request.user)

            try:
                print("user ="+format(user))
                newbids = Bid.objects.get(bidded_by=user,ad_id_id=id)
                newbids.bid_amount = bids.bid_amount
                newbids.bid_time = datetime.now()
                newbids.save()
                id.is_bidded = True
                id.save()
                print("new bids = "+format(newbids))
            except:
                print(traceback.format_exc())
                print("inside except")
                bids.ad_id = id
                bids.bidded_by = user
                bids.product = id.pname
                bids.bid_time = datetime.now()
                bids.save()
            status = 'Bidded Successfully '
            bidders_list = Bid.objects.filter(ad_id=id)
            return render(request, 'scrapapp/Ads.html',
                          {'ads': adsobj, 'form': formset, 'status': status, 'user': request.user,
                           'currentbidders': bidders_list, 'cart': cartobject})
        else:
            status = 'unsuccessfull bid'
            return render(request, 'scrapapp/Ads.html',
                          {'ads': adsobj, 'form': formset, 'status': status, 'user': request.user,
                           'currentbidders': bidders_list, 'cart': cartobject})
    else:

        formset = Bidform()
        return render(request, 'scrapapp/Ads.html',
                      {'ads': adsobj, 'form': formset, 'user': request.user, 'currentbidders': bidders_list,
                       'date': date, 'cart': cartobject})


def mycart(adsid, user):
    ad = Ads.objects.get(id=adsid)
    cart = Cart()
    cart.user = user
    cart.ads = ad
    cart.save()


@user_passes_test(User, login_url='/home/')
def cart(request):
    if not request.user.is_authenticated:
        alert = "You must login "
        return HttpResponseRedirect("/home/")
    currentuser = My_User(request.user)
    print(currentuser)
    if currentuser.is_seller:
        return HttpResponseRedirect("/home/")
    if not currentuser.is_active:
        return HttpResponseRedirect('/codeverify/')

    items = Cart.objects.filter(user=currentuser)

    return render(request, 'scrapapp/cart.html', {'items': items, 'user': currentuser})


@user_passes_test(User, login_url='/home/')
def bids(request, ):
    if not request.user.is_authenticated:
        alert = "You must login "
        return HttpResponseRedirect("/home/")
    user = UserProfile.objects.get(user=request.user)
    if user.is_dealer:
        return HttpResponseRedirect("/home/")

    if not user.is_active:
        return HttpResponseRedirect('/codeverify/')
    ads = Ads.objects.filter(username=user)

    return render(request, 'scrapapp/ad_detail.html', {'ads': ads, 'user': request.user.username})


@user_passes_test(User, login_url='/home/')
def viewbids(request, id):
    if not request.user.is_authenticated:
        alert = "You must login "
        return HttpResponseRedirect("/home/")
    currentuser = My_User(request.user)
    if currentuser.is_dealer:
        return HttpResponseRedirect("/home/")
    if not currentuser.is_active:
        return HttpResponseRedirect('/codeverify/')
    print("inside viewbids")
    try:
        bid_detail = Bid_Detail.objects.get(seller_name=currentuser)
        bid_message = "Your Deal has been Submitted Successfully to "+format(bid_detail.bidder_name)
    except:
        print("inside except")
        bid_message = None

    """
    if request.POST:
        try:
            bid_id = request.POST.get('id')
            print(bid_id)
            bid_info = Bid.objects.get(id=bid_id)
            print(bid_info)

            bid_detail_ob = Bid_Detail()
            bid_detail_ob.seller_name = ad.username
            bid_detail_ob.ad = ad
            bid_detail_ob.bid_detail = bid_info
            bid_detail_ob.amount = bid_info.bid_amount
            bid_detail_ob.product = ad.pname
            bid_detail_ob.bidder_name = bid_info.bidded_by
        except:
            pass
        try:
            bid_detail_ob.save()
            message = {'message':"Your order will be done within 2 days"}
            ad.is_actibe = False
            ad.save()
            return JsonResponse(message)
        except:
            message = {'message':"You have already finished bidding"}
            return JsonResponse(message)
            #return render(request, 'scrapapp/bids.html', {'mybids': viewbids,
            #                                             'user': request.user,
            #                                            'ad': ad,
            #                                           'biddetail': bid_detail_ob,
            #                                          'error': error})
"""

    ad = Ads.objects.get(id=id)
    viewbids = Bid.objects.filter(ad_id=id)
    expired_ads = Expired_Ad.objects.filter(user=currentuser)
    message = None
    return render(request, 'scrapapp/bids.html', {'mybids': viewbids,
                                                  'user': request.user,
                                                  'ad': ad,
                                                  'message': message,
                                                  'bid_message': bid_message,'expired_ad':expired_ads})


def recentbids(request):
    if not request.user.is_authenticated:
        alert = "You must login "
        return HttpResponseRedirect("/home/")

    user = UserProfile.objects.get(user=request.user)
    if user.is_seller:
        return HttpResponseRedirect("/home/")
    if not user.is_active:
        return HttpResponseRedirect('/codeverify/')

    dealer_bids = Bid.objects.filter(bidded_by=user)
    products = ProductProfit.objects.filter(user=user)
    total = 0
    basetotal = 0
    sellprice = 0
    for bid in dealer_bids:
        total = total + bid.bid_amount
        basetotal = basetotal + bid.product.baseprice




    differnce = total - basetotal
    return render(request, 'scrapapp/recentbids.html',
                  {'bids': dealer_bids, 'user': user, 'total': total, 'baseprice': basetotal,
                   'diff': differnce,})


def deals(request):
    if not request.user.is_authenticated:
        alert = "You must login "
        return render(request, 'scrapapp/home.html', {'alert': alert})

    user = UserProfile.objects.get(user=request.user)
    if user.is_seller:
        return HttpResponseRedirect("/home/")
    if not user.is_active:
        return HttpResponseRedirect('/codeverify/')

    mydeals = Bid.objects.filter(bidded_by=user)
    print(mydeals)

    return render(request, 'scrapapp/deals.html', {'mydeal': mydeals,
                                                   'user': user.user})


def dealsid(request, id):
    if not request.user.is_authenticated:
        alert = "You must login "
        return HttpResponseRedirect("/home/")
    currentuser = My_User(request.user)
    if currentuser.is_seller:
        return HttpResponseRedirect("/home/")
    if not currentuser.is_active:
        return HttpResponseRedirect('/codeverify/')

    mybid = 0
    user = 'none'
    mydeals = Bid.objects.get(id=id)
    mybid = Bid_Detail.objects.get(bid_detail=mydeals)

    if request.POST:
        try:
            print("inside dealsid try")
            transaction = Transactions()
            transaction.user = mydeals.ad_id.username
            transaction.ad = mydeals.ad_id
            transaction.is_rated = True
            transaction.bid_detail = mybid
            #
            try:
                print("inside try try")
                wallet = Wallet.objects.get(user=currentuser)
                if wallet.amount < mybid.amount:
                    message = {'message': " You dont have enough balance to do the transaction "}
                    return JsonResponse(message)
                else:
                    wallet.amount = wallet.amount - mybid.amount
                    transaction.save()
                    wallet.save()

                    try:
                        wallet = Wallet.objects.get(user=mybid.seller_name)
                        wallet.amount = wallet.amount + mybid.amount
                        wallet.save()
                    except:
                        wallet = Wallet()
                        wallet.user = mybid.seller_name
                        wallet.amount = mybid.amount
                        wallet.save()
                    message = {'message': "rs "+format(mybid.amount)+" has been reduced from your account"}
                    return JsonResponse(message)
            except:
                print("inside inner except")
                print(traceback.format_exc())
                wallet = Wallet()
                wallet.user = currentuser
                wallet.amount = mybid.amount
                wallet.save()

        except:
            print("inside outer except")
            pass

    try:
        user_seller = "something"
        mydeals = Bid.objects.get(id=id)
        mybid = Bid_Detail.objects.get(bid_detail=mydeals)
        seller = User.objects.get(username=mybid.seller_name)
        user = UserProfile.objects.get(user=seller)
        print("inside try")
    except:
        print("inside except")
        user_seller = None
        message = "Sorry your bids havent been taken yet"
        return render(request, 'scrapapp/recentbiddetails.html', {'message': message,'user_sell':user_seller})
    return render(request, 'scrapapp/recentbiddetails.html', {'mybid': mybid, 'user': user,'user_sell':user_seller})


def index(request):
    print(request.user)
    if request.POST:
        name = format(request.POST.get('name'))
        place = format(request.POST.get('place'))
        mobile = format(request.POST.get('mobile'))
        message = format(request.POST.get('msg'))
        email = format(request.POST.get('email'))
        print(name+place+mobile+email+message)
        contact = ContactUs()
        contact.Name = name
        contact.place = place
        contact.mobile = mobile
        contact.message = message
        contact.email = email
        flag = 0
        try:
            print(contact)
            message ={'message': "your question is sucessfully posted "}
            contactmessage = "thanks for giving your feedback for us..We will be in touch with you ASAP"
            subject = "Scrappy -Thanku you for giving your feedback"
            sendmail(email,subject,contactmessage)
            contact.save()
            return JsonResponse(message)
            #return render(request, 'scrapapp/index.html', {'message': message})
        except:
            message ={'message': "Please enter a valid email "}
            return JsonResponse(message)
            #return render(request, 'scrapapp/index.html', {'message': message})

    return render(request, 'scrapapp/index.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/home/')



def addtocart(request):
    if request.POST.get('id'):
        print("hello")
        print(request.POST.get('id'))

    currentuser = My_User(request.user)
    id = Ads.objects.get(id=request.POST.get('id'))

    try:
        cartobj = Cart.objects.get(ads=id)
        message = {'message': cartobj.id}
        print("last try")
    except:
        print("inside except")
        cartobj = "None"
        message = {'message': cartobj}

    if cartobj == "None":
        print("inside if")
        mycart(request.POST.get('id'), currentuser)
    else:
        print("inside else")
        deletecart = Cart.objects.get(ads=id)
        deletecart.delete()

    print(cartobj)
    return JsonResponse(message)


def acceptbid(request):
    id = request.POST.get("id")
    print("id = "+format(id))
    message = {'message':"data is here"}
    if request.POST:
        bid_info = Bid.objects.get(id=id)
        print(bid_info)
        ad = Ads.objects.get(id=bid_info.ad_id.id)
        print(ad)

        bid_detail_ob = Bid_Detail()
        bid_detail_ob.seller_name = ad.username
        bid_detail_ob.ad = ad
        bid_detail_ob.bid_detail = bid_info
        bid_detail_ob.amount = bid_info.bid_amount
        bid_detail_ob.product = ad.pname
        bid_detail_ob.bidder_name = bid_info.bidded_by
        try:
            bid_detail_ob.save()
            message = {'message':"Your Deal has been Submitted Successfully",'ajaxmsg':"true",'bidder':format(bid_detail_ob.bidder_name)}
            ad.is_actibe = False
            ad.save()
            return JsonResponse(message)
        except:
            message = {'message':"Your Deal has been Submitted Successfully",'ajaxmsg':"true",'bidder':format(bid_detail_ob.bidder_name)}
            return JsonResponse(message)
    return JsonResponse(message)



def wallet(request):
    if not request.user.is_authenticated:
        alert = "You must login "
        return HttpResponseRedirect("/home/")
    currentuser = My_User(request.user)
    if not currentuser.is_active:
        return HttpResponseRedirect('/codeverify/')


    if request.POST:
        amount = request.POST.get('amount')
        print(amount)
        try:
            print("inside wallet try")
            mywallet = Wallet.objects.get(user=currentuser)
            mywallet.amount = mywallet.amount+int(amount)
            mywallet.save()
        except:
            print("inside wallet except")
            mywallet = Wallet()
            mywallet.user = currentuser
            mywallet.amount = amount
            mywallet.save()

        #mywallet.amount += amount
        #mywallet.save()
        message = {'message':"Successfully added",'amount':mywallet.amount}
        return JsonResponse(message)
    try:
        balance = Wallet.objects.get(user=currentuser)
    except:
        balance = None

    try:
        if currentuser.is_seller:
            transactions = Transactions.objects.filter(user=currentuser)
            print(transactions)
        else:
            user = format(request.user)
            transactions = Transactions.objects.filter(bid_detail__bidder_name=user)
    except:
        print(traceback.format_exc())
        transactions = None

    return render(request,'scrapapp/wallet.html',{'user':currentuser,'balance':balance,'transactions':transactions})



def statistics(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/home/")
    currentuser = My_User(request.user)
    if currentuser.is_seller:
        return HttpResponseRedirect("/home/")
    if not currentuser.is_active:
        return HttpResponseRedirect('/codeverify/')

    ads = Ads.objects.filter(is_bidded=True)

    if request.POST:
        req_id = request.POST.get('id')
        try:
            bid_obj = Bid_Detail.objects.get(ad__id=req_id)
            print(bid_obj)
            status = "Bid completed"
            obj = {"low":format(bid_obj.ad.price),"high":format(bid_obj.amount),"status":status}
        except:
            bid_obj = Bid.objects.get(ad_id__id=req_id)
            print(bid_obj)
            status = "Bid in progress"
            obj = {"low":format(bid_obj.ad_id.price),"high":format(bid_obj.bid_amount),"status":status}

        print(obj)
        return JsonResponse(obj, safe=False)

    return render(request,'scrapapp/dealer_stats.html',{'ads':ads})




def test(request):

    pname = request.POST.get('product')
    print(pname)
    product = Product.objects.filter(id=pname)
    print(product)
    data = serializers.serialize('json', product)
    print(data)
    return JsonResponse(data,safe=False)


def profit(request):
    user = My_User(request.user)
    return render(request,'scrap/dealer_stats.html',{})
