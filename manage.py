#! /usr/bin/env python
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
import json
import os

import click

from chalicelib import db


def _get_chalice_stages():
    config = _get_chalice_config()
    stages: dict = config["stages"]
    return list(stages.keys())


def _get_chalice_config():
    with open(".chalice/config.json") as f:
        config = json.load(f)
    return config


def _apply_chalice_stage(stage):
    config = _get_chalice_config()
    stage_config: dict = config["stages"][stage]
    env_vars: dict = stage_config.get("environment_variables", {})
    for k, v in env_vars.items():
        if k not in os.environ:
            os.environ[k] = v


@click.group()
@click.option(
    "--stage",
    help="The Chalice stage",
    type=click.Choice(_get_chalice_stages()),
    default=_get_chalice_stages()[0],
    show_default=True,
)
def go(stage) -> None:
    """
    The Terraform Registry Management CLI
    """
    _apply_chalice_stage(stage)


@go.group()
def db():
    """
    Manage the DynamoDB backend (init, destroy, backup, restore).
    """
    pass


@db.command(name="init")
def db_init():
    """Initializes the backend."""
    return db.db_init()


@db.command(name="destroy")
def db_destroy():
    """Destroys the backend."""
    click.confirm(
        "There is no coming back from this... are you sure you want to continue?",
        abort=True,
    )
    return db.db_destroy()


@db.command(name="backup")
@click.argument("filename", type=click.Path(dir_okay=False, writable=True))
def db_backup(filename):
    """Backups the backend content."""
    db.db_dump(filename)
    return 0


@db.command(name="restore")
@click.argument("filename", type=click.Path(exists=True, dir_okay=False))
def db_restore(filename):
    """Restores the backend content."""
    db.db_load(filename)
    return 0


@go.group(name="record")
def record():
    """Manage records in the backend (create, delete, import, ...)"""
    pass


def validate_fqvmn(ctx, param, value):
    try:
        namespace, name, provider, version = map(str, value.split("/", 4))
        return (namespace, name, provider, version)
    except ValueError:
        raise click.BadParameter(
            f"{param} needs to be in format <namespace>/<name>/<provider>/<version>"
        )


fqvm_argument = click.argument(
    "fqvmn", callback=validate_fqvmn, metavar="<namespace>/<name>/<provider>/<version>"
)


@record.command("create")
@fqvm_argument
@click.argument("getter-url", metavar="getter-url")
def record_create(fqvmn, getter_url):
    """
    Create a new Terraform Module Record.

    Hashicorp's `getter-url` format supports a variety of protocols,
    and implements various tricks to do certain things. For full-details
    on the URL format see http://bit.ly/2Wxgxk7.

    \b
    Examples:
        - Local:
              ./local
        - GitHub:
              github.com/terraform-aws-modules/terraform-aws-vpc?ref=2.29.0
        - S3:
              s3::http://s3.amazonaws.com/bucket/hello.txt
    """
    from chalicelib.models import ModuleModel, ModuleName

    namespace, name, provider, version = fqvmn
    module_name = ModuleName(namespace, name, provider)
    try:
        ModuleModel.get(module_name, version)  # noqa
        return 1
    except ModuleModel.DoesNotExist as dne:
        module = ModuleModel(
            module_name=ModuleName(namespace, name, provider),
            version=version,
            getter_url=getter_url,
        )
        module.save()


@record.command("delete")
@fqvm_argument
def record_delete(fqvmn):
    """
    Delete a Terraform Module Record.
    """
    from chalicelib.models import ModuleModel, ModuleName

    namespace, name, provider, version = fqvmn
    module_name = ModuleName(namespace, name, provider)
    try:
        module = ModuleModel.get(hash_key=module_name, range_key=version)  # noqa
        module.delete()
    except ModuleModel.DoesNotExist:
        pass


@record.command("list")
def record_list():
    """
    Lists all the Terraform Modules in backend.
    """
    from chalicelib.models import ModuleModel

    for module in ModuleModel.scan(attributes_to_get=["module_name", "version"]):
        click.echo(f"{module.module_name}/{module.version}")


if __name__ == "__main__":
    go()
