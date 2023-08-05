# coding: utf-8

from pyinfra.api import FactBase


class NginxVersion(FactBase):
    '''
    Returns the nginx version installed.
    '''

    def command(self):
        return "nginx -v 2>&1"

    def process(self, output):
        return str(output[0].split('/')[1].split()[0]).strip()


class NodeVersion(FactBase):
    """get odoo version"""

    def command(self):
        return "node --version"

    def process(self, output):
        return output[0].strip()


class PythonVersion(FactBase):
    """get python version"""

    def command(self):
        return 'cat /usr/local/lib/pyenv/_pyenv/version'

    def process(self, output):
        return output[0].strip()


class UwsgiVersion(FactBase):
    '''
    Returns the uwsgi version installed.
    '''

    def command(self):
        return "uwsgi --version"

    def process(self, output):
        return str(output[0]).strip()
