# -*- coding:utf-8 -*-
from django.shortcuts import render,render_to_response
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login 

from coupon.models import *


def userlogin(request):
    print request.POST
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
	user = authenticate(username = username, password = password)
	allowedlist = [19,20,21,22,23,24,25,26,27,28,40]
        if user is not None and user.id in allowedlist:
                login(request, user)
                return HttpResponseRedirect('/webcouponlist/')
        else:
                return render(request,'Login.html',{"login":0})
    return render(request, 'Login.html')


def couponlist(request):

    if request.method == 'GET':
	try:
        	queryset = CouponVerify.objects.filter(status = 0).filter(checkerlist__contains=request.user.id)
        	idlist = []
       		for query in queryset:
            		checkerlist = query.checkerlist.encode("utf-8").replace('[','').replace(']','').replace(' ','').split(',')                
            		checkstatuslist = query.checkstatuslist.encode("utf-8").replace('[','').replace('\'','').replace(']','').replace(' ','').split(',')
            		if checkstatuslist[checkerlist.index(str(request.user.id))] == '0' and checkstatuslist[checkerlist.index(str(request.user.id)) - 1 ] == '1' :
                		idlist.append(query.id)
        	queryset = queryset.filter(id__in = idlist)
	except Exception, e:
		print e
		return HttpResponseRedirect('/')
        return render(request ,'XDF.html', locals())

    if request.method == 'POST':
        submitid = request.POST.get('submitid')
	print submitid
	query = CouponVerify.objects.get(id = submitid)
        query.checkstatuslist = query.checkstatuslist.replace('0', '1', 1)
	from datetime import datetime
	checktimelist ="%s" %(query.checktimelist[:-1]+","+str(datetime.now())+"]" )
	query.checktimelist = checktimelist
        query.save()
        return HttpResponseRedirect('/webcouponlist/')
