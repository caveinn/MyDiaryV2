'''Test api endpoints'''
import unittest
import json
from app import create_app
from app.models import Db


class api_test_case(unittest.TestCase):
    def setUp(self):
        self.db_obj = Db()
        self.db_obj.create_tables()
        self.app = create_app(configName="testing")
        self.client = self.app.test_client
        self.user_information = json.dumps({
            "username": "jane doe", "password":"12345",
            "email":"janedoe@gmail.com"}
                                   )
        self.entry_information = json.dumps({
            'content-type': "application/json",
            "title":"sample1", "content":"sample1 sample1 sample1 sample1"})
        #create user to test various endpoints
        res1 = self.client().post("/api/v2/auth/signup",data=self.user_information,content_type = 'application/json')
        #get token for various  
        resp_token = self.client().post("/api/v2/auth/login", data = self.user_information,content_type = 'application/json')
        result = json.loads(resp_token.data.decode())  
        self.token= result["token"]
        #create entry to test
        res2 = self.client().post("/api/v2/entries", data =self.entry_information, 
            headers={"access_token":self.token}, content_type="application/json")
       

    def tearDown(self):
        self.db_obj.drop_all()

    def test_a_login(self):
        res = self.client().post("/api/v2/auth/login", data = self.user_information, content_type = "application/json"
                                )
        self.assertEqual(res.status_code,200)

    def test_a_login_wrong(self):
        res = self.client().post("/api/v2/auth/login", headers={
            "Content-Type":"application/json",
            "Authorization":"Basic amFuZSBkb2U3MTIzNDU="}
                                )
        self.assertNotEqual(res.status_code,200)

    def test_signup(self):
        res=self.client().post("/api/v2/auth/signup",data=json.dumps({"username":"kevin", "password":"kevin", "email":"kevin@gmail.com"}), 
            content_type = 'application/json')
        self.assertEqual(res.status_code,201)

    def test_get_entries(self):
        
        res=self.client().get("/api/v2/entries", headers={"access_token":self.token} )
        self.assertEqual(res.status_code,200)

    def test_get_single_entry(self):
        res=self.client().get("/api/v2/entries/1", headers={"access_token":self.token}, content_type="application/json")
        self.assertEqual(res.status_code,200)    

    def test_modify_entry(self):
        res=self.client().put("/api/v2/entries/1",data=self.entry_information,
            headers= {"access_token":self.token},
            content_type="application/json")
        self.assertEqual(res.status_code,200)

if __name__ == "__main__":
    unittest.main()
