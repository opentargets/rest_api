
from flask import current_app
from flask.ext import restful
from flask.ext.restful import abort,reqparse
from flask_restful_swagger import swagger
from app.common import boilerplate
from app.common.boilerplate import Paginable
from app.common.auth import TokenAuthentication, is_authenticated

__author__ = 'andreap'



class RequestToken(restful.Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('appname', type=str, required=True, help="app name [appname] is required")
    parser.add_argument('secret', type=str, required=True, help="app secret [secret] is required")
    parser.add_argument('uid', type=str, required=False, help="user id [uid] ")
    parser.add_argument('password', type=str, required=False, help="password [password] ")

    def get(self, ):
        args = self.parser.parse_args()
        return TokenAuthentication.get_auth_token('cttv_api',auth_data=args)


class ValidateToken(restful.Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('auth_token', type=str, required=True, help="auth_token is required")

    def get(self, ):
        args = self.parser.parse_args()
        auth_token = args['auth_token']
        return TokenAuthentication.is_valid(auth_token)
