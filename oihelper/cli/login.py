import pickle
import click
import requests

from oihelper.auth import AuthenticationHandler
from .common import CONFIG_DIR, abort_with_error

@click.command()
@click.option("--username", prompt=True, help="Username of the account.")
@click.option("--password", prompt=True, hide_input=True, help="Password of the account.")
def login(username: str, password: str):
    """Login to a Luogu account."""
    auth_handler = AuthenticationHandler()
    auth_handler.show_captcha()
    captcha = click.prompt("Captcha")
    try:
        response = auth_handler.login(username, password, captcha)
    except requests.HTTPError as e:
        abort_with_error(f"Failed to login with {e}")
    auth_handler.sync_login(response["syncToken"])
    pickle.dump(auth_handler.session, open(f"{CONFIG_DIR}/session.pickle", "wb"))
    click.echo(click.style("Login success!", bold=True, fg="green"))
