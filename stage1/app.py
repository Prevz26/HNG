from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from marshmallow.exceptions import ValidationError
from extensions import ma
from schema import User_Schema  
from dotenv import load_dotenv
import os
import ipinfo
import requests

load_dotenv()

app = Flask(__name__)
api = Api(app)
ma.init_app(app)

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(e.messages), 400

def access_token():
    token = os.getenv("secret")
    return token

# routes
class User(Resource):
    def get(self):
        name = request.args.get("visitor_name")
        # ip = "105.113.40.64"
        ip = request.remote_addr
        token = access_token()
        handler = ipinfo.getHandler(token)
        user_schema = User_Schema() 
        details = handler.getDetails(ip_address=ip)
        # print(details)
        ip_details = user_schema.dump(details)

        url = f" http://api.weatherapi.com/v1/current.json"
        params = {
            "key": os.getenv("weather_api_key"),
            "q": ip_details.get("city")
        }

        req = requests.get(url, params=params)
        response = req.json()
        print(type(response))
        # ["current"]["temp_c"]

        res = {
            "client_ip": ip_details.get("ip"),
            "location": ip_details.get("city"),
            "greeting":f"hello, {name}! your temperature is {response} degrees celsius in {ip_details.get('city')}",
        }
        return jsonify(res)

api.add_resource(User, "/api/hello")

if __name__ == "__main__":
    app.run(debug=True)


