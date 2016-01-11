import boto3

client = boto3.client('ses',region_name='us-east-1')

response = client.send_email(
    Source='****@gmail.com',
    Destination={
        'ToAddresses': [
            '*******@troweprice.com'
        ]
    },
    Message={
        'Subject': {
            'Data': 'govern8r welcomes you to confirm your account',
            'Charset': 'iso-8859-1'
        },
        'Body': {
            'Text': {
                'Data': 'To complete your registration with govern8r please click the link',
                'Charset': 'iso-8859-1'
            },
            'Html': {
                'Data': 'http://www.govern8r.com/address/confirm/XXXXXXX',
                'Charset': 'iso-8859-1'
            }
        }
    }

)
