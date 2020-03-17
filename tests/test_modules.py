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


@pytest.fixture(name="modules_api")
def fixture_modules_api(client: RequestHandler) -> str:
    response = client.get("/.well-known/terraform.json")
    return response.json["modules.v1"][:-1]


def test_list_versions_response_schema(
    modules_api: str, client: RequestHandler
) -> None:
    fqmn = "namespace/name/provider"

    response = client.get(f"{modules_api}/{fqmn}/versions")

    assert response.status_code == HTTPStatus.OK
    assert "modules" in response.json

    modules = response.json["modules"]
    assert type(modules) == list
    assert len(modules) == 1

    first_module = modules[0]
    assert "source" in first_module
    assert first_module["source"] == fqmn

    assert "versions" in first_module
    assert type(first_module["versions"]) == list


def test_list_versions(modules_api: str, client: RequestHandler, monkeypatch) -> None:
    from chalicelib.models import ModuleModel

    fqmn = "namespace/name/provider"
    versions = ["0.1.0", "0.2.0", "0.3.0"]

    def mock_query(hash_key, **kwargs):
        return [ModuleModel(hash_key, version=version) for version in versions]

    monkeypatch.setattr(ModuleModel, "query", mock_query)

    response = client.get(f"{modules_api}/{fqmn}/versions")
    response_versions = [v["version"] for v in response.json["modules"][0]["versions"]]

    assert response_versions == versions


def test_download_latest(modules_api: str, client: RequestHandler, monkeypatch) -> None:
    from chalicelib.models import ModuleModel

    fqmn = "namespace/name/provider"
    versions = ["0.0.0", "0.9.0", "0.10.0"]
    fqvmn = f"{fqmn}/{versions[-1]}"

    def mock_query(hash_key, **kwargs):
        from random import shuffle

        shuffle(versions)
        return [ModuleModel(hash_key, version=version) for version in versions]

    monkeypatch.setattr(ModuleModel, "query", mock_query)

    response = client.get(f"{modules_api}/{fqmn}/download")

    assert response.status_code == HTTPStatus.FOUND
    assert "Location" in response.headers
    assert response.headers["Location"] == f"{modules_api}/{fqvmn}/download"


def test_download_latest_dne(
    modules_api: str, client: RequestHandler, monkeypatch
) -> None:
    from chalicelib.models import ModuleModel

    fqmn = "namespace/name/provider"

    monkeypatch.setattr(ModuleModel, "query", lambda *args, **kwargs: [])
    response = client.get(f"{modules_api}/{fqmn}/download")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_download_success(
    modules_api: str, client: RequestHandler, monkeypatch
) -> None:
    from chalicelib.models import ModuleModel

    fqvmn = "namespace/name/provider/0.1.0"

    def mock_get(hash_key, **kwargs):
        rv = ModuleModel(hash_key, version=kwargs["range_key"])
        rv.source = "./name"
        return rv

    def mock_save(*args, **kwargs):
        pass

    monkeypatch.setattr(ModuleModel, "get", mock_get)
    monkeypatch.setattr(ModuleModel, "save", mock_save)

    response = client.get(f"{modules_api}/{fqvmn}/download")

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.headers["X-Terraform-Get"] == "./name"


def test_download_failure(modules_api: str, client: RequestHandler) -> None:
    fqvmn = "namespace/name/provider/0.0.0"
    response = client.get(f"{modules_api}/{fqvmn}/download")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert type(response.json["errors"]) == list
