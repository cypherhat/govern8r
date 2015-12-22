# govern8r

This is the repo for the govern8r client and server.

## Environment setup

Install python3.5

Install virtualenv for both client and server:
```
virtualenv -p /Library/Frameworks/Python.framework/Versions/3.5/bin/python3 govern8rClient
virtualenv -p /Library/Frameworks/Python.framework/Versions/3.5/bin/python3 govern8rService
```

## Setup packages for services

in directory govern8rService:
```
	source bin/activate
	sudo pip install flask
	sudo pip install pybitid
	sudo pip install blockcypher
	sudo pip install pymongo
	sudo pip install certifi
```

I've had issues installing a few things due to SSL errors. When I installed pyopenssl, I had such an error. The failure was on the pycparser package. So, my resolution is to clone the repo and install manually.
```
	git clone https://github.com/eliben/pycparser.git
```
	
Change to the pycparser directory and:
```
sudo python ./setup.py install
```
	
Same deal with boto3 - the AWS APIs.
```
	git clone https://github.com/boto/botocore.git
```

Change to the botocore-develop directory
```
sudo python ./setup.py install
```

Now you can:
```
	sudo pip install boto3
```	

For the template to start from...
```
	git clone https://github.com/LaurentMT/pybitid_demo.git
```

## Setup packages for client


in directory govern8rClient:
```
	source bin/activate
	sudo pip install python-bitcoinlib
	sudo pip install requests
	sudo pip install certifi

```

've had issues installing a few things due to SSL errors. When I installed pyopenssl, I had such an error. The failure was on the pycparser package. So, my resolution is to clone the repo and install manually.
```
	git clone https://github.com/eliben/pycparser.git
```
	
Change to the pycparser directory and:
```
	sudo python ./setup.py install
	sudo pip install pyopenssl
```

