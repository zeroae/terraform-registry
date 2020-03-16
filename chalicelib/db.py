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


def db_init():
    from chalicelib.models import ModuleModel

    if not ModuleModel.exists():
        ModuleModel.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )


def db_destroy():
    from chalicelib.models import ModuleModel

    if ModuleModel.exists():
        ModuleModel.delete_table()
