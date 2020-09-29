import typing

from cli_api.extensions import db

from .model import Script
from .interface import ScriptInterface


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
    def get_script_by_user_and_name(user: str, name: str) -> typing.Iterable[Script]:
        """
        Get specific script from user. Can return multiple scripts if
        the user has uploaded multiple versions of the same script.
        """
        return Script.query.filter_by(user=user, name=name).all()

    @staticmethod
    def create(new_obj: ScriptInterface) -> None:
        """
        Create a new script object.
        """
        name = new_obj["name"]
        user = new_obj["user"]
        content = new_obj["content"]

        # Check if already exists
        existing_scripts = ScriptService.get_script_by_user_and_name(
            user=user, name=name
        )
        existing_scripts = sorted(existing_scripts, key=lambda x: x.version)
        if existing_scripts:
            version = existing_scripts[-1].version + 1
        else:
            version = 1

        new_script = Script(name=name, user=user, version=version, content=content)

        db.session.add(new_script)
        db.session.commit()

        return new_script
