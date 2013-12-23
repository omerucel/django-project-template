Projeyi template dosyasından aşağıdaki komutla kurulur:

```bash
$ django-admin.py startproject myproject --e py,conf,json,js,Vagrantfile,sample,html,gitignore --template=https://github.com/omerucel/django-project-template/archive/master.zip
```

# Adım 1

Ortam için gerekli paketler kurulmalı.

```bash
$ npm install
$ grunt watch
$ source /home/vagrant/pythonproject/bin/activate
$ cd /vagrant
$ easy_install -U distribute
$ pip install -r requirements.txt
```

# Adım 2

Veritabanı oluşturulmalı.

# Adım 3

Veritabanı oluşturulmalı ve sunucu çalıştırılmalı.

```
$ fab dev_syncdb
$ fab dev_migrate
$ fab dev_runserver
```