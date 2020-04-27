#  Copyright (c) 2020 Zero A.E., LLC
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
from http import HTTPStatus
from random import random

import requests
from chalice import Blueprint, Response
from jinja2 import Environment, PackageLoader

bp: Blueprint = Blueprint(__name__)
j2: Environment = Environment(loader=PackageLoader(__name__, "templates"))


nonce: str = None


def _create_nonce() -> str:
    # TODO: Convert State into DynamoDB Entry with a short TTL
    global nonce
    nonce = "".join(random.choices("01234567889abcedf", k=40))
    return nonce


def _verify_nonce(rhs_nonce: str):
    # TODO: GitHub is not sending the state/nonce back...
    return True

    global nonce
    if nonce and nonce == rhs_nonce:
        nonce = None
        return True
    return False


@bp.route("/")
def manifest():
    """
    Note: HTTP Post Redirect, 307 code
    ref: https://softwareengineering.stackexchange.com/questions/99894/why-doesnt-http-have-post-redirect
    :return:
    """
    from .config import GITHUB_URL

    app_url = "https://tf.local.zeroae.net"
    setup_html = j2.get_template("setup.html")
    body = setup_html.render(
        github_url=GITHUB_URL,
        organization="zeroae",
        name="Terraform Registry",
        description="""# Terraform Registry
                       Share Terraform Modules directly from GitHub using GitHub as the 
                       Storage, Authentication, and Authorization backends.""",
        url=app_url,
        redirect_url=f"{app_url}/gh/callback",
        hook_url=f"{app_url}/gh/events",
        public=False,
        default_permissions={"contents": "read"},
        default_events=["meta", "release", "repository"],
        nonce=_create_nonce(),
    )
    return Response(body=body, status_code=200, headers={"Content-Type": "text/html"})


@bp.route("/callback")
def manifest_callback():
    """
    Finishes the GitHub Application  Registration flow
    1. Verifies state is correct
    2. Converts code for clientId, clientSecret, webhook secret, and App PEM
    3. Stores above in DynamoDB

    :return:
    """
    from .config import GITHUB_API_URL

    query_params = bp.current_request.query_params
    query_params = query_params if query_params else dict()

    rhs_nonce = query_params.get("state", None)
    if not _verify_nonce(rhs_nonce):
        return Response(
            body='{"error": "The state value does not match expectations."}',
            status_code=HTTPStatus.EXPECTATION_FAILED,
            headers={"Content-Type": "text/html"},
        )

    code = query_params.get("code", None)
    if code is None:
        return Response(
            body='{"error": "The GitHub code is missing."}',
            status_code=HTTPStatus.EXPECTATION_FAILED,
            headers={"Content-Type": "text/html"},
        )

    s: requests.Session = requests.Session()
    s.headers["Accept"] = "application/vnd.github.machine-man-preview+json"

    r: requests.Response = s.post(f"{GITHUB_API_URL}/app-manifests/{code}/conversions")

    return Response(
        body=r.content,
        status_code=r.status_code,
        headers={"Content-Type": r.headers["Content-Type"]},
    )


@bp.route("/events")
def events():
    raise NotImplementedError()
