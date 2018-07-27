'''Test api endpoints'''
import unittest
import json
from app import create_app


class api_test_case(unittest.TestCase):
    def setUp(self):
        self.app = create_app(configName="testing")
        self.client = self.app.test_client
        self.user_information = json.dumps({
            "content-type": "application/json",
            "username": "jane doe", "password":"12345",
            "email":"janedoe@gmail.com"}
                                          )
        self.entry_information = json.dumps({
            "contenttype":"application/json",
            "title":"sample1", "content":"sample1 sample1 sample1 sample1"}
                                           )

    def test_a_login(self):
        res = self.client().post("/api/v2/auth/login", headers={
            "content-type":"application/json",
            "Authorization":"Basic amFuZSBkb2U6MTIzNDU="}
                                )
        self.assertEqual(res.status_code,200)

    def test_a_login_wrong(self):
        res = self.client().post("/api/v2/auth/login", headers={
            "content-type":"application/json",
            "Authorization":"Basic amFuZSBkb2U3MTIzNDU="}
                                )
        self.asserNotEqual(res.status_code,200)

    def test_signup(self):
        
        res=self.client().post("/api/v2/auth/signup",data=self.user_information)
        self.assertEqual(res.status_code,201)

    def test_get_entries(self):
        resp_token = self.client().post("/api/v2/auth/login", headers={
            "content-type":"application/json",
            "Authorization":"Basic amFuZSBkb2U6MTIzNDU="})
        result = json.loads(resp_token.data.decode())
        res=self.client().get("/api/v2/entries", headers={"access_token":result["token"]} )
        self.assertEqual(res.status_code,200)

    def test_get_single_entry(self):
        resp_token = self.client().post("/api/v2/auth/login", headers={
            "content-type":"application/json",
            "Authorization":"Basic amFuZSBkb2U6MTIzNDU="})
        result = json.loads(resp_token.data.decode())
        res=self.client().get("/api/v2/entries/1", headers={"access_token":result["token"]})
        self.assertEqual(res.status_code,200)

    def test_add_entry(self):
       res=self.client().post("/api/v2/entries", data =self.entry_information)
       self.assertEqual(res.status_code,201)

    def test_modify_entry(self):
       res=self.client().put("/api/v2/entries/2",data=self.entry_information)
       self.assertEqual(res.status_code,200)

if __name__ == "__main__":
    unittest.main()
