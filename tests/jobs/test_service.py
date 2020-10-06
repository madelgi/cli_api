from unittest.mock import MagicMock

from flask_sqlalchemy import SQLAlchemy

from cli_api.jobs.model import Job
from cli_api.jobs.service import JobService, JobRedisService


def test_get_job_by_id(db: SQLAlchemy):
    job = Job(id="job_1", name="a_job", user_id=1, description="it's a job")
    db.session.add(job)
    db.session.commit()

    assert JobService.get_job_by_id("job_1") == job


def test_get_jobs_by_user_id(db: SQLAlchemy):
    job1 = Job(id="job_1", name="a_job", user_id=1, description="it's a job")
    job2 = Job(id="job_2", name="another_job", user_id=1, description="it's a job")
    db.session.add(job1)
    db.session.add(job2)
    db.session.commit()

    jobs = JobService.get_jobs_by_user_id(user_id=1)
    assert jobs[0] == job1
    assert jobs[1] == job2


def test_create_job(db: SQLAlchemy):
    job_dict = dict(id="job_1", name="a_job", user_id=1, description="it's a job")

    job = JobService.create_job(job_dict)
    assert not job.complete
    assert job.submit_time is not None

    for k, v in job_dict.items():
        assert getattr(job, k) == v


def test_write_job_results_to_db(db: SQLAlchemy):
    job_dict = dict(id="job_1", name="a_job", user_id=1, description="it's a job")

    JobService.create_job(job_dict)
    JobService.write_job_results_to_db("job_1", "HELLO\n")

    job = JobService.get_job_by_id("job_1")
    assert job.results == "HELLO\n"


def test_redis_submit_job_no_placeholder(monkeypatch):
    # No placeholder
    queue_execution = MagicMock()
    monkeypatch.setattr("cli_api.jobs.service._execute_script.queue", queue_execution)

    JobRedisService.submit_job('echo "HELLO WORLD"')
    queue_execution.assert_called_with('echo "HELLO WORLD"')


def test_redis_submit_job_placeholder_default(monkeypatch):
    queue_execution = MagicMock()
    monkeypatch.setattr("cli_api.jobs.service._execute_script.queue", queue_execution)

    JobRedisService.submit_job('echo {{PLACEHOLDER:"default text"}} | wc -w')
    queue_execution.assert_called_with('echo "default text" | wc -w')


def test_redis_submit_job_placeholder(monkeypatch):
    queue_execution = MagicMock()
    monkeypatch.setattr("cli_api.jobs.service._execute_script.queue", queue_execution)

    JobRedisService.submit_job(
        'echo {{PLACEHOLDER:"default text"}} | wc -w',
        variable_dict={"PLACEHOLDER": '"replacement text"'},
    )
    queue_execution.assert_called_with('echo "replacement text" | wc -w')


