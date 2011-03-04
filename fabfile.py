from fabric.api import *
from fabric.contrib.files import exists
import os
from time import strftime

path = '/theodo/sflive2011vm/sflive2011'

env.hosts = ['theodo@thor.theodo.fr']
# check read-access to the keys, to be server-independent
keys = ['/home/fabriceb/.ssh/id_rsa', '/var/lib/hudson/.ssh/id_rsa']
env.key_filename = [key for key in keys if os.access(key, os.R_OK)]

def tag_prod():
    tag = "prod/%s" % strftime("%Y/%m-%d-%H-%M-%S")
    local('git tag -a %s -m "Prod"' % tag)
    local('git push --tags')

def install():
    run('mkdir -p ' + path)
    with cd(path):
        run('git clone /git/sflive2011.git .')

def update():
    with cd(path):
        run('git fetch')
        tag = run('git tag -l prod/* | sort | tail -n1')
        run('git checkout ' + tag)

def deploy():
    if not exists(path):
        install()

    tag_prod()
    update()

def rollback(num_revs=1):
    with cd(path):
        run('git fetch')
        tag = run('git tag -l prod/* | sort | tail -n' + str(1 + int(num_revs)) + ' | head -n1')
        run('git checkout ' + tag)
