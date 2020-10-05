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
    "Jobs", description="Endpoint for fetching job status and results", path="/jobs"
)


@api.route("")
class JobResource(Resource):
    @responds(schema=JobSchema(many=True))
    def get(self):
        """
        Get information about all jobs.
        """
        auth_token = get_bearer_token()
        user_id = User.decode_auth_token(auth_token)
        return JobService.get_jobs_by_user_id(user_id)


@api.route("/<string:job_id>")
@api.doc(params={"job_id": "A job ID"})
class JobIdResource(Resource):
    @responds(schema=JobSchema)
    def get(self, job_id: str):
        """
        Get information about the given job ID.
        """
        auth_token = get_bearer_token()
        user_id = User.decode_auth_token(auth_token)

        return JobService.get_job_by_id(job_id=job_id, user_id=user_id)
