from src.Entities.Git.git_api_requester import GitApiRequester
from flask_restful import Resource, reqparse


class GitRepositoryController(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("token", required=True, help="token is required")
        parser.add_argument("rp_name", required=True, help="rp_name is required")
        args = parser.parse_args()

        # domain
        requester = GitApiRequester(args["token"])
        rp = requester.get_rp_by_name(args['rp_name'])
        return requester.get_rp_info(rp), 200