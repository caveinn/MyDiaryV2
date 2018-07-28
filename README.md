This is an online diary where users can pen down their thoughts


[![Build Status](https://travis-ci.org/caveinn/MyDiaryV2.svg?branch=develop)](https://travis-ci.org/caveinn/MyDiaryV2) 
[![Coverage Status](https://coveralls.io/repos/github/caveinn/MyDiaryV2/badge.svg?branch=ch-refactor-to-tests-159381535)](https://coveralls.io/github/caveinn/MyDiaryV2?branch=ch-refactor-to-tests-159381535)
[![Maintainability](https://api.codeclimate.com/v1/badges/7bfa0b3c076b50e59903/maintainability)](https://codeclimate.com/github/caveinn/MyDiaryV2/maintainability) 

Prerequisites to run this app:  
   1. have postgres installed in your system running on localhost

To run this project you should follow the following steps:  

1. Cretate  a virual enviroment with the command  
`$ virtualenv -p python3 venv`  

1. Activate the venv with the command     
`$ source venv/bin/activate`


1. Install git  
1. clone this repo  
`$ git clone "https://github.com/caveinn/MyDiaryV2.git"` 
  
1. cd into the folder MyDiaryV2
1. export required enviroments  
	`$ export APP_SETTINGS="development"`  
	`$ export SECRET="a secret string of your choosing"`
1. install requirements      
`$ pip install -r requirements.txt`

1. now we are ready to run. 
	1. for tests run  
	`$ python test_Api.py`   
	1. for the application run  
	`$ python run.py`  

If you ran the aplication you can test the various api end points using postman. The appi endpoints are  

|Endpoint|functionality|contraints(requirements)|
|-------|-------------|----------|
|post /api/v2/auth/login | login |requires authentication |
|get /api/v2/entries| get all the entries| pass a token |
|get /api/v2/entries/<entryid>|return a single entry| entry id, pass token|
|post /api/v2/entries | create a new entry| entry data, pass token|
|put  /api/v12/entries/<entryid> |update an entry| entry id & new entry data, pass token| 
|post /api/v2/auth/signup|create a user|user information|



