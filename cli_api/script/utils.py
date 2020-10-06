import re

from cli_api.common.errors import UserException


def get_placeholders(script_content: str) -> dict:
    """
    Given a script, return a dictionary mapping placeholders to default values.
    """
    placeholders = re.findall(r"{{(.*)}}", script_content)
    placeholder_dict = {}

    # Build up placeholders/defaults
    for placeholder in placeholders:
        p = placeholder.split(":")
        var = p.pop(0)
        default = ":".join(p) if p else None
        placeholder_dict[var] = default

    return placeholder_dict


def set_placeholders(script_content: str, variable_dict: dict = None):
    """
    Replace placeholders in script with
    """
    placeholder_dict = get_placeholders(script_content)

    for placeholder, default in placeholder_dict.items():
        if variable_dict and placeholder in variable_dict:
            value = variable_dict[placeholder]
        elif default:
            value = default
        else:
            raise UserException(
                f"No value provided for placeholder '{placeholder}'", 400
            )

        script_content = re.sub(rf"{{{{{placeholder}.*}}}}", value, script_content)

    return script_content
