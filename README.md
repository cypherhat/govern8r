virtualenv -p /Library/Frameworks/Python.framework/Versions/3.5/bin/python3 govern8rClient
virtualenv -p /Library/Frameworks/Python.framework/Versions/3.5/bin/python3 govern8rService
in directory govern8rService:

	source bin/activate
	sudo pip install flask
	sudo pip install pybitid
	sudo pip install blockcypher
	sudo pip install pymongo
	sudo pip install certifi
	git clone https://github.com/eliben/pycparser.git
		- in pycparser, sudo python ./setup.py install
	git clone https://github.com/boto/botocore.git
		- in botocore-develop, sudo python ./setup.py install
	sudo pip install boto3

	git clone https://github.com/LaurentMT/pybitid_demo.git