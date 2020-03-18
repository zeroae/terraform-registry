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
import os
import random
import string
from time import sleep

import docker
import pytest
from chalice import Chalice
from docker import DockerClient
from docker.models.containers import Container
from docker.types import Healthcheck

from chalicelib.db import db_init, db_destroy


@pytest.fixture(scope="session")
def docker_client() -> DockerClient:
    client = docker.from_env()
    yield client
    client.close()


@pytest.fixture(scope="session")
def ddb_url(docker_client: DockerClient) -> str:
    SECOND: int = 1_000_000_000
    local_port: int = random.randint(49152, 65535)
    container: Container = docker_client.containers.run(
        "amazon/dynamodb-local",
        detach=True,
        healthcheck=Healthcheck(
            test="curl -s -I http://localhost:8000 | grep -q 'HTTP/1.1 400 Bad Request'",
            interval=1 * SECOND,
            timeout=1 * SECOND,
            retries=3,
        ),
        ports={"8000/tcp": local_port},
        remove=True,
    )

    def health_status():
        state = docker_client.api.inspect_container(container.id)["State"]
        return state["Health"]["Status"]

    while health_status() != "healthy":
        sleep(0.5)
        container.reload()

    yield f"http://localhost:{local_port}"
    container.stop()


@pytest.fixture(scope="session")
def aws_credentials() -> None:
    # Configure fake AWS Credentials...
    os.environ["AWS_SECRET_ACCESS_KEY"] = "fake_key"
    os.environ["AWS_ACCESS_KEY_ID"] = "fake_id"

    yield

    os.unsetenv("AWS_SECRET_ACCESS_KEY")
    os.unsetenv("AWS_ACCESS_KEY_ID")


@pytest.fixture(autouse=True, scope="module")
def db(ddb_url, aws_credentials) -> None:
    # Configure Database
    os.environ["ZTR_DYNAMODB_URL"] = ddb_url

    prefix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    os.environ["ZTR_DYNAMODB_TABLE_PREFIX"] = f"ztr-pytest-{prefix}"

    # Initialize Tables/Models
    db_init()

    yield

    # Destroy Tables/Models
    db_destroy()

    os.unsetenv("ZTR_DYNAMODB_TABLE_PREFIX")
    os.unsetenv("ZTR_DYNAMODB_URL")


@pytest.fixture
def app(db) -> Chalice:
    from app import app as chalice_app

    return chalice_app
