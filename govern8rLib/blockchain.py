from blockcypher import embed_data
import requests

# coin symbol can be  btc-testnet or btc and may more there. refer blockcypher.
def embed(data_value, token_value, coin_network='btc') :
    try :
        response=embed_data(to_embed=data_value,api_key=token_value,data_is_hex=True,coin_symbol=coin_network)
        print response
        hash_value = response['hash']
        return hash_value
    except requests.ConnectionError as e :
         print "Connection Error"
         print e
         return "error"