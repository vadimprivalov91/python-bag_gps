from __future__ import with_statement

from fabric.api import *
from contextlib import contextmanager as _contextmanager
# import paramiko, os
# paramiko.common.logging.basicConfig(level=paramiko.common.DEBUG)
from lamonte import settings, local_settings

env.directory = '/home/nt/lamonte_server'
env.activate = 'source /home/nt/.venv/lamonte/bin/activate'
env.hosts = ['178.62.127.124']
env.port = 2222
env.user = local_settings.FABRIC_USER
env.key_filename = [local_settings.FABRIC_KEYFILE]
env.roledefs = {
    'web': ['178.62.127.124'],
}


@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield


@roles('web')
def sync():
    local('git push')
    with virtualenv():
        run('git checkout master')
        run('git pull')
        run('sudo /usr/sbin/service gunicorn restart')


@roles('web')
def pull():
    with virtualenv():
        run('git checkout master')
        run('git pull')
        run('sudo /usr/sbin/service gunicorn restart')


def full():
    local('git push')
    with virtualenv():
        run('git checkout master')
        run('git pull')
        run('pip install -r r.txt')
        run('python manage.py migrate')
        run('python manage.py collectstatic --noinput')
        run('sudo /usr/sbin/service gunicorn restart')


@roles('web')
def restart():
    with virtualenv():
        run('sudo /usr/sbin/service gunicorn restart')


@roles('web')
def ls():
    run("ls")
