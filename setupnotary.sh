#!/bin/bash

# one time command to update python in  MAC env.
#ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
#brew install python
#sudo eas_install virtualenv
#sudo easy_install pip

# start to download all the repos
git clone https://github.com/boto/botocore.git
git clone https://github.com/rajumariappan/govern8r.git
git clone https://github.com/rajumariappan/govern8rClient.git
git clone https://github.com/rajumariappan/govern8rService.git
git clone https://github.com/rajumariappan/govern8rLib.git
git clone https://github.com/cypherhat/python-bitcoinlib.git


virtualenv -p /usr/bin/python govern8rClient
virtualenv -p /usr/bin/python govern8rService

source govern8rService/bin/activate
pip install flask
pip install flask-api
pip install pybitid
pip install blockcypher
pip install certifi
pip install configparser
pip install ecdsa
pip install pycrypto
pip install simple-crypt

cd botocore
python setup.py install
cd ..

pip install boto3
pip install awscli

cd python-bitcoinlib
python setup.py install
cd ..     
         
cd govern8r/govern8rLib
python setup.py install 
cd ../..     

deactivate
    
    
source govern8rClient/bin/activate
pip install requests
pip install ecdsa
pip install pycrypto
pip install configparser
pip install simple-crypt
    
cd python-bitcoinlib
python setup.py install
cd ..

cd govern8r/govern8rLib
python setup.py install
cd ../..

deactivate
