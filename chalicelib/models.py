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
from dataclasses import dataclass
from datetime import datetime

from pynamodb.attributes import (
    Attribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
    BooleanAttribute,
    NumberAttribute,
)
from pynamodb.constants import STRING
from pynamodb.models import Model

from .config import ZTR_DYNAMODB_TABLE_PREFIX, ZTR_DYNAMODB_URL


@dataclass
class ModuleName(object):
    """
    The Terraform Registry Fully Qualified Module Name (FQMN)
    """

    namespace: str
    name: str
    provider: str


class ModuleNameAttribute(Attribute):
    """
    (de)Serializer for ModuleName
    """

    attr_type = STRING

    def serialize(self, value: ModuleName) -> str:
        return "/".join([value.namespace, value.name, value.provider])

    def deserialize(self, value: str) -> ModuleName:
        return ModuleName(*value.split("/"))


class ModuleModel(Model):
    """
    A Terraform Registry Module Model
    """

    class Meta:
        host = ZTR_DYNAMODB_URL
        table_name = f"{ZTR_DYNAMODB_TABLE_PREFIX}Module"

    module_name = ModuleNameAttribute(hash_key=True)
    version = UnicodeAttribute(range_key=True)
    source = UnicodeAttribute()

    published_at = UTCDateTimeAttribute(default_for_new=datetime.utcnow)

    verified = BooleanAttribute(null=True)

    owner = UnicodeAttribute(null=True)
    description = UnicodeAttribute(null=True)

    downloads = NumberAttribute(default_for_new=0)


if not ModuleModel.exists():
    ModuleModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
