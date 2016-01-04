from flask import request, Response, json
from flask_api import FlaskAPI
from wallet import NotaryWallet
from services.account_service import AccountService
from services.notarization_service import NotarizationService
from message import SecureMessage
from bitcoinlib.signmessage import VerifyMessage
import hashlib

app = FlaskAPI(__name__)
wallet = NotaryWallet("foobar")
account_service = AccountService(wallet)
notarization_service = NotarizationService(wallet)
secure_message = SecureMessage(wallet)


def build_fingerprint():
    fingerprint = str(request.user_agent)+str(request.remote_addr)
    return fingerprint


def build_token(nonce):
    nonce_hash = hashlib.sha256(nonce).digest()
    fingerprint_hash = hashlib.sha256(build_fingerprint()).digest()
    token = hashlib.sha256(nonce_hash + fingerprint_hash).digest()
    return token.encode("hex")


def validate_token(nonce, token):
    check_token = build_token(nonce)
    return check_token == token


def authenticated(address):
    account_data = account_service.get_account_by_address(address)
    govern8r_token = request.cookies.get('govern8r_token')
    return validate_token(account_data['nonce'], govern8r_token)


def rotate_authentication_token(address):
    account_data = account_service.get_challenge(address)  ## rotate authentication token
    govern8r_token = build_token(account_data['nonce'])
    js = json.dumps({})
    authenticated_response = Response(js, status=200, mimetype='application/json')
    authenticated_response.set_cookie('govern8r_token', govern8r_token)
    return authenticated_response


@app.route("/govern8r/api/v1/pubkey", methods=['GET'])
def pubkey():
    """
    Return server public key. The key is encoded in hex and needs to be decoded
    from hex to be used by the encryption utility.
    """
    # request.method == 'GET'
    public_key = wallet.get_public_key()
    data = {
        'public_key': public_key.encode("hex")
    }
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route("/govern8r/api/v1/challenge/<address>", methods=['GET', 'PUT'])
def challenge(address):
    """
    Authentication
    Parameters
    ----------
    address : string
       The Bitcoin address of the client.
    """
    js = json.dumps({})
    bad_response = Response(js, status=500, mimetype='application/json')
    bad_response.set_cookie('govern8r_token', 'UNAUTHENTICATED')

    if request.method == 'GET':
        account_data = account_service.get_challenge(address)
        if account_data is None:
            return bad_response
        str_nonce = json.dumps({'nonce': account_data['nonce']})
        payload = secure_message.create_secure_payload(account_data['public_key'], str_nonce)
        good_response = Response(js, status=200, mimetype='application/json')
        good_response.data = json.dumps(payload)
        return good_response
    elif request.method == 'PUT':
        account_data = account_service.get_account_by_address(address)
        if account_data is None:
            return bad_response
        payload = request.data
        if secure_message.verify_secure_payload(address, payload):
            raw_message = secure_message.get_message_from_secure_payload(payload)
            message = json.loads(raw_message)
            if message['nonce'] == account_data['nonce']:
                govern8r_token = build_token(account_data['nonce'])
                good_response = Response(js, status=200, mimetype='application/json')
                good_response.set_cookie('govern8r_token', value=govern8r_token)
                return good_response
            else:
                bad_response.status_code = 401
                return bad_response
        else:
            bad_response.status_code = 401
            return bad_response
    return bad_response


@app.route("/govern8r/api/v1/account/<address>", methods=['GET', 'PUT'])
def account(address):
    """
    Account registration
    Parameters
    ----------
    address : string
       The Bitcoin address of the client.
    """

    good_response = Response(json.dumps({}), status=200, mimetype='application/json')
    bad_response = Response(json.dumps({}), status=500, mimetype='application/json')

    inbound_payload = request.data
    if secure_message.verify_secure_payload(address, inbound_payload):
        str_registration_data = secure_message.get_message_from_secure_payload(inbound_payload)
        registration_data = json.loads(str_registration_data)

        if request.method == 'PUT':
            if not account_service.create_account(address, registration_data):
                return bad_response
            else:
                return good_response
        elif request.method == 'GET' and authenticated(address):
            account_data = account_service.get_account_by_address(address)
            outbound_payload = secure_message.create_secure_payload(account_data['public_key'], json.dumps(account_data))
            authenticated_response = rotate_authentication_token(address)
            authenticated_response.data = outbound_payload
            return authenticated_response

        else:
            return bad_response

    return good_response


@app.route("/govern8r/api/v1/account/<address>/<nonce>", methods=['GET'])
def confirm_account(address, nonce):
    """
    Account registration confirmation
    Parameters
    ----------
    address : string
       The Bitcoin address of the client.
    nonce : string
       The nonce sent to the email address
    """
    if request.method == 'GET':
        account_service.confirm_account(address, nonce)
    return {}


@app.route("/govern8r/api/v1/account/<address>/notarization/<document_hash>", methods=['PUT'])
def notarization(address, document_hash):
    """
    Notarize document
    Parameters
    ----------
    address : string
       The Bitcoin address of the client.
    document_hash : string
       The hash of the document.
    """

    js = json.dumps({})
    unauthenticated_response = Response(js, status=401, mimetype='application/json')
    unauthenticated_response.set_cookie('govern8r_token', 'UNAUTHENTICATED')

    if request.method == 'PUT':
        if authenticated(address):
            inbound_payload = request.data
            str_notarization_input_data = secure_message.get_message_from_secure_payload(inbound_payload)
            notarization_input_data = json.loads(str_notarization_input_data)
            if notarization_input_data['document_hash'] == document_hash:
                notarization_input_data['address'] = address
                notarization_output_data = notarization_service.notarize(notarization_input_data)
                authenticated_response = rotate_authentication_token(address)
                if notarization_output_data is not None:
                    account_data = account_service.get_account_by_address(address)
                    outbound_payload = secure_message.create_secure_payload(account_data['public_key'], json.dumps(notarization_output_data))
                    authenticated_response.data = json.dumps(outbound_payload)
                else:
                    authenticated_response.status_code = 500
                return authenticated_response
            else:
                return unauthenticated_response
        else:
            return unauthenticated_response
    return unauthenticated_response


@app.route("/govern8r/api/v1/account/<address>/notarization/<document_hash>/status", methods=['GET'])
def notarization_status(address, document_hash):
    """
    Notarization status
    Parameters
    ----------
    address : string
       The Bitcoin address of the client.
    document_hash : string
       The hash of the document.
    """

    js = json.dumps({})
    unauthenticated_response = Response(js, status=401, mimetype='application/json')
    unauthenticated_response.set_cookie('govern8r_token', 'UNAUTHENTICATED')

    if request.method == 'GET':
        if authenticated(address):
            authenticated_response = rotate_authentication_token(address)
            status_data = notarization_service.get_notarization_status(document_hash)
            authenticated_response.data = status_data
            return authenticated_response
        else:
            return unauthenticated_response
    return unauthenticated_response


@app.route("/govern8r/api/v1/account/<address>/test", methods=['GET'])
def test_authentication(address):
    """
    Test authentication
    Parameters
    ----------
    address : string
       The Bitcoin address of the client.
    """

    js = json.dumps({})
    unauthenticated_response = Response(js, status=401, mimetype='application/json')
    unauthenticated_response.set_cookie('govern8r_token', 'UNAUTHENTICATED')

    if request.method == 'GET':
        if authenticated(address):
            authenticated_response = rotate_authentication_token(address)
            return authenticated_response
        else:
            return unauthenticated_response
    return unauthenticated_response


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)