# coding: utf-8

from fnmatch import fnmatch
from os import path, walk

from pathlib import Path
from pyinfra.api import operation
from pyinfra.api.exceptions import OperationError
from pyinfra.modules import files, server

file = files.file
directory = files.directory
put = files.put


@operation
def move(state, host, src, dest, add_deploy_dir=True, force=False, mkdir=True, **kwargs):
    """Move a file."""
    kwargs.pop('sudo', None)

    # no source or destination
    if src is None:
        raise OperationError('source not defined')
    if dest is None:
        raise OperationError('destination not defined')

    src_path = Path(state.deploy_dir, src) if add_deploy_dir and state.deploy_dir else Path(src)
    dest_path = Path(dest)
    dest_dir = dest_path.parent

    if not host.fact.directory(dest_dir) and mkdir:
        yield files.directory(
            state, host,
            {f"Make dir {dest_dir}"},
            dest_dir,
            present=True, recursive=True, **kwargs,
            sudo=True
        )

    mv_args = []
    if force:
        mv_args.append('-f')

    yield server.shell(
        state, host,
        {f"Mv {src_path} file to {dest_path}"},
        f"mv {src_path} {dest_path}",
        sudo=True
    )

    if src_path.is_dir():
        yield files.directory(
            state, host,
            {f"Change dir {dest_path} mode"},
            dest,
            recursive=True, **kwargs,
            sudo=True
        )
    else:
        yield files.file(
            state, host,
            {f"Change file {dest_path} mode"},
            dest,
            **kwargs,
            sudo=True
        )


@operation(pipeline_facts={
    'find_files': 'destination',
})
def sync(
        state, host, source, destination,
        user=None, group=None, mode=None, delete=False, exclude=None, exclude_dir=None, add_deploy_dir=True,
):
    '''
    Syncs a local directory with a remote one, with delete support. Note that delete will
    remove extra files on the remote side, but not extra directories.

    + source: local directory to sync
    + destination: remote directory to sync to
    + user: user to own the files and directories
    + group: group to own the files and directories
    + mode: permissions of the files
    + delete: delete remote files not present locally
    + exclude: string or list/tuple of strings to match & exclude files (eg *.pyc)
    '''

    # If we don't enforce the source ending with /, remote_dirname below might start with
    # a /, which makes the path.join cut off the destination bit.
    if not source.endswith(path.sep):
        source = '{0}{1}'.format(source, path.sep)

    # Add deploy directory?
    if add_deploy_dir and state.deploy_dir:
        source = path.join(state.deploy_dir, source)

    # Ensure exclude is a list/tuple
    if exclude is not None:
        if not isinstance(exclude, (list, tuple)):
            exclude = [exclude]

    put_files = []
    ensure_dirnames = []
    for dirname, _, filenames in walk(source):
        remote_dirname = dirname.replace(source, '')

        # Should we exclude this dir?
        if exclude_dir and any(fnmatch(remote_dirname, match) for match in exclude_dir):
            continue

        if remote_dirname:
            ensure_dirnames.append(remote_dirname)

        for filename in filenames:
            full_filename = path.join(dirname, filename)

            # Should we exclude this file?
            if exclude and any(fnmatch(full_filename, match) for match in exclude):
                continue

            put_files.append((
                # Join local as normal (unix, win)
                full_filename,
                # Join remote as unix like
                '/'.join(
                    item for item in
                    (destination, remote_dirname, filename)
                    if item
                ),
            ))

    # Ensure the destination directory
    yield directory(
        state, host, destination,
        user=user, group=group,
    )

    # Ensure any remote dirnames
    for dirname in ensure_dirnames:
        yield directory(
            state, host,
            '/'.join((destination, dirname)),
            user=user, group=group,
        )

    # Put each file combination
    for local_filename, remote_filename in put_files:
        yield put(
            state, host,
            local_filename, remote_filename,
            user=user, group=group, mode=mode,
            add_deploy_dir=False,
        )

    # Delete any extra files
    if delete:
        remote_filenames = set(host.fact.find_files(destination) or [])
        wanted_filenames = set([remote_filename for _, remote_filename in put_files])
        files_to_delete = remote_filenames - wanted_filenames
        for filename in files_to_delete:
            yield file(state, host, filename, present=False)
