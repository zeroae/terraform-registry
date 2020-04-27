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
import urllib

from environs import Env

env: Env = Env()
env.read_env()

with env.prefixed("GITHUB"):
    GITHUB_URL = env.str("URL", "https://github.com")
    if GITHUB_URL == "https://github.com":
        GITHUB_API_URL = "https://api.github.com"
    else:
        GITHUB_API_URL = urllib.join(GITHUB_URL, "/api/v3")

    GITHUB_APP_ID = env.str("APP_ID", None)
    GITHUB_APP_CLIENT_ID = env.str("APP_CLIENT_ID", None)

    # TODO: decrypt these with KMS or Credstash
    GITHUB_APP_CLIENT_SECRET = env.str("APP_CLIENT_SECRET", None)
    GITHUB_APP_WEB_SECRET = env.str("APP_WEB_SECRET", None)
    GITHUB_APP_PRIVATE_KEY = env.str("APP_PRIVATE_KEY", None)
