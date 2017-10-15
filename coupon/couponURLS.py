from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from coupon import views


## API URL PATTERNS
urlpatterns = format_suffix_patterns([

        url(r'login/$', views.LoginViewSet.as_view()),
        url(r'department/list/$',views.DepartmentList.as_view()),
        url(r'department/create/$',views.DepartmentCreate.as_view()),
        url(r'users/usercreate/$',views.UserCreate.as_view()),
        url(r'users/userstatus/list/$',views.UserStatusCheckList.as_view()),
        url(r'users/userstatus/update/(?P<pk>[0-9]+)/$',views.UserStatusUpdate.as_view()),
        url(r'users/userinfo/list/$',views.UserInfo.as_view()),
        url(r'users/userinfo/staff/list/$',views.StaffInfo.as_view()),
	url(r'users/password/update/$',views.UserPasswordUpdate.as_view()),
        url(r'users/userinfo/update/(?P<pk>[0-9]+)/$',views.UserUpdate.as_view()),
        url(r'couponinfo/create/$',views.CouponCreate.as_view()),
        url(r'couponinfo/list/$',views.CouponList.as_view()),
        url(r'couponinfo/update/(?P<pk>[0-9]+)/$',views.CouponCheck.as_view()),
        url(r'couponinfo/recorder/list/$',views.RecorderCouponFollow.as_view()),
        url(r'couponinfo/leader/list/$',views.LeaderCouponFollow.as_view()),
        url(r'couponinfo/usage/$',views.CouponExcelDetail.as_view()),
	url(r'excel/gradeinfo/$',views.GradeInput.as_view()),
        url(r'excel/couponinfo/$',views.CouponInput.as_view()),
        url(r'excel/idinfo/$',views.IDInput.as_view()),
        url(r'excel/gradeinfo/gradeplace/list/$',views.GradePlaceList.as_view()),
        url(r'excel/coupon/registrationsplace/list/$',views.RegistratinosplaceList.as_view()),
        url(r'excel/output/couponusage/$',views.ExcelOutput.as_view()),
        url(r'docx/output/$',views.DocxOutput.as_view()),
	url(r'filter/excel/gradeinfo/list/$',views.GradeListFilter.as_view()),
        url(r'filter/excel/couponinfo/list/$',views.StudentGradeRelatedFilterList.as_view()),


]) 


