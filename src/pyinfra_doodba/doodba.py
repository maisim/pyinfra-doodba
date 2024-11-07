from pyinfra import host
from pyinfra.operations import files, server, apt, pipx
from pyinfra.api import deploy

DEFAULTS = {
    "ssh_user": "root",  # The username used by pyinfra to connect to the host
    "doodba_user": "doodba",
    "doodba_home_dir": "/home/doodba",
}


@deploy("Install doodba", data_defaults=DEFAULTS)
def install_doodba():
    apt.packages(
        name="Install doodba dependencies",
        packages=["git", "pipx", "bash-completion"],
        update=True,
    )
    server.user(
        name="Create the doodba user",
        user=host.data.doodba_user,
        home=host.data.doodba_home_dir,
        shell="/bin/bash",
        public_keys=[host.data.default_ssh_key],
    )

    files.directory(
        name="Ensure the doodba home directory exists",
        path=host.data.doodba_home_dir,
        user=host.data.doodba_user,
        group=host.data.doodba_user,
    )

    pipx.ensure_path(
        name=f"Ensure pipx path is in the {host.data.doodba_user} user's PATH",
        _sudo=True,
        _use_sudo_login=True,
        _sudo_user=host.data.doodba_user,
    )

    pipx.packages(
        name="Install doodba python dependencies from pipx",
        packages=["copier", "invoke", "pre-commit"],
        _sudo=True,
        _use_sudo_login=True,
        _sudo_user=host.data.doodba_user,
    )

    pipx.upgrade_all(
        name="Upgrade all pipx packages",
        _sudo=True,
        _use_sudo_login=True,
        _sudo_user=host.data.doodba_user,
    )
