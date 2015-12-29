from flask import request, jsonify
from flask_api import FlaskAPI, status, exceptions
from wallet import NotaryWallet


app = FlaskAPI(__name__)
wallet = NotaryWallet()


@app.route("/govern8r/api/v1/pubkey", methods=['GET'])
def pubkey():
    """
    Return server public key. The key is encoded in hex and needs to be decoded from hex to be used by the encryption utility.
    """
    # request.method == 'GET'
    public_key = wallet.get_public_key()
    return {'public_key': public_key.encode("hex")}


@app.route("/govern8r/api/v1/challenge/<address>", methods=['GET', 'PUT'])
def challenge(address):
    """
    Authentication
    """
    if request.method == 'PUT':
        return ""

    # request.method == 'GET'
    return ""


@app.route("/govern8r/api/v1/account/<address>", methods=['GET'])
def account(address):
    """
    Account registration
    """
    # request.method == 'POST'
    return ""


@app.route("/govern8r/api/v1/account", methods=['POST'])
def register_account():
    """
    Account registration
    """
    # request.method == 'POST'
    return ""


@app.route("/govern8r/api/v1/account/<address>/notarization/<document_hash>", methods=['PUT'])
def notarization(address, document_hash):
    """
    Notarize document
    """

    # request.method == 'PUT'
    return ""


@app.route("/govern8r/api/v1/account/<address>/notarization/<document_hash>/status", methods=['GET'])
def notarization_status(address, document_hash):
    """
    Notarization status
    """

    # request.method == 'GET'
    return ""


if __name__ == "__main__":
    app.run(debug=True)