Örnek proje template dosyasından aşağıdaki komutla kurulur:

```bash
$ django-admin.py startproject myproject -e py,conf,json,js,sample --template=https://github.com/omerucel/django-project-template/archive/master.zip
```

# Özel Ayarlar

## vagrant/Vagrantfile

- **$web_server_ip** : Proje için ip adresi
- **$vagrant_module_path** : vagrant-shell-modules projesi yolu.

# Vagrant

```bash
(local)$ cd vagrant
(local)$ vagrant up
(local)$ vagrant ssh
(vagrant)$ source /home/vagrant/pythonproject/bin/activate
(vagrant)$ easy_install -U distribute
(vagrant)$ cd /vagrant
(vagrant)$ pip install -r requirements.txt
```

# Database & Server

Vagrant ayarlandıktan sonra, proje ile çalışmak için aşağıdaki komutları çalıştırabilirsiniz. Bu komutlar öncesinde **project_name/settings.py**, **project_name/settings_development.py**, **project_name/settings_stage.py** ayar dosyaları projeye göre düzenlenmeli.

```bash
(local)$ cp project_name/settings_development.py.sample project_name/settings_development.py
(local)$ cp project_name/settings_stage.py.sample project_name/settings_stage.py
(local)$ cd vagrant
(local)$ vagrant up
(local)$ vagrant ssh
(vagrant)$ mysql -u root -p -e "CREATE DATABASE project_name CHARACTER SET utf8 COLLATE utf8_general_ci;"
(vagrant)$ fab development syncdb
(vagrant)$ fab development init_migration
(vagrant)$ fab development migrate
(vagrant)$ fab development runserver
```
# Fabfile

Fabfile dosyasında hem deployment için hem de veritabanı senkronizasyonu için komutlar bulunur. Örneğin model dosyanızda bir değişiklik olmuşsa, aşağıdaki komutları sırasıyla çalıştırmanız gerekir:

```bash
(vagrant)$ fab development check_migration
(vagrant)$ fab development migrate
```

# Deployment

Aşağıdaki komutla, aws üzerinde açık olan bir sunucuya gerekli kurulumları yapıp sistemin çalışmasını sağlayabilirsiniz:

```bash
(local)$ fab stage deploy
```

fabfile.py dosyasında development, stage ve production profilleri eklendi. Bunlardan stage profilinde, deploy işleminden önce kendi ayarlarınızı düzenlemeniz gerekmekte.

# Sass

Sass dosyalarının otomatik olarak derlenmesi için aşağıdaki komut ayrı terminal ekranında çalıştırılabilir. sass klasörü içinde olası bir değişiklik sonrası **project_name/static/app.css** dosyası yeniden oluşturulur.

(local)$ npm install
(local)$ grunt watch