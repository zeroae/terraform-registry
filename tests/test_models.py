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
from chalicelib.models import ModuleName, ModuleNameAttribute


def test_module_name_init():
    fqmn: ModuleName = ModuleName("namespace", "name", "provider")

    assert fqmn.namespace == "namespace"
    assert fqmn.name == "name"
    assert fqmn.provider == "provider"


def test_module_name_attribute_serialize():
    mn_attr: ModuleNameAttribute = ModuleNameAttribute()

    fqmn_str: str = mn_attr.serialize(ModuleName("namespace", "name", "provider"))
    assert fqmn_str == "namespace/name/provider"


def test_module_name_attribute_deserialize():
    mn_attr: ModuleNameAttribute = ModuleNameAttribute()

    fqmn: ModuleName = mn_attr.deserialize("namespace/name/provider")
    assert fqmn == ModuleName("namespace", "name", "provider")
