'''Test api endpoints'''
import unittest
import json
from app import create_app


class api_test_case(unittest.TestCase):
    def setUp(self):
        self.app = create_app(configName="testing")
        self.client = self.app.test_client
        self.user_information = json.dumps({"content-type": "application/json", "name": "jane doe", "password":"12345", "email":"janedoe@gmail.com"})
        self.entry_information = json.dumps({"cont-type":"application/json","title":"sample1", "content":"sample1 sample1 sample1 sample1"})

    def test_login(self):
        res = self.client().post("api/v2/auth/login", hearders={"content-type":"application/json","authorizatin":"Basic amFuZSBkb2U6MTIzNA=="})
        self.assertEqual(res.status_code,200)

    def test_signup(self):
       res=self.client().post("api/v2/auth/signup",data=self.userInformation)
       self.assertEqual(res.status_code,201)

    def test_get_entries(self):
       res=self.client().get("api/v2/entries")
       self.assertEqual(res.status_code,200)

    def test_get_single_entry(self):
       res=self.client().get("api/v2/entries/1")
       self.assertEqual(res.status_code,200)

    def test_add_entry(self):
       res=self.client().post("api/v2/entries", data =self.entryInformation)
       self.assertEqual(res.status_code,201)

    def test_modify_entry(self):
       res=self.client().put("/api/v2/entries/1",data=self.entryInformation)
       self.assertEqual(res.status_code,200)

if __name__ == "__main__":
    unittest.main()
