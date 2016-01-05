import notary
import os
print "deleting wallet file"
if os.path.isfile("notarywallet.data"):
     os.remove("notarywallet.data")
else:    ## Show an error ##
     print("Error: %s file not found" % "notarywallet.data")


result = notary.mainMethod(['register', '-email', 'rajumail@gmail.com','-password', 'test123'])
print result
if result == 500:
    print "500,possible duplication.Clean wallet before register."
elif result is None:
    print "Registration not successful"
else:
    print "calling confirm"
    confirm_result = notary.mainMethod(['confirm','-confirm_url', result,'-password', 'test123'])
    print confirm_result
    # if 200 means go ahead and notarize a file.
    if confirm_result == 200 :
        login_result = notary.mainMethod(['login', '-password', 'test123'])
        if login_result :
            transaction_id = notary.mainMethod(['notarize', '-file', 'testnotarizecontent.txt','-metadata','testmetadata.txt','-password', 'test123'])
            if transaction_id is not None :
                 transaction_status = notary.mainMethod(['notarystatus', "-transaction_id",transaction_id, '-password', 'test123'])
                 print transaction_status
            else :
                print "There is not transaction id returned"
        else :
            print "Login failed"
    else:
        print "Account confirmation failed"



notary.mainMethod([ '-h' ])
