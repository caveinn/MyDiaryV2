import unittest
import json

class apiTestCase(unittest.TestCase):
	def setUp(slef):
		self.app=createApp(configName="testing")
		self.client=self.app.test_client
		self.userInformation=json.dumps({"content-type":"application/json","name":"jane doe", "password":"12345", "email":"janedoe@gmail.com"})

	def testLogin(self):
		res=self.client().post("api/v2/auth/login",hearder={
			"content-type":"application/json","authorizatin":"Basic amFuZSBkb2U6MTIzNA=="
			})
		self.assertEqual(res.status_code,200)

	def testSignUp(self):
		res=self.client().post("api/v2/auth/signup",data=self.userInformation)
		self.assertEqual(res.status_code,201)

	
