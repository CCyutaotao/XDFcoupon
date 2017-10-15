# -*- coding:utf-8 -*-
from django.conf.urls import url, include, patterns
from . import views


urlpatterns = [
	url(r'excel/(?P<filename>.{1,500})/', views.excel_download),
	url(r'docx/(?P<filename>.{1,500})/', views.docx_download),
]
