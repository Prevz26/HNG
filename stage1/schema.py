from marshmallow.fields import String
from extensions import ma

class User_Schema(ma.Schema):
    ip = String(required=True)
    country = String(required=True)
    city = String(required=True)
