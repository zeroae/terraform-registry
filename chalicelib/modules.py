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

from chalice import Blueprint, Response, ChaliceViewError
from pynamodb.exceptions import DoesNotExist

from .config import *
from .models import ModuleName, ModuleModel

bp = Blueprint(__name__)


@bp.route("/")
def list_all():
    """
    Lists all modules in the registry
    ref: https://www.terraform.io/docs/registry/api.html#list-modules
    """
    bp.current_request.query_params["q"] = "*"
    return search()


@bp.route("/{namespace}")
def list_namespace(namespace):
    """
    Lists all modules in the given namespace
    ref: https://www.terraform.io/docs/registry/api.html#list-modules
    
    """
    bp.current_request.query_params["q"] = "*"
    bp.current_request.query_params["namespace"] = namespace
    return search()


@bp.route("/search")
def search():
    """
    Search for modules in the registry
    ref: https://www.terraform.io/docs/registry/api.html#search-modules
    """
    q = bp.current_request.query_params["q"]

    # Optional
    offset = bp.current_request.query_params.get("offset", 0)
    limit = bp.current_request.query_params.get("limit", ZTR_LIMIT)
    provider = bp.current_request.query_params.get("provider", None)
    verified = bp.current_request.query_params.get("verified", None)
    namespace = bp.current_request.query_params.get("namespace", None)

    raise NotImplementedError()


@bp.route("/{namespace}/{name}")
def list_latest_all_providers(namespace, name):
    """
    List Latest Version of Module for All Providers
    ref: https://www.terraform.io/docs/registry/api.html#list-latest-version-of-module-for-all-providers
    """
    # Optional
    offset = bp.current_request.uri_params.get("offset", 0)
    limit = bp.current_request.uri_params.get("limit", ZTR_LIMIT)

    raise NotImplementedError()


@bp.route("/{namespace}/{name}/{provider}")
def list_latest(namespace, name, provider):
    """
    Latest Version for a Specific Module Provider
    ref: https://www.terraform.io/docs/registry/api.html#latest-version-for-a-specific-module-provider
    """

    raise NotImplementedError()


@bp.route("/{namespace}/{name}/{provider}/versions")
def list_versions(namespace, name, provider):
    """
    List Available Versions for a Specific Module
    ref: https://www.terraform.io/docs/registry/api.html#list-available-versions-for-a-specific-module
    """

    raise NotImplementedError()


@bp.route("/{namespace}/{name}/{provider}/{version}")
def get_module(namespace, name, provider, version):
    """
    Get a Specific Module
    ref: https://www.terraform.io/docs/registry/api.html#get-a-specific-module
    """

    raise NotImplementedError()


@bp.route("/{namespace}/{name}/{provider}/download")
def download_latest(namespace, name, provider):
    """
    Download the Latest Version of a Module
    ref: https://www.terraform.io/docs/registry/api.html#download-the-latest-version-of-a-module

    :param namespace:
    :param name:
    :param provider:
    :return:
    """

    raise NotImplementedError()


@bp.route("/{namespace}/{name}/{provider}/{version}/download")
def download(namespace: str, name: str, provider: str, version: str):
    """
    Download Source Code for a Specific Module Version
    ref: https://www.terraform.io/docs/registry/api.html#download-source-code-for-a-specific-module-version

    This is a slight misnomer, this call actually returns an empty body with an HTTP Response header
    X-Terraform-Get pointing to the actual location of the module source code.

    The module location must follow the go-getter URL format (c.f. https://github.com/hashicorp/go-getter#url-format)

    :param namespace: The module namespace
    :param name: The module name
    :param provider: The module primary provider
    :param version: The module version
    :return: HTTP 204 (no content), with X-Terraform-Get header pointing to module.source
    """

    # noinspection PyTypeChecker
    try:
        module_name = ModuleName(namespace, name, provider)
        module = ModuleModel.get(module_name, range_key=version)
        if module.source is None:
            raise ChaliceViewError(
                msg=f"{namespace}/{name}/{provider}/{version} is missing the `source` attribute."
            )

        return Response(
            body=None,
            status_code=HTTPStatus.NO_CONTENT,
            headers={"X-Terraform-Get": module.source},
        )
    except DoesNotExist as dne:
        return Response(
            body={"errors": [dne.args[0]]}, status_code=HTTPStatus.NOT_FOUND
        )
    except ChaliceViewError as cve:
        return Response(body={"errors": cve.args}, status_code=cve.STATUS_CODE)
