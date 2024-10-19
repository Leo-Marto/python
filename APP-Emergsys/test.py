import jwt
import datetime

# Define a secret key for signing the token
SECRET_KEY = 'elpepe'

# Payload data (user info, expiration, etc.)
payload = {
    'info':{ "usuario":"elpepe",
            "mail":"lacaca"

    }
}

# Generate the token
token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

print("Token generado:", token)


decoded_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
print("Decoded data:", decoded_data)
