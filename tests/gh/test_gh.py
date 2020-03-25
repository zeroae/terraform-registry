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

import pytest
from pytest_chalice.handlers import RequestHandler

from chalicelib import gh


@pytest.fixture()
def gh_app_api() -> str:
    return "/gh"


def test_j2_can_find_template():
    from chalicelib.gh import j2

    assert j2.get_template("setup.html") is not None


def test_manifest(gh_app_api: str, client: RequestHandler):
    response = client.get(f"{gh_app_api}/")
    assert response.status_code == HTTPStatus.OK


def test_manifest_callback_invalid_nonce(gh_app_api: str, client: RequestHandler):
    response = client.get(f"{gh_app_api}/callback?state=xxx")
    assert response.status_code == HTTPStatus.EXPECTATION_FAILED


def test_manifest_callback(gh_app_api: str, client: RequestHandler, monkeypatch):
    def mock_nonce(rhs):
        return True

    monkeypatch.setattr(gh, "_verify_nonce", mock_nonce)

    response = client.get(f"{gh_app_api}/callback?state=mocked")

    assert response.status_code == HTTPStatus.OK
