from django.conf.urls import url,include
from . import views
from django.contrib.auth import views as auth_views



app_name='scrapapp'
urlpatterns = [
    url(r'^home/$', views.home),
    url(r'^adminlogin/$', views.adminlogin),
    url(r'^validateuser/$',views.validate_user),
    url(r'^index/$', views.index),
    url(r'^dealerlogin/$',views.dealerlogin),
    url(r'^sellerlogin/$', views.sellerlogin),
    url(r'^dealerregister/$', views.dealerreg),
    url(r'^sellerregister/$', views.sellerreg),
    url(r'^ads/(?P<id>[0-9]+)/$', views.adsid),
    url(r'^cart/$',views.cart),
    url(r'^sellerlogin/bids/$',views.bids),
    url(r'^sellerlogin/bids/(?P<id>[0-9]+)/$',views.viewbids),
    url(r'^recentbids/$',views.recentbids),
    url(r'^deals/$',views.deals),
    url(r'^deals/(?P<id>[0-9]+)/$', views.dealsid),
    url(r'^codeverify/$',views.codeverify),
    url(r'^addtocart/$',views.addtocart),
    url(r'^acceptbid/$', views.acceptbid),
    url(r'^wallet/$', views.wallet),
    url(r'^stats/$', views.statistics),
    url(r'^logout/$',views.logout_view),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^test/$', views.test),

]