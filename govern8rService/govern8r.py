from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions


app = FlaskAPI(__name__)


@app.route("/govern8r/api/v1/pubkey", methods=['GET'])
def pubkey():
    """
    Return server pubkey.
    """

    # request.method == 'GET'
    return ""


@app.route("/govern8r/api/v1/challenge/<address>", methods=['GET', 'PUT'])
def challenge(address):
    """
    Authentication
    """
    if request.method == 'PUT':
        return ""

    # request.method == 'GET'
    return ""


@app.route("/govern8r/api/v1/account", methods=['POST'])
def account():
    """
    Account registration
    """

    # request.method == 'POST'
    return ""


@app.route("/govern8r/api/v1/account/<address>", methods=['GET'])
def account(address):
    """
    Account registration
    """

    # request.method == 'GET'
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