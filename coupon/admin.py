from django.contrib import admin

from coupon.models import *
# Register your models here.

admin.site.register(Department)
admin.site.register(Student)
admin.site.register(UserList)
admin.site.register(CouponVerify)
admin.site.register(Coupon)
admin.site.register(Grade)

