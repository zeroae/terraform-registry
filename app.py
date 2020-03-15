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

from chalice import Chalice

from chalicelib.modules import bp as modules_bp

app = Chalice(app_name="terraform-registry")
app.experimental_feature_flags.update(["BLUEPRINTS"])
app.register_blueprint(modules_bp, url_prefix="/v1")


@app.route("/.well-known/terraform.json")
def discovery():
    """The Terraform Registry Service Discovery Protocol

       ref: https://www.terraform.io/docs/internals/remote-service-discovery.html#discovery-process
    """
    host = app.current_request.headers["host"]
    # Only HTTPS is allowed for Terraform Registry protocol
    # Use ngrok to redirect https traffic for free during development
    return {"modules.v1": f"https://{host}/v1"}
