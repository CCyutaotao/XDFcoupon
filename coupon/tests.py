#-*- coding:utf-8 -*-
from django.test import TestCase
from django.test import Client

# Create your tests here.
class LoginViewSetUnitTest(TestCase):
	
	target_api= '/coupon/login/'

	def test_login_authentication_api_post_with_no_info(self):
		response = self.client.post(target_api, {})
		print response.content
		self.assertEqual(response.status_code, 400)

	def test_login_authentication_api_post_with_username_only(self):
		response = self.client.post(target_api, {"username":"yutaotao"})
		print response.content
		self.assertEqual(response.status_code, 400)

	def test_login_authentication_api_post_with_username_nonexistent(self):
		response = self.client.post(target_api, {"username":"nonexistent", "password":"nonexistent"})
		print response.content
		self.assertEqual(response.status_code, 400)

	def test_login_authentication_api_post_with_real_username_and_password(self):
		response = self.client.post(target_api, {"username":"yutaotao", "password":"user123456"})
		print response.content
		self.assertEqual(response.status_code, 200)



class UserCreateUnitTest(TestCase):
	
	target_api = '/coupon/users/usercreate/'

	def test_user_create_api_post_with_no_info(self):
		response = self.client.post(target_api, {})
		print response.content
		self.assertEqual(response.status_code, 400)
	
	def test_user_create_api_post_with_all_required_info(self):
		response = self.client.post(target_api, 	
			{"username":"testuser","password":"123456","name":u"测试用户","email":"2622@qq.com",	"sex":u"男","phone":"12345678900","departmentid":6,"leaderid":2}	
		)
		print response.content
		self.assertEqual(response.status_code, 200)

	def test_user_create_api_post_with_all_required_info_but_authentication_token(self):
		response = self.client.post(target_api, 
			{"couponname":"样例","content":"样例批件2","starttime":"2015-1-1 11:11:11","endtime":"2016-1-1 11:11:11","account":"200","status":"0"
		})
		print response.content
		self.assertEqual(response.status_code, 200)



class UserStatusCheckListUnitTest(TestCase):

	target_api = '/coupon/users/userstatus/list/'

	def test_user_info_valid_or_not_for_leader_to_confirm_api_get_with_no_leader_authentication(self):
		response  = self.client.get(target_api)
		print response.content
		self.assertEqual(response.status_code, 401)

	def test_user_info_valid_or_not_for_leader_to_confirm_api_get_with_authentication(self):
		response = self.client.get(target_api, Authorization = "Token a20683bf8da95778abb8a1424b0a51d5af43a190")
		print response.content
		self.assertEqual(response.status_code, 200)

class UserStatusUpdateUnitTest(TestCase):

	target_api = '/coupon/users/userstatus/update/{}'

	def test_user_info_not_valid_to_yes_for_leader_api_update_with_data(self):
		response = self.client.update(target_api.format('27/'), {"status": 1})
		print response.content
		self.assertEqual(response.status_code, 200)

	def test_user_info_not_valid_to_yes_for_leader_api_update_with_no_data(self):
		response = self.client.update(target_api.format('27'), {"status": 1})
		print response.content
		self.assertEqual(response.status_code, 200)


class UserInfoListUnitTest(TestCase):
	
	target_api = '/coupon/users/userinfo/list/{}'

	def test_user_info_list_api_get(self):
		response = self.client.update(target_api.format(''))
		print response.content
		self.assertEqual(response.status, 200)

	def test_user_personal_info_list_api_get(self):
		response = self.client.get(target_api.foramt('?id=7'))
		print response.content
		self.assertEqual(response.status_code, 200)


