# -*- coding:utf-8 -*- 

from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^coupon/',include('coupon.couponURLS'),name="批件"),
    url(r'^download/',include('folder.downloadURLS'),name="下载"),
    url(r'^$','coupon.web_views.userlogin'),
    url(r'^webcouponlist/$', 'coupon.web_views.couponlist'),
    url(r'^docs/', include('rest_framework_docs.urls')),
]

