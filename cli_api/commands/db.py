import click
import json

from flask.cli import with_appcontext

from cli_api.auth.service import UserService
from cli_api.script.service import ScriptService


@click.command("seed_db")
@click.option("--in-file", "-i", required=True, type=str)
@with_appcontext
def seed_db(in_file: str):
    """
    Seed database with test data. Should probably make this modular, maybe
    read from a file currently
    sets myself as admin.
    """
    with open(in_file, "r") as handle:
        objs = json.load(handle)

    users = objs.get("users", [])
    for user in users:
        UserService.register_user(user)

    scripts = objs.get("scripts", [])
    for script in scripts:
        ScriptService.create(script)
