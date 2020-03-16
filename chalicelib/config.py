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

from environs import Env

env = Env()
env.read_env()

# Configuration Options
ZTR_LIMIT = 1_000

with env.prefixed("ZTR_"):
    with env.prefixed("DYNAMODB_"):
        ZTR_DYNAMODB_URL = env.str("URL", default=None)
        ZTR_DYNAMODB_TABLE_PREFIX = env.str("TABLE_PREFIX")
