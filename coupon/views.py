# -*- coding:utf-8 -*-
from django.http import StreamingHttpResponse

from django.contrib.auth import authenticate,login,logout
from django.db.models import Count


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import filters,viewsets,generics   
from rest_framework import permissions
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter

from rest_framework.pagination import LimitOffsetPagination

from coupon.serializers import *

from coupon.models import *

import logging

logger = logging.getLogger('XDFcoupon.coupon.views')

class LoginViewSet(APIView):
    """
    登陆接口     
    """
    queryset = User.objects.all()
    serializer_class = AuthTokenSerializer
    permission_classes=()
    def post(self, request, *args, **kwargs):
		
                serializer = self.serializer_class(data=request.data)
                serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
                if UserList.objects.get(id=user.id).status == 0:
                        return Response({'detail':'Ask the manager to confirm your identity '})
                login(request,user)
                token, created = Token.objects.get_or_create(user=user)
                duty = UserList.objects.get(id = user.id).duty
                return Response({'userid':user.id, 'username':user.username, 'token': token.key,'duty':duty})  






class UserCreate(APIView):
    """
    注册接口
    """
    queryset = UserList.objects.all()
    serializer_class = UserSerializer
    permission_classes =  (
    )


    def post(self, request, *args, **kwargs):
            if len(UserList.objects.filter(username=request.data['username']))!=0:
                    return Response({'detail':'username exist'},status = status.HTTP_400_BAD_REQUEST)
            try:     
                    user = UserList()
                    user.username = request.data['username']
                    user.set_password(request.data['password'])
                    user.name = request.data['name']
                    user.sex = request.data['sex']
                    user.email = request.data['email']
                    user.phone = request.data['phone']
                    user.departmentid =Department.objects.get(id=request.data['departmentid'])
                    user.leaderid = request.data['leaderid']
                    user.is_active = True
                    user.is_staff = True
                    user.save()
                    return Response({'detail':"Success"})
            except Exception,e:
                    print e
                    return Response({'detail':'Failed'},status = status.HTTP_400_BAD_REQUEST)                        


class UserStatusCheckList(generics.ListAPIView):
    """
    返回 所有待审核的新注册用户  权限用户专用
    """

    serializer_class = UserSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )


    def list(self, request):
            queryset = UserList.objects.filter(status = 0).filter(departmentid = UserList.objects.get(id= request.user.id).departmentid)
            serializer = UserInfoSerializer(queryset, many = True)
            return Response(serializer.data)



class UserStatusUpdate(generics.UpdateAPIView):
    """
    待审核用户状态更新  允许登陆客户端
    """
    queryset = UserList.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )


class InValidUserDelete(generics.DestroyAPIView):
    """
    审核未通过用户删除 权限用户专用
    """
    queryset = UserList.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )


    def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            instance.delete()
            return Response({"detail":"success"}, status=status.HTTP_200_OK)




class UserInfo(generics.ListAPIView):

    """
    用户本人信息查看  限用户本人 
    """
    queryset =  UserList.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )


    def list(self, request):
            queryset = UserList.objects.filter(id = request.user.id)
            serializer = UserInfoSerializer(queryset, many =True)
            return Response(serializer.data)

class StaffInfo(generics.ListAPIView):
    """
    本部门员工信息查看  权限用户专用
    """
    queryset = UserList.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )


    def list(self, request):
            queryset = UserList.objects.filter(leaderid = request.user.id)
            serializer = UserInfoSerializer(queryset, many=True)
            return Response(serializer.data)



class UserUpdate(generics.UpdateAPIView):
    """
    用户本人信息更新
    """
    queryset = UserList.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (
	     permissions.IsAuthenticated,
    ) 
    filter_fields = ('id',)



class UserPasswordUpdate(APIView):
    """
    密码更改
    """
    def post(self, request, *args, **kwargs):
            oldpwd = request.data['opwd']
            newpwd = request.data['npwd']
	    user = authenticate(username = request.user.username, password = oldpwd)
            if  user is None :
                    return Response({"detail": u"旧密码错误"}, status = status.HTTP_200_OK)
            else : 
                    user.set_password(newpwd)
		    user.save()
                    return Response({"detail": u"修改密码成功"}, status = status.HTTP_200_OK)



class DepartmentList(generics.ListAPIView):
    """
    部门列表    

    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (
		permissions.IsAuthenticated,
    )


    def list(self, request):
            queryset = Department.objects.all()
            serializer = DepartmentSerializer(queryset, many=True)
            for i in range(0,len(serializer.data)):
                    a = serializer.data[i]

                    leadername = UserList.objects.get(id= a['leaderid']).name 
                    a['leadername']=leadername
            return Response(serializer.data)


class DepartmentCreate(generics.CreateAPIView):
    """
    部门创建
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = (
    )


