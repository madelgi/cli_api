import typing


from cli_api.common.errors import UserException
from cli_api.extensions import db
from .model import Script
from .interface import ScriptInterface
from cli_api.jobs.service import JobRedisService, JobService


class ScriptService:

    @staticmethod
    def get_all_by_user(user_id: int) -> typing.Iterable[Script]:
        """
        Return a script by user/script name.

        :param user: The user that registered the script.
        :param name: Name of the script.
        """
        return Script.query.filter_by(user=user_id).all()

    @staticmethod
    def get_script_by_user_and_name(user_id: int, name: str, version: int = None) -> Script:
        """
        Get specific script from user.

        :param user_id: The user's id.
        :param name: The script name.
        :param version: The script version.
        :returns: A script. If no version is specified, returns the most recent version
        """
        scripts = Script.query.filter_by(user=user_id, name=name).all()

        # Raise error if there's no script
        if not scripts:
            raise UserException(f"Unable to find script `{name}`.", status_code=404)

        if version:
            for script in scripts:
                if script.version == version:
                    return script
            else:
                raise UserException(f"Unable to find version {version} of `{name}`", status_code=404)

        else:
            # If no version is specified,
            scripts = sorted(scripts, key=lambda x: x.version)
            return scripts[-1]

    @staticmethod
    def create(new_obj: ScriptInterface) -> None:
        """
        Create a new script object.
        """
        name = new_obj["name"]
        user = new_obj["user"]
        content = new_obj["content"]

        # Check if already exists
        try:
            script = ScriptService.get_script_by_user_and_name(user, name)
            version = script.version + 1
        except UserException:
            version = 1

        new_script = Script(name=name, user=user, version=version, content=content)

        db.session.add(new_script)
        db.session.commit()
        return new_script

    @staticmethod
    def execute(
            user_id: int,
            name: str,
            version: int = None,
            description: str = None,
            placeholder_dict: str = None):
        """
        Execute a given script.
        """
        # Get script
        script = ScriptService.get_script_by_user_and_name(user_id, name, version=version)

        # Submit job
        job_id = JobRedisService.submit_job(script.content, placeholder_dict)

        # Create job entry in database
        job = JobService.create_job(
            {'id': job_id, 'user_id': user_id, 'name': name, 'description': description}
        )

        # When job is completed, update job entry
        JobRedisService.commit_job_result(job_id)

        return job
