import os
from fabric.operations import local as lrun
from fabric.api import *

'''
helpful variables
'''

# name of the package
project = "wit"

# path to git
git = "/usr/bin/git"

# file name
file = project + ".zip"

# pat to deploy to
build_path = "/tmp/build-" + project

# local temp file
tmp_file = "/tmp/" + file


# if available, use ssh config
if env.ssh_config_path and os.path.isfile(os.path.expanduser(env.ssh_config_path)):
    env.use_ssh_config = True


'''
Set up some variables to use locally
'''
@task
def localhost():
  env.run = lrun
  env.hosts = ["localhost"]

'''
Set up some variables to use if connecting remotely
'''
@task
def remote(host):
  env.run = run
  env.hosts = [host]

'''
run the command, this is a wrapper as sudo on localhost is poo
'''
def sudo_run(cmd):
  if env.run is lrun:
    env.run('sudo ' + cmd)
  else:
    sudo(cmd)

'''
package up the client with git archive
'''
def build_package(branch='master', out='/tmp/outfile.zip'):
  # archive the git branch
  local(git + " archive " + branch + " -o " + out)


'''
deploy the client
'''
@task
def deploy(branch='master'):

  # package up the file
  build_package(branch, tmp_file)

  # if we are coppying to the remote server then
  # push the archive to that server
  if env.run is not lrun:
    put(tmp_file)

  # if we are coppying to local then set local path
  # otherwise unzip from where we uploaded the file
  if env.run is lrun:
    sudo_run('unzip -o -u ' + tmp_file + ' -d ' + build_path)
  else:
    sudo_run('unzip -o -u ~/' + file + ' -d ' + build_path)

  # install
  install()

  # clean up any unneeded files
  cleanup()

'''
build deploy project
'''
def install():
  with cd(build_path):
    sudo_run('python setup.py install')


def setpermissions():
  sudo_run('chown -R ' + user + ':' + user + ' ' + deploy_path)


'''
remove any unneeded files
'''
def cleanup():
  local('rm -f ' + tmp_file)
  if env.run is not lrun:
    sudo_run('rm -f ~/' + file)