class CouponCreate(generics.CreateAPIView):
    """
    批件创建
    """
    queryset = CouponVerify.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (
            permissions.IsAuthenticated,
    )


    def perform_create(self,serializer):
            from datetime import datetime
            checkerlist= [int(self.request.user.id)]
            checkstatuslist = [1]
            checktimelist = [str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))]
            id = UserList.objects.get(id=self.request.user.id).leaderid
            while (id!=0 ):
                    checkerlist.append(int(id))
                    checkstatuslist.append(0)
                    id = UserList.objects.get(id=id).leaderid 
	    if CouponVerify.objects.filter(couponname = self.request.data["couponname"]): return Response({"detail":u'批件名重复'})
           
	    serializer.save(
                    recorderid = UserList.objects.get(id=self.request.user.id),
                    checkerlist = checkerlist,
                    checkstatuslist = checkstatuslist,
		    checktimelist = checktimelist,
            )

class CouponList(APIView):
    """
    合格批件列表
    """
    queryset = CouponVerify.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (
	permissions.IsAuthenticated,
    )


    def get(self, request):
            leaderlist = [17, 19, 20, 40, 51] 
            months= 24
            departmentids = [9,10,11,12,13,14,15,16] 
            for item in request.GET.items():
		    print item
                    if item[0] == 'months':
                        months = item[1]
                    if item[0] == 'departmentids':
			departmentids = item[1].split(',')
            from datetime import datetime, timedelta
            if request.user.id in leaderlist:
                couponlist = CouponVerify.objects.filter(status = 1).filter(recorderid__departmentid__in = departmentids).filter(starttime__gte = (datetime.now()- timedelta(30 * int(months) )))
            else:
                couponlist = CouponVerify.objects.filter(status = 1).filter(recorderid__departmentid = UserList.objects.get(id = request.user.id).departmentid).filter(starttime__gte = (datetime.now()- timedelta(30 * int(months) )))
            serializer = CouponSerializer(couponlist, many = True)
            return Response(serializer.data)




class RecorderCouponFollow(generics.ListAPIView):
    """
    发布者追踪批件信息
    """
    queryset = CouponVerify.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (
	 permissions.IsAuthenticated,
    ) 


    def list(self, request):
            queryset = CouponVerify.objects.filter(recorderid = request.user.id).order_by("-id")
            serializer = CouponSerializer(queryset, many = True)
            for i in range(0,len(serializer.data)):
                    a = serializer.data[i]
                    checkerlist = a['checkerlist']
                    checkstatuslist = a['checkstatuslist']
		    if checkstatuslist.count('0') == 0:
			a["uncheckedname"] = u'无'
                    else:
			uncheckedid=checkerlist.encode("utf-8").replace('[','').replace(']','').split(',')[0-checkstatuslist.count('0')]
                    	a['uncheckedname'] = UserList.objects.get(id = uncheckedid).name
            return Response(serializer.data)


class LeaderCouponFollow(generics.ListAPIView):
    """
    领导查看待审核批件
    """
    queryset = CouponVerify.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (
	permissions.IsAuthenticated,
    )


    def list(self, request):
            queryset = CouponVerify.objects.filter(checkerlist__contains=request.user.id).exclude(status=2)
            serializer = CouponSerializer(queryset, many = True)
            newdata = []
            for i in range(0,len(serializer.data)):
                    a= serializer.data[i]
                    checkerlist = a['checkerlist'].encode("utf-8").replace('[','').replace(']','').replace(' ','').split(',')                
                    checkstatuslist = a['checkstatuslist'].encode("utf-8").replace('[','').replace('\'','').replace(']','').replace(' ','').split(',')
                    if checkstatuslist[checkerlist.index(str(request.user.id))] == '0' and checkstatuslist[checkerlist.index(str(request.user.id)) - 1 ] == '1' :
                            newdata.append(a)
            return Response(newdata)



class CouponCheck(generics.UpdateAPIView):
    """
    批件内容状态更新
    """
    queryset = CouponVerify.objects.all()
    serializer_class = CouponSerializer
    permission_classes = (
	permissions.IsAuthenticated,
    )

class GradeInput(APIView):
    """
    班级上课地点录入

    """
    queryset = Grade.objects.all()
    serializer_class = GradeInputSerializer
    permission_classes = (
    )


    def post(self, request, *args, **kwargs):
            try :
                    dic = {}
                    for key, value in request.data.items():
                            dic[key] = 0
                            grade = Grade()
                            value = value.encode("utf-8").replace('[', '').replace(']', '').replace(' ','').split(',') 
                            grade.gradeindex = value[0]
                            grade.gradename = value[1].decode("unicode_escape")
                            grade.productname = value[2].decode("unicode_escape")
                            grade.gradeplace =  value[3].decode("unicode_escape")
                            grade.save()
                            dic[key] = 1
                    return Response(dic, status = status.HTTP_200_OK)
            except Exception, e:
                            print e
                            return Response(dic, status = status.HTTP_200_OK)





