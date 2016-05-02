"""pick_delivery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

import order.views
import sender.views


router = DefaultRouter()
router.register(r'orders', order.views.OrderViewSet, base_name='order')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', TemplateView.as_view(template_name='base.html')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^order_completed /', order.views.order_completed),
    url(r'^order_confirm/(?P<id>\d+)/(?P<key>\w+)/$', order.views.confirm_order),
    url(r'^register_sender/$', sender.views.register_sender),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),    
]
