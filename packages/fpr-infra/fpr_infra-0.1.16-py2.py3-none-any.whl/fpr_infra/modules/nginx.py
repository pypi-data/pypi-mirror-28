# coding: utf-8

from pyinfra.api import deploy
from pyinfra.modules import files, server
from fpr_infra.modules import files as fpr_files


@deploy("Enable nginx application configuration")
def enable_conf(state, host, conf_file, dest=None):
    dest = dest or conf_file

    # set available conf
    if host.fact.file(f"/etc/nginx/sites-available/{dest}"):
        server.shell(
            state, host,
            f"rm /etc/nginx/sites-available/{dest}",
            sudo=True
        )
    fpr_files.move(
        state, host,
        {f"Make available {dest} site"},
        conf_file, f"/etc/nginx/sites-available/{dest}",
        sudo=True
    )

    # set available conf as enabled
    if host.fact.file(f"/etc/nginx/sites-enabled/{dest}"):
        server.shell(
            state, host,
            f"rm /etc/nginx/sites-enabled/{dest}",
            sudo=True
        )
    files.link(
        state, host,
        {f"Make enabled {dest} site"},
        f"/etc/nginx/sites-enabled/{dest}", f"/etc/nginx/sites-available/{dest}",
        sudo=True
    )


@deploy("Disable nginx application configuration")
def disable_conf(state, host, conf_file):
    if host.fact.link(f"/etc/nginx/sites-enabled/{conf_file}"):
        server.shell(
            state, host,
            {f"Disable {conf_file} site"},
            f"rm /etc/nginx/sites-enabled/{conf_file}",
            sudo=True
        )
