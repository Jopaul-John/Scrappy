from django.contrib import admin
from django.contrib.auth.models import User


from .models import *

admin.site.register(UserProfile),
admin.site.register(Product),
admin.site.register(Ads),
admin.site.register(Bid),
admin.site.register(Bid_Detail),
admin.site.register(ContactUs),
admin.site.register(Cart),
admin.site.register(Wallet),
admin.site.register(Transactions),
admin.site.register(Expired_Ad),
admin.site.register(ProductProfit),
admin.site.register(Profit),