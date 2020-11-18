from flask_restful import Resource, reqparse


class ExampleController(Resource):
    def get(self):
        return {
            "message": "success"
        }, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("account", required=True, help="account is required.")
        parser.add_argument("password", required=True, help="password is required.")

        args = parser.parse_args()
        return {
            "message": 'success',
            'args':{
                "account": args["account"],
                "password": args["password"]
            }
        }