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
sudo pip install flask
sudo pip install flask-api
sudo pip install pybitid
sudo pip install blockcypher
sudo pip install certifi
sudo pip install configparser
sudo pip install ecdsa
sudo pip install pycrypto
sudo pip install simple-crypt

cd botocore
sudo python setup.py install
cd ..

sudo pip install boto3
sudo pip install awscli

cd python-bitcoinlib
sudo python setup.py install
cd ..     
         
cd govern8r/govern8rLib
sudo python setup.py install 
cd ../..     

deactivate
    
    
source govern8rClient/bin/activate
sudo pip install requests
sudo pip install ecdsa
sudo pip install pycrypto
sudo pip install configparser
sudo pip install simple-crypt
    
cd python-bitcoinlib
sudo python setup.py install
cd ..

cd govern8r/govern8rLib
sudo python setup.py install
cd ../..

deactivate
