from cli_api.jobs.model import Job


def test_job_create():
    job = Job(id='job_id_123', name='job_name', user_id=1, description='it\'s a job')
    assert job
