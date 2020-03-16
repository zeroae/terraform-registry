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

from pytest_chalice.handlers import RequestHandler

from chalicelib.models import ModuleModel


def test_list_versions_response_schema(client: RequestHandler, monkeypatch) -> None:
    fqmn = "namespace/name/provider"

    response = client.get(f"/v1/{fqmn}/versions")

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


def test_download_success(client: RequestHandler, monkeypatch) -> None:
    fqvmn = "namespace/name/provider/0.1.0"

    def mock_get(hash_key, **kwargs):
        rv = ModuleModel(hash_key, version=kwargs["range_key"])
        rv.source = "./name"
        return rv

    def mock_save(*args, **kwargs):
        pass

    monkeypatch.setattr(ModuleModel, "get", mock_get)
    monkeypatch.setattr(ModuleModel, "save", mock_save)

    response = client.get(f"/v1/{fqvmn}/download")

    assert response.status_code == HTTPStatus.NO_CONTENT


def test_download_failure(client: RequestHandler) -> None:
    fqvmn = "namespace/name/provider/0.0.0"
    response = client.get(f"/v1/{fqvmn}/download")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert type(response.json["errors"]) == list
