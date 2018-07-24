import unittest
import json
from app import createApp

class apiTestCase(unittest.TestCase):
	def setUp(self):
		self.app=createApp(configName="testing")
		self.client=self.app.test_client
		self.userInformation=json.dumps({"content-type":"application/json","name":"jane doe", "password":"12345", "email":"janedoe@gmail.com"})
		self.entryInformation=jsonn.dumps({"cont-type":"application/json","title":"sample1", "content":"sample1 sample1 sample1 sample1"})
	
	def testLogin(self):
		res=self.client().post("api/v2/auth/login",hearder={
			"content-type":"application/json","authorizatin":"Basic amFuZSBkb2U6MTIzNA=="
			})
		self.assertEqual(res.status_code,200)

	def testSignUp(self):
		res=self.client().post("api/v2/auth/signup",data=self.userInformation)
		self.assertEqual(res.status_code,201)

	def testGetEntries(self):
		res=self.client().get("api/v2/entries")
		self.assertEqual(res.status_code,200)

	def testGetSingleEntry(self):
		res=self.client().get("api/v2/entries/1")
		self.assertEqual(res.status_code,200)

	def testAddEntry(self):
		res=self.client().post("api/v2/entries", data =self.entryInformation)
		self.assertEqual(res.status_code,201)

	def testModifyEntry(self):
		res=self.client().put("/api/v2/entries/1",data=self.entryInformation)
		self.assertEqual(res.status_code,200)

if __name__=="__main__":
	unittest.main()