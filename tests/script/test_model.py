from cli_api.script.model import Script


def test_script_create():
    script = Script(user=1, name="script", version=1, content='echo "HELLO"')
    assert script
