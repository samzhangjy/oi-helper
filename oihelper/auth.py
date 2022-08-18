from html.parser import HTMLParser

import click
import requests

from .common import USER_AGENT
from oihelper.cli.common import CONFIG_DIR


class AuthenticationHandler(object):
    def __init__(self, session: requests.Session = None) -> None:
        super().__init__()
        self.session = session or requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self.session.headers["referer"] = "http://www.luogu.com.cn/"

    def _get_csrf_token(self) -> str:
        class HTMLCSRFTokenParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                try:
                    if tag == "meta" and attrs["name"] == "csrf-token":
                        raise StopIteration(attrs["content"])
                except KeyError:
                    pass

        r = self.session.get("https://www.luogu.com.cn/auth/login")
        r.raise_for_status()
        try:
            HTMLCSRFTokenParser().feed(r.text)
        except StopIteration as csrf_token:
            return str(csrf_token)

    def login(self, username: str, password: str, captcha: str) -> None:
        r = self.session.post(
            "https://www.luogu.com.cn/api/auth/userPassLogin",
            headers={
                "x-csrf-token": self._get_csrf_token(),
            },
            json={
                "username": username,
                "password": password,
                "captcha": captcha,
            },
        )
        r.raise_for_status()
        return r.json()

    def show_captcha(self) -> None:
        r = self.session.get("https://www.luogu.com.cn/api/verify/captcha")
        r.raise_for_status()
        captcha_local = f"{CONFIG_DIR}/captcha.png"
        with open(captcha_local, "wb") as f:
            f.write(r.content)
        click.launch(captcha_local)

    def sync_login(self, token: str) -> None:
        self.session.post(
            "https://www.luogu.org/api/auth/syncLogin", json={"syncToken": token}
        )
