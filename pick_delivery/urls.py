from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

import order.views
import sender.views

from .views import *

router = DefaultRouter()
router.register(r'orders', order.views.OrderViewSet, base_name='order')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^email_verified/', TemplateView.as_view(template_name='email_verified.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^order_completed /', order.views.order_completed),
    url(r'^order_confirm/(?P<id>\d+)/(?P<key>\w+)/$', order.views.confirm_order),
    url(r'^register_sender/$', sender.views.register_sender),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),    
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^rest-auth/twitter/$', TwitterLogin.as_view(), name='twitter_login'),    
    url(r'^accounts/', include('allauth.urls')),    
]
