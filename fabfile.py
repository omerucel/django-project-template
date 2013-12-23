#-*- coding: utf-8 -*-

from fabric.api import *
from fabric.contrib.files import exists

import time
timestamp = int(time.time())

### TOOLS ###

def remove_pyc():
    local('find . -name "*.pyc" -exec rm -rf {} \;')

def create_archive():
    local('git archive --format=zip --output=/tmp/%s.zip master' %(timestamp))

### Profiles ###

def development():
    env.django_settings_module = '{{ project_name }}.settings_development'

def stage():
    env.user = 'ubuntu'
    env.hosts = []
    env.key_filename = '/Users/omer/linux.pem'

    env.release_dir = '/home/ubuntu/{{ project_name }}'
    env.current_release_dir = '%s/%s' %(env.release_dir, timestamp)
    env.project_env_home = '/home/ubuntu/{{ project_name }}env'

    env.project_env_bin = '%s/bin' %(env.project_env_home)
    env.pip_bin = '%s/pip-2.7' %(env.project_env_bin)
    env.uwsgi_bin = '%s/uwsgi' %(env.project_env_bin)
    env.python_bin = '%s/python' %(env.project_env_bin)

    env.uwsgi_pid_file = '%s/uwsgi.pid' %(env.release_dir)
    env.uwsgi_log_file = '%s/uwsgi.log' %(env.release_dir)

    env.module_name = '{{ project_name }}.wsgi:application'
    env.django_settings_module = '{{ project_name }}.settings_stage'

    env.nginx_vhost_file = '%s/current/stage_vhost.conf' %(env.release_dir)

def production():
    pass

###

def syncdb():
    with shell_env(DJANGO_SETTINGS_MODULE=env.django_settings_module):
        local('python manage.py syncdb')

def init_migration():
    with shell_env(DJANGO_SETTINGS_MODULE=env.django_settings_module):
        local('python manage.py schemamigration {{ project_name }} --initial')

def migrate():
    with shell_env(DJANGO_SETTINGS_MODULE=env.django_settings_module):
        local('python manage.py migrate {{ project_name }}')

def dev_check_migration():
    with shell_env(DJANGO_SETTINGS_MODULE=env.django_settings_module):
        local('python manage.py schemamigration {{ project_name }} --auto')

def runserver():
    with shell_env(DJANGO_SETTINGS_MODULE=env.django_settings_module):
        local('python manage.py runserver 0.0.0.0:8080')

def collectstatic():
    with shell_env(DJANGO_SETTINGS_MODULE=env.django_settings_module):
        local('mkdir static')
        local('cd static && python ../manage.py collectstatic')

### DEPLOYMENT ###

def deploy():
    # Sunucuda gerekli kurulumları yap.
    sudo('apt-get -y install nginx python-pip python-virtualenv unzip gcc python-dev libmysqlclient-dev')
    if exists(env.project_env_home) == False:
        run('virtualenv --distribute %s' %(env.project_env_home))

    # Projeyi arşivle ve sunucuya gönder.
    create_archive()
    archive_file = '/tmp/%s.zip' %(timestamp)
    put(archive_file, archive_file)
    local('rm -rf %s' %(archive_file))

    # Proje dizinini oluştur.
    run('mkdir -p %s' %(env.current_release_dir))
    with cd(env.current_release_dir):
        run('unzip %s -d %s' %(
            archive_file,
            env.current_release_dir
        ))
        run('rm -rf %s' %(archive_file))
        run('%s install -r requirements.txt' %(env.pip_bin))

    current_dir = '%s/current' %(env.release_dir)
    run('rm -f %s' %(current_dir))
    run('ln -s %s %s' %(env.current_release_dir, current_dir))

    restart()

def restart():
    current_dir = '%s/current' %(env.release_dir)
    if exists(current_dir) == False:
        raise SystemExit('current directory not found.')

    with cd(current_dir), shell_env(DJANGO_SETTINGS_MODULE=env.django_settings_module):
        if exists(env.uwsgi_pid_file):
            if run('ls %s' %(env.uwsgi_pid_file), quiet=True).succeeded:
                try:
                    run('kill -INT `cat %s`' %(env.uwsgi_pid_file))
                    time.sleep(3)
                except SystemExit:
                    pass
            run('rm -f %s' %(env.uwsgi_pid_file))

        run('%s manage.py syncdb' %(env.python_bin))
        run('%s manage.py migrate {{ project_name }}' %(env.python_bin))
        run('%s --chdir=%s --module=%s --env DJANGO_SETTINGS_MODULE=%s --master --pidfile=%s --socket=127.0.0.1:8000 --processes=5 --daemonize=%s' %(
            env.uwsgi_bin,
            current_dir,
            env.module_name,
            env.django_settings_module,
            env.uwsgi_pid_file,
            env.uwsgi_log_file
        ))

    if exists('/etc/nginx/sites-enabled/default', use_sudo=True):
        sudo('rm -rf /etc/nginx/sites-enabled/default')

    sudo('rm -f /etc/nginx/sites-enabled/vhost.conf')
    sudo('ln -s %s /etc/nginx/sites-enabled/vhost.conf' %(env.nginx_vhost_file))
    sudo('service nginx restart')