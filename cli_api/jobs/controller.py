"""
Resources for the /scripts endpoint
"""
from flask_restx import Namespace, Resource
from flask_accepts import accepts, responds

from cli_api.extensions import rq
from cli_api.auth.model import User
from cli_api.common.utils import get_bearer_token
from .schema import JobSchema
from .service import JobService


api = Namespace(
    "Jobs",
    description="Endpoint for fetching job status and results",
    path="/jobs"
)


@api.route("")
class JobResource(Resource):

    @responds(schema=JobSchema(many=True))
    def get(self):
        auth_token = get_bearer_token()
        user_id = User.decode_auth_token(auth_token)
        return JobService.get_jobs_by_user_id(user_id)


@api.route("/<string:job_id>")
class JobIdResource(Resource):

    @responds(schema=JobSchema)
    def get(self, job_id: str):
        """
        Get details for given job_id.

        :param job_id: The job ID to look up.

        :todo: Right now, we have no restrictions on who can look up a job ID. Should confirm
            the user ID is valid for the given job.
        """
        auth_token = get_bearer_token()
        user_id = User.decode_auth_token(auth_token)

        return JobService.get_job_by_id(job_id=job_id, user_id=user_id)
