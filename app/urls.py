"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from wmposts.views import index, submit, singlepost, upvote, justin, random
from wmuser.views import signup, signin, signout, account_holdings, changePassword, profileComments, profileSettings, profileUpvotes, profileMyPosts, profile
from wmbitcoin.views import bitcointest, deposit,  CallBack, comment_upvote, nested_comment_upvote#withdraw,
from django.views.generic.base import RedirectView

urlpatterns = [
	url(r'^$', index),
    url(r'^justin/', justin),
    url(r'^random/', random),
    url(r'^submit/', submit),
    url(r'^signup/', signup),
    url(r'^signin/', signin),
    url(r'^signout/', signout),
    url(r"^(\d+)/$", singlepost),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^btc/', account_holdings),
    url(r'^test/', bitcointest),
    url(r'^btcdeposit/', deposit),
    url(r'^btcwithdraw/', withdraw),
    url(r'^profile/bitcoins', deposit),
    url(r'^profile/settings', profileSettings),
    url(r'^profile/upvotes', profileUpvotes),
    url(r'^profile/posts', profileMyPosts),
    url(r'^profile/$', profile),
    url(r'^changepass/onetimesecret/', changePassword),
    url(r'^profile/comments', profileComments),
    # Django_Facebook SETUP
    url(r'^accounts/', include('allauth.urls')),
    # Upvote/Ajax GET URL
    url(r'^upvote/$', upvote),
    url(r'^comment_upvote/$', comment_upvote),
    url(r'^nested_comment_upvote/$', nested_comment_upvote),
    # Coinbase API Callback URL
    url(r'^callback/secret=ferraripojatlolxd/$', CallBack), 
    
    

 #  url(r'^.*$', RedirectView.as_view(url='wrongurl', permanent=False), name='wrong'), uudelleen ohjaa jos vaara url, toimii huonosti ?
   
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #<--
# !!!!!!!   Django does not serve MEDIA_ROOT by default. That would be dangerous in production environment. 
#But in development stage, we could cut short. Pay attention to the last line.
#That line enables Django to serve files from MEDIA_URL. This works only in developement stage.


#Users would then be able to register by visiting the URL /accounts/register/, login (once activated) at /accounts/login/, etc.
