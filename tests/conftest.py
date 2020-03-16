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

import pytest
from chalice import Chalice

from chalicelib.db import db_init, db_destroy


@pytest.fixture(autouse=True, scope="session")
def db() -> None:
    # Configure Database
    ddb_table_prefix_env = "ZTR_DYNAMODB_TABLE_PREFIX"

    prefix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    os.environ[ddb_table_prefix_env] = f"ztr-pytest-{prefix}"

    # Initialize Tables/Models
    db_init()

    yield

    # Destroy Tables/Models
    db_destroy()
    os.unsetenv(ddb_table_prefix_env)


@pytest.fixture
def app(db) -> Chalice:
    from app import app as chalice_app

    return chalice_app
