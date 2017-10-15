#-*- coding:utf-8 -*-
from rest_framework import serializers

from coupon.models import *

class LoginSerializer(serializers.ModelSerializer):
    username  = serializers.CharField(required=True, max_length=1024)
    password = serializers.CharField(required=True, max_length=1024)
    token = serializers.UUIDField()
    class Meta:
        model = UserList
        fields = ('id', 'username', 'password', 'token')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.HiddenField(default=True)
    departmentname = serializers.ReadOnlyField(source='departmentid.departmentname')
    class Meta:
        model = UserList
        fields = ('id','username','password','name','sex','email','phone','departmentid','departmentname','leaderid')


class UserInfoSerializer(serializers.ModelSerializer):
    departmentname = serializers.ReadOnlyField(source='departmentid.departmentname')
    class Meta:
        model = UserList
        fields = ('id','name','sex','duty','phone','email','departmentid','departmentname','status')

class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id','departmentname','leaderid','stage')


class CouponSerializer(serializers.ModelSerializer):
    recordername = serializers.ReadOnlyField(source = 'recorderid.name')
    departmentname = serializers.ReadOnlyField(source = 'recorderid.departmentid.departmentname')
    phone = serializers.ReadOnlyField(source = 'recorderid.phone')
    class Meta:
        model = CouponVerify
        fields = ('id','couponname','content','starttime','endtime','recordtime','account','recorderid','phone','recordername','departmentname','checkerlist','checkstatuslist','checktimelist','status','advice','amount','coreid','comment')



class GradeInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ('id','gradeindex','gradename','productname','gradeplace','createtime') 

class GradePlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ('gradeplace',)

class CouponInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ('id','discounttype','discountnumber','account','studentid','registrationplace','gradeindex','source','extra')

class CouponRegistrationplaceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Coupon
        fields = ('registrationplace',)


class IDInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = ID
        fields = ('id','coreid','ids')



