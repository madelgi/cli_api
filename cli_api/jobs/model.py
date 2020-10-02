import datetime

from sqlalchemy import String, Column, Integer, Text, DateTime, ForeignKey, Boolean

from cli_api.extensions import db


class Job(db.Model):
    """
    Model for submitted jobs.

    :param id: The job UUID.
    :param name: Name of the job.
    :param submitted: Date of submission.
    :param description: An optional job description.
    :param complete: Job completion status.
    :param results: Job results (container stdout, as of now)

    :todo: Maybe send results to some sort of static hosting service, and make the results field a URL.
    :todo: Rather than `complete`, have a `status` field that indicates the job status (e.g., 'submitted', 'running',
        'succeeded', 'failed')
    """
    id = Column(String(36), primary_key=True)
    name = Column(String(128), index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    description = Column(String(512), index=True)

    submit_time = Column(DateTime, default=datetime.datetime.utcnow)
    complete_time = Column(DateTime)
    complete = Column(Boolean, default=False)
    results = Column(Text)
