from unittest.mock import patch

from cli_api.jobs.service import JobService
from cli_api.auth.model import User


@patch.object(User, "decode_auth_token", lambda _: 1)
def test_get_all_jobs(app, db):
    with app.test_client() as client:
        job1 = JobService.create_job({'id': 'job1', 'user_id': 1})
        job2 = JobService.create_job({'id': 'job2', 'user_id': 1})
        headers = {"Authorization": "Bearer abc123"}
        jobs = client.get("/jobs", headers=headers)
        assert jobs.status_code == 200

        jobs = jobs.get_json()
        assert jobs[0]['id'] == job1.id
        assert jobs[1]['id'] == job2.id


@patch.object(User, "decode_auth_token", lambda _: 1)
def test_get_job_by_id(app, db):
    with app.test_client() as client:
        job1 = JobService.create_job({'id': 'job1', 'user_id': 1})
        headers = {"Authorization": "Bearer abc123"}
        job_req = client.get("/jobs/job1", headers=headers)

        assert job_req.status_code == 200
        assert job_req.get_json()['id'] == job1.id


@patch.object(User, "decode_auth_token", lambda _: 1)
def test_get_job_by_id_wrong_user(app, db):
    with app.test_client() as client:
        JobService.create_job({'id': 'job1', 'user_id': 2})
        headers = {"Authorization": "Bearer abc123"}
        res = client.get("/jobs/job1", headers=headers)

        assert res.status_code == 403
        assert res.get_json()["message"] == "Permission denied"