class UserUpdateUnitTest(TestCase):

	target_api = '/coupon/users/userinfo/update/{}'

	def test_user_personal_info_api_update_with_auth_only(self):
		response = self.client.update(target_api.format('?id=7'),{ }, Authorization = "Token a20683bf8da95778abb8a1424b 0a51d5af43a190")	
		print response.content
		self.assertEqual(response.status_code, 200)

	def test_user_personal_info_api_update_with_auth_and_data(self):
		response = self.client.update(target_api.format('?id=7'), {"status":1}, Authorization = "Token a20683bf8da95778abb8a1424b0a51d5af43a190")
		print response.content
		self.assertEqual(response.status_code, 200) 


class DepartmentListUnitTest(TestCase):

	target_api = '/coupon/department/list/{}'

	def test_department_info_api_get(self):
		response = self.client.get(target_api.format(''))
		print response.content
		self.assertEqual(response.status_code, 200)


	def test_department_info_api_get_filter_with_depaetmentid(self):
		response = self.client.get(taget_api.format('?id=2'))
		print response.content
		self.assertEqual(response.status_code, 200)


	def test_department_info_api_get_filter_with_departmentname(self):
		response = self.client.get(taget_api.format('?departmentname=""'))
		print response.content
		self.assertEqual(response.status_code, 200)


class DepartmentCreateUnitTest(TestCase):

	target_api = '/coupon/department/create/'

	def test_department_create_api_post_with_no_auth(self):
		response = self.client.post(target_api, {"departmentname":"某部门"})
		print response.content
		self.assertEqual(response.status_code, 200)

	def test_department_create_api_post_with_auth(self):
		response = self.client.post(target_api, {"departmentname":"某部门"},  Authorization = "Token a20683bf8da95778abb8a1424b 0a51d5af43a190")
		print response.content
		self.assertEqual(response.status_code, 200)


class CouponCreateUnitTest(TestCase):

	target_api = '/coupon/couponinfo/create/'

	def test_coupon_create_api_post_with_no_auth_or_data(self):
		response = self.client.post(target_api, {},  Authorization = "Token a20683bf8da95778abb8a1424b 0a51d5af43a190")
		print rsponse.content
		self.assertEqual(response.status_code, 200)

	def test_coupon_create_api_post_with_data_and_no_auth(self):
		response = self.client.post(target_api, 
			{"couponname":"样例","content":"样例批件2","starttime":"2015-1-1 11:11:11","endtime":"2016-1-1 11:11:11","account":"200","status":0,"amount":200},
		)


class RecorderCouponFollowUnitTest(TestCase):

	target_api = '/coupon/couponinfo/recorder/list/'

	def test_coupon_follow_for_recorder_api_get_with_no_auth(self):
		response = self.client.get(target_api)
		print response.content
		self.assertEqual(response.status_code, 200)

	def test_coupon_follow_for_recorder_api_get_with_auth(self):
		response = self.client.get(target_api, Authorization = "Token a20683bf8da95778abb8a1424b 0a51d5af43a190")
		print response.content
		self.assertEqual(response.status_code, 200)


class LeaderCouponFollowListUnitTest(TestCase):

	target_api = '/coupon/couponinfo/leader/list/'

	def test_coupon_follow_for_leader_api_get_with_no_auth(self):
		response = self.client.get(target_api)
		print response.content
		self.assertEqual(response.status_code, 200)

	def test_coupon_follow_for_leader_api_get_with_auth(self):
		response = self.client.get(target_api)
		print response.content
		self.assertEqual(response.status_code, 200)


class CouponCheckUpdateUnitTest(TestCase):

	target_api = '/coupon/couponinfo/update/'

	def test_coupon_info_api_update_with_no_auth_or_data(self):
		response = self.client.patch(target_api)
		print response.content
		self.assertEqual(response.status_code, 400)

	def test_coupon_info_api_update_with_auth_and_data(self):
		response = self.client.patch(target_api, {"status":1}, Authorization = "Token a20683bf8da95778abb8a1424b 0a51d5af43a190")
		print response.content
		self.assertEqual(response.status_code, 200)

	def test_coupon_info_api_update_with_data_but_no_auth(self):
		response = self.client.patch(target_api, {"status":1})
		print response.content
		self.assertEqual(response.status_code, 200)