class CouponInput(APIView):
    """
    批件使用情况录入
    """
    queryset = Coupon.objects.all()
    serializer_class = CouponInputSerializer
    permission_classes = (
    )

    def post(self, request, *args, **kwargs):
            try:
                    dic = {}
                    import decimal
                    for key,value in request.data.items():
                            dic[key] = 0
                            coupon = Coupon()
                            value = value.encode("utf-8").replace('[','').replace(']','').replace(' ','').split(',')
                            coupon.discounttype = value[0].decode("unicode_escape")
                            coupon.discountnumber = value[1].encode("utf-8").replace('u','').replace('\'', '')
                            coupon.account = decimal.Decimal(value[2][2:-1]) 
                            coupon.studentid = value[3].encode("utf-8").replace('u','').replace('\'', '')
                            coupon.registrationplace = value[4].decode("unicode_escape").encode("utf-8").replace('u','').replace('\'', '')
                            coupon.gradeindex = value[5].decode("unicode_escape").encode("utf-8").replace('u','').replace('\'', '')
                     
                            coupon.source = value[6].decode("unicode_escape").encode("utf-8").replace('u','').replace('\'', '')
                            try:
			    	coupon.save()
			    except Exception, e:
				pass
                            dic[key] = 1
                    return Response(dic,status = status.HTTP_200_OK)
            except Exception, e:
                    print e
                    return Response(dic,status = status.HTTP_200_OK)




class IDInput(APIView):

    """
    批件小编号 录入
    """
    queryset = ID.objects.all()
    serializer_class = IDInputSerializer
    permission_classes = (
    )


    def post(self, request, *args, **kwargs):
            try:
                    dic = {}
                    for key, value in request.data.items():
                            dic[key] = 0
                            i = ID()
                            value = value.encode("utf-8").replace('[', '').replace(']','').replace(' ','').replace('u','').split(',')
                            i.ids = value[0].decode("unicode_escape")
                            i.save()
                            dic[key] = 1
                    return Response(dic, status = status.HTTP_200_OK)
            except Exception, e:
                    print e
                    return Response(dic, status = status.HTTP_200_OK)



class GradePlaceList(generics.ListAPIView):
    """
    班级上课地点  distinct列表 
    """
    queryset = Grade.objects.all()
    serializer_class =  GradePlaceSerializer
    permission_classes = (

    )


    def list(self, request):
            queryset = Grade.objects.values("gradeplace").order_by("gradeplace").distinct()
            serializer  = GradePlaceSerializer(queryset, many=True)
            return Response(serializer.data)


class GradeListFilter(generics.ListAPIView):
    """
    班级上课地点 按 班级编号 上课地点过滤 
    """

    queryset = Grade.objects.all()
    serializer_class = GradeInputSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
    )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('gradeindex', 'gradeplace',)


class RegistratinosplaceList(generics.ListAPIView):
    """
    报名点 distinct列表 
    """
    queryset = Coupon.objects.all()
    serializer_class = CouponRegistrationplaceSerializer
    permission_classes = (
    )
    pagination_class = LimitOffsetPagination


    def list(self, request):
            queryset = Coupon.objects.values("registrationplace").order_by("registrationplace").distinct()
            serializer = CouponRegistrationplaceSerializer(queryset, many=True)
            return Response(serializer.data)


class StudentGradeRelatedFilterList(generics.ListAPIView):
    """
    学生表过滤
    """
    queryset = Coupon.objects.all()
    serializer_class = CouponInputSerializer
    permission_classes = (
    )
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('discountnumber', 'registrationplace','gradeindex','studentid',)
    pagination_class = LimitOffsetPagination



class CouponExcelDetail(APIView):
    """
    优惠批件 各校区 使用情况 
    """
    def get(self, request):
            for item in  request.GET.items():
                    if item[0] == 'discountnumber':
                            discountnumber = item[1]
            couponusage = Coupon.objects.filter(discountnumber = discountnumber).order_by('discountnumber')
            couponusage_orderby_place = couponusage.values('registrationplace').annotate(count=Count('registrationplace'))
            return Response(couponusage_orderby_place)



class ExcelOutput(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        months = request.data.get('months', 6) 
        departmentids = request.data.get('departmentids', '9,10,11,12,13,14,15,16').split(',')
	from datetime import datetime, timedelta
        couponlist = CouponVerify.objects.filter(status = 1).filter(recorderid__departmentid__in = departmentids).filter(starttime__gte = (datetime.now()- timedelta(30 * int(months))))
        serializer = CouponSerializer(couponlist, many = True)
        for i in range(0,len(serializer.data)):
            a = serializer.data[i]
            discountnumber = a['coreid']
            a['couponusage'] = Coupon.objects.filter(discountnumber = discountnumber).values('studentid','registrationplace').distinct().values('registrationplace').order_by("registrationplace").annotate(count=Count('registrationplace'))
        from folder.excelwrite import excelwrite
	filepath = excelwrite(serializer.data, request.user.username)
        return Response({'path':filepath})



class DocxOutput(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
	couponname = request.data["couponname"]
	coupondetail = CouponVerify.objects.get(couponname = couponname)
	leadername = UserList.objects.get(id = int(UserList.objects.get(id = int(coupondetail.recorderid_id)).leaderid)).name
	serializer = CouponSerializer(coupondetail, many = False)
	dic = serializer.data
	dic["leadername"] = leadername
	
	from folder.docxwrite import docxwrite
        filepath = docxwrite(dic)
        return Response({'path':filepath})


