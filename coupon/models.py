# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

from django.utils import timezone

# Create your models here.
class Department(models.Model):
        DEPARTMENT_DUTIES = (
                (u'校长部',u'校长部'),
                (u'市场部',u'市场部'),
                (u'客服部',u'客服部'),
                (u'国内部',u'国内部'),
                (u'国外部',u'国外部'),
                (u'泡泡少儿部',u'泡泡少儿部'),
                (u'优能一对一部',u'优能一对一部'),
                (u'优能精品班部',u'优能精品班部'),
                (u'国际游学部',u'国际游学部'),
                (u'小语种部',u'小语种部'),
                (u'教学部',u'教学部'),

        )
        departmentname = models.TextField(max_length=200)
        leaderid = models.IntegerField()
        stage = models.CharField(max_length=20,choices=DEPARTMENT_DUTIES)
        class Meta:
                ordering = ['-id']


        def __unicode__(self):
                return self.departmentname


class Student(models.Model):
        numbers = models.CharField(max_length=20,unique=True)
        name = models.CharField(max_length=20,default=u'匿名')
        extra = models.TextField()

        class Meta:
                ordering = ['-id']

        def __unicode__(self):
                return self.numbers


class UserList(User):
        DUTY_CHOICES = (
                (u'员工',u'员工'),
                (u'部门总监',u'部门总监'),
                (u'市场总监',u'市场总监'),
                (u'客服总监',u'客服总监'),
                (u'校长',u'校长'),
        )
        SEX_CHOICES =(
                (u'男',u'男'),
                (u'女',u'女'),
        )
        lastlogin = models.DateTimeField(default=timezone.now)
        status = models.BooleanField(default=0)
        duty = models.CharField(max_length=20,choices=DUTY_CHOICES,default=u'普通职员')
        name = models.CharField(max_length=20)
        sex = models.CharField(max_length=10,choices=SEX_CHOICES)
        phone = models.CharField(max_length=11,unique=True)
        departmentid = models.ForeignKey(Department,editable=True,on_delete=models.CASCADE)
        leaderid = models.IntegerField()
        extra = models.TextField(blank=True)

        class Meta:
                ordering = ['-id']

        def __unicode__(self):
                return self.departmentid.departmentname


class CouponVerify(models.Model):
        COUPONVERIFY_STATUS = (
                ('0',u'待审核'),
                ('1',u'有效'),
		('2',u'失败')
        )
        couponname = models.CharField(max_length=200, unique=True)     
        content = models.TextField(max_length=2000)
        starttime = models.DateTimeField()
        endtime = models.DateTimeField()
        recordtime = models.DateTimeField(auto_now_add=True)
        account = models.DecimalField(max_digits=10,decimal_places=2)
        recorderid = models.ForeignKey(UserList,editable=False,on_delete=models.CASCADE)
        checkerlist = models.CharField(max_length=200,blank=True)
        checkstatuslist = models.CharField(max_length=200,blank=True)
        checktimelist = models.CharField(max_length=200,blank=True)
        status = models.CharField(max_length=20,choices=COUPONVERIFY_STATUS,default=0)
        advice = models.TextField(blank=True)
	amount = models.IntegerField(default=1)	
	coreid = models.CharField(max_length=20,blank=True)	
 	comment = models.CharField(max_length=200,default=u'无' )
	class Meta:
		ordering = ['-id']

	def __unicode__(self):
		return self.couponname


class Coupon(models.Model):
        discounttype = models.CharField(max_length=100)
        discountnumber = models.CharField(max_length=100)
        account = models.DecimalField(max_digits=10,decimal_places=2,blank=True)
        studentid = models.CharField(max_length=20)
        registrationplace = models.CharField(max_length=100)
        gradeindex = models.CharField(max_length=20)
        source = models.CharField(max_length=20)
        extra = models.TextField(blank=True)

        class Meta:
                ordering = ['discountnumber']
		unique_together = ['discountnumber', 'studentid', 'gradeindex']

        def __unicode__(self):
                return self.discountnumber


		

class Grade(models.Model):
      gradeindex = models.CharField(max_length=200,unique=True)
      gradename = models.CharField(max_length=200,blank=True)
      productname = models.CharField(max_length=200,blank=True)
      gradeplace = models.TextField(blank=True)   
      createtime = models.DateTimeField(auto_now_add=True) 
	
      class Meta:
                ordering = ['-gradeindex']
      def __unicode__(self):
        return u'%s %s' %(self.gradeindex,self.gradename)



class ID(models.Model):
    coreid = models.CharField(max_length=20,blank=True,default='0')
    ids = models.CharField(max_length=20,blank=True)

    class Meta:
        ordering = ['-coreid']
    def __unicode__(self):
        return self.coreid



