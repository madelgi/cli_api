import datetime
import re
import typing

import docker
from rq import get_current_job

from .interface import JobInterface
from .model import Job
from cli_api.app import create_app
from cli_api.extensions import rq, db
from cli_api.common.errors import ServerException, UserException


class JobService:
    """
    Utilities for interacting with the Job table.
    """

    @staticmethod
    def get_job_by_id(job_id: str, user_id: int = None) -> Job:
        job = Job.query.filter_by(id=job_id).first()
        if user_id and job.user_id != user_id:
            raise UserException("Permission denied", 403)

        return job

    @staticmethod
    def get_jobs_by_user_id(user_id: int) -> typing.List[Job]:
        return Job.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_job(job: JobInterface) -> Job:
        new_job = Job(
            id=job["id"],
            user_id=job["user_id"],
            name=job.get("name"),
            description=job.get("description"),
        )
        db.session.add(new_job)
        db.session.commit()

        return new_job

    @staticmethod
    def write_job_results_to_db(job_id: str, job_result: str):
        job: Job = JobService.get_job_by_id(job_id)
        if not job:
            raise ServerException(f"Unable to find job with ID {job_id}")

        job.complete = True
        job.complete_time = datetime.datetime.utcnow()
        job.results = job_result

        db.session.commit()


class JobRedisService:
    """
    Utilities for interacting with the redis job queue.
    """

    @staticmethod
    def submit_job(script_content: str, variable_dict: dict = None):
        """
        Submit a job to the queue.
        """
        script_content = _handle_placeholders(script_content, variable_dict)
        job = _execute_script.queue(script_content)
        return job.id

    @staticmethod
    def commit_job_result(job_id: str):
        """
        Commit RQ job result to database.
        """
        _update_job_db.queue(depends_on=job_id, at_front=True)


####################################################################################################
# Private helper methods for redis service
####################################################################################################
@rq.job
def _execute_script(script_content: str):
    """
    Helper function that executes a code string in a docker container.
    """
    client = docker.from_env()
    return client.containers.run(
        "alpine", command=script_content, mem_limit="10m", remove=True
    )


@rq.job
def _update_job_db():
    """
    Once job has completed running, update the database with job results and status.

    :todo: Should probably use a separate queue for these jobs.
    :todo: We need this to execute immediately after the corresponding script execution, or
        else we may run into issues with TTL.
    """
    parent_job = get_current_job().dependency
    app = create_app("prod")
    with app.app_context():
        JobService.write_job_results_to_db(
            parent_job.id, parent_job.result.decode("utf-8")
        )


def _handle_placeholders(script_content: str, variable_dict: dict = None) -> str:
    """
    Helper method for replacing placeholders with values.
    """
    if not variable_dict:
        variable_dict = {}

    placeholders = re.findall(r"{{(.*)}}", script_content)
    placeholder_dict = {}

    # Build up placeholders/defaults
    for placeholder in placeholders:
        p = placeholder.split(":")
        var = p.pop(0)
        default = ":".join(p) if p else None
        placeholder_dict[var] = default

    for placeholder, default in placeholder_dict.items():
        if placeholder in variable_dict:
            value = variable_dict[placeholder]
        elif default:
            value = default
        else:
            raise UserException(
                f"No value provided for placeholder '{placeholder}'", 400
            )

        script_content = re.sub(rf"{{{{{placeholder}.*}}}}", value, script_content)

    return script_content
