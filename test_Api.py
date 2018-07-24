import unittest

class apiTestCase(unittest.TestCase):
	def setUp(slef):
		self.app=createApp(configName="testing")
		self.client=self.app.test_client

	def testLogin(self):
		res=self.client().post('api/v2/auth/login'hearder={
			'content-type':'application/json','authorizatin':'Basic amFuZSBkb2U6MTIzNA=='
			})
		self.assertEqual(res.status_code,200)

	def testSignUp()