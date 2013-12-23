Projeyi template dosyasından aşağıdaki komutla kurulur:

```bash
$ django-admin.py startproject myproject --e py,conf,json,js,Vagrantfile,sample,html,gitignore --template=https://github.com/omerucel/django-project-template/archive/master.zip
```

# Vagrant

```bash
(local)$ cd vagrant
(local)$ vagrant up
(local)$ vagrant ssh
(vagrant)$ source /home/vagrant/pythonproject/bin/activate
(vagrant)$ easy_install -U distribute
(vagrant)$ pip install -r requirements.txt
```

# Database & Server

Vagrant ayarlandıktan sonra, proje ile çalışmak için aşağıdaki komutları çalıştırabilirsiniz:

```bash
(local)$ cd vagrant
(local)$ vagrant up
(local)$ vagrant ssh
(vagrant)$ fab dev_syncdb
(vagrant)$ fab dev_migrate
(vagrant)$ fab dev_runserver
```
# Fabfile

Fabfile dosyasında hem deployment için hem de veritabanı senkronizasyonu için komutlar bulunur. Örneğin model dosyanızda bir değişiklik olmuşsa, aşağıdaki komutları sırasıyla çalıştırmanız gerekir:

```bash
(vagrant)$ fab dev_check_migration
(vagrant)$ fab dev_migrate
```

# Deployment

Aşağıdaki komutla, aws üzerinde açık olan bir sunucuya gerekli kurulumları yapıp sistemin çalışmasını sağlayabilirsiniz:

```bash
(local)$ fab stage deploy
```

fabfile.py dosyasında development, stage ve production profilleri eklendi. Bunlardan stage profilinde, deploy işleminden önce kendi ayarlarınızı düzenlemeniz gerekmekte.

# Sass

Sass dosyalarının otomatik olarak derlenmesi için aşağıdaki komut ayrı terminal ekranında çalıştırılabilir. sass klasörü içinde olası bir değişiklik sonrası project_name/static/app.css dosyası yeniden oluşturulur.

(local)$ npm install
(local)$ grunt watch