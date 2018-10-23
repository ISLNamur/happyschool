Prérequis
=========

Happyschool a été prévu pour fonctionner sur le plus d'environnement
possible, il peut donc techniquement tourner sur Windows, OSX, linux.
Cependant, il a été activement développé sous linux et c'est donc ce
type système d'exploitation, et en particulier Ubuntu qui est recommandé
et qui sera utilisé dans ce manuel.

**Configuration minimale :**

- Ubuntu 16.04 (sans interface graphique)
- 1GO de mémoire vive

**Configuration recommandée :**

- Ubuntu 16.04
- 2GO de mémoire vive

Il y a deux types d'installations, une pour le développement et une
pour la mise en production.

Installation de l’environnement de développement
================================================
Base de donnée
--------------

Happyschool utilise une base de donnée *postgresql* avec une extension
pour gérer les caractères accentués.

Pour l'installer :
```
sudo apt install postgresql postgresql-contrib
```
Pour activer l'extension pour toutes les futures base de données :
```
sudo -u postgres bash -c "psql -U postgres -d 'template1' -c 'CREATE EXTENSION unaccent;'"
```
Puis créer un utilisateur et une base de donnée. D'abord accéder au shell `psql`:
```
sudo -u postgres bash -c "psql"
```
Et introduire les commandes SQL suivantes en spécifiant utilisateur, mot
de passe et nom de la base de donnée :
```
CREATE USER newuser WITH PASSWORD 'yourpassword';
CREATE DATABASE mydb WITH OWNER newuser;
\quit
```

Paquets système
---------------

Happyschool utilise principalement du python pour fonctionner mais pas
seulement. Il utilise entre autres `git` pour la collecte et les mises à
jour du code et un serveur `redis` pour communiquer entre différents processus.

Pour les installer :
```
sudo apt install python-dev libldap2-dev libsasl2-dev libssl-dev python3-pip git python3-dateutil ttf-bitstream-vera redis-server
```

NodeJS
------
Une partie de l'interface, et à terme toute l'interface, est en javascript.
Elle utilise le framework [Vue.js](https://vuejs.org/) et a besoin d'être
transformée pour être lisible et allégée pour le navigateur client.
Pour cela, Happyschool utilise *webpack* qui s'installe avec [Node.js](https://nodejs.org/en/)
à travers *npm*. Pour installer une version récente :
```
curl -sL https://deb.nodesource.com/setup\_8.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Happyschool
------------

Le code d'Happyschool est disponible sur [github](https://github.com/ISLNamur/happyschool.git).
Pour l'installer, placez-vous dans le dossier où vous vous voulez le mettre
puis récupérer le code avec git :
```
cd /home/user/mon/dossier
git clone https://github.com/ISLNamur/happyschool.git
```

Happyschool s'appuie sur le framework [Django](https://www.djangoproject.com/)
ainsi que toutes une série de modules python. Pour les installer :
```
sudo pip3 install -r happyschool/requirements.txt
```
À noter que l'installation se fait sur le système tout entier, pour gérer
différentes versions il est alors mieux d'utiliser `virtualenv` ou apparenté.

Il existe plusieurs niveaux de configurations pour Happyschool, le plus
bas niveau est `happyschool/settings.py` (chemin relatif au dossier racine
d'Happyschool, faire `cd happyschool` pour vous y rendre). Un fichier exemple
est disponible et peut être copié :
```
cp happyschool/settings.example.py happyschool/settings.py
```
Dans celui-ci vous retrouverez la possibilité d'activer/désactiver une
application, configurer l'accès à la base de donnée (pensez à mettre le
nom de la db, l'utilisateur et le mot de passe définit plus haut), configurer le
serveur d'envoi d'email, configurer authentification pour un serveur
LDAP/ActiveDirectory, etc. Plus de détails sont disponibles dans la section
[Configuration](configuration.md).

Pour installer les dépendances javascript et les compiler, dans le dossier
racine (cela peut prendre un peu de temps):
```
npm install
./node_modules/.bin/webpack --config webpack.dev.js
```

Pour écrire les schémas dans la base de donnée :
```
python3 manage.py makemigrations
python3 manage.py migrate
```
Certaines applications ont besoin que les groupes soient déjà accessibles pour
pouvoir fonctionner. La commande suivante permet de les générer à partir
du fichier `happyschool/settings.py`:
```
python3 manage.py creategroups
```
Vous pouvez créer un super utilisateur en répondant aux questions posées par :
```
python3 manage.py createsuperuser
```
Finalement, pour la lancer le serveur de test :
```
python3 manage.py runserver
```
Installation de l’environnement de production
=============================================
Base de donnée
--------------

Happyschool utilise une base de donnée *postgresql* avec une extension
pour gérer les caractères accentués.

Pour l'installer :
```
sudo apt install postgresql postgresql-contrib
```
Pour activer l'extension pour toutes les futures base de données :
```
sudo -u postgres bash -c "psql -U postgres -d 'template1' -c 'CREATE EXTENSION unaccent;'"
```
Puis créer un utilisateur et une base de donnée. D'abord accéder au shell `psql`:
```
sudo -u postgres bash -c "psql"
```
Et introduire les commandes SQL suivantes en spécifiant utilisateur, mot
de passe et nom de la base de donnée :
```
CREATE USER newuser WITH PASSWORD 'yourpassword';
CREATE DATABASE mydb WITH OWNER newuser;
\quit
```

Paquets système
---------------

Happyschool utilise principalement du python pour fonctionner mais pas
seulement. Il utilise entre autres `git` pour la collecte et les mises à
jour du code et un serveur `redis` pour communiquer entre différents processus.

Pour les installer :
```
sudo apt install python-dev libldap2-dev libsasl2-dev libssl-dev python3-pip git python3-dateutil ttf-bitstream-vera redis-server
```

NodeJS
------
Une partie de l'interface, et à terme toute l'interface, est en javascript.
Elle utilise le framework [Vue.js](https://vuejs.org/) et a besoin d'être
transformé pour être lisible et légère pour le navigateur client.
Pour cela, Happyschool utilise *webpack* qui s'installe avec [Node.js](https://nodejs.org/en/)
à travers *npm*. Pour installer une version récente :
```
curl -sL https://deb.nodesource.com/setup\_8.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Django et paquets python
------------------------

Happyschool s'appuie sur le framework [Django](https://www.djangoproject.com/)
ainsi que toutes une série de modules python. Pour les installer :
```
sudo pip3 install django django-crispy-forms z3c.rml django_auth_ldap ldap3 unidecode coverage celery django-webpack-loader djangorestframework channels psycopg2-binary django-filter asgi_redis channels_redis
```
À noter que l'installation se fait sur le système tout entier, pour gérer
différentes versions il est alors mieux d'utiliser `virtualenv` ou apparenté.

Par ailleurs, Happyschool utilise son propre système de widget pour le
calendrier. Même s'il est en cours de remplacement, il est encore
nécessaire de l'installer. Pour cela, la commande suivante va télécharger
le code dans le dossier courant puis l'installer :
```
git clone https://github.com/Supermanu/django-bootstrap3-datetimepicker && cd django-bootstrap3-datetimepicker && sudo python3 setup.py install && cd ..
```
Happyschool
------------

Le code d'Happyschool est disponible sur [github](https://github.com/ISLNamur/happyschool.git).
Pour l'installer, placez-vous dans le dossier où vous vous voulez le mettre
puis récupérer le code avec git :
```
cd /home/user/mon/dossier
git clone https://github.com/ISLNamur/happyschool.git
```

Happyschool s'appuie sur le framework [Django](https://www.djangoproject.com/)
ainsi que toutes une série de modules python. Pour les installer :
```
sudo pip3 install -r happyschool/requirements.txt
```
À noter que l'installation se fait sur le système tout entier, pour gérer
différentes versions il est alors mieux d'utiliser `virtualenv` ou apparenté.

Il existe plusieurs niveaux de configurations pour Happyschool, le plus
bas niveau est `happyschool/settings.py` (chemin relatif au dossier racine
d'Happyschool, faire `cd happyschool` pour vous y rendre). Un fichier exemple
est disponible et peut être copié :
```
cp happyschool/settings.example.py happyschool/settings.py
```
Dans celui-ci vous retrouverez la possibilité d'activer/désactiver une
application, configurer l'accès à la base de donnée (pensez à mettre le
nom de la db, l'utilisateur et le mot de passe définit plus haut), configurer le
serveur d'envoi d'email, configurer authentification pour un serveur
LDAP/ActiveDirectory, etc. Plus de détails sont disponibles dans la section
[Configuration](configuration.md).

Pour installer les dépendances javascript et les compiler, dans le dossier
racine (cela peut prendre un peu de temps):
```
npm install
./node_modules/.bin/webpack --config webpack.prod.js
```

Pour créer les différents schémas dans la base de donnée, l'utilitaire
`manage.py`, fournit par django, vous permet de facilement le faire :
```
python3 manage.py makemigrations
python3 manage.py migrate
```
Certaines applications ont besoin que les groupes soient déjà accessibles pour
pouvoir fonctionner. La commande suivante permet de les générer à partir
du fichier `happyschool/settings.py`:
```
python3 manage.py creategroups
```
Ensuite récupérez les fichiers statiques (css,…) utilisés par django et ses
applications :
```
python3 manage.py collectstatic
```
Supervisor
----------
[Supervisor](http://supervisord.org/) est un système de gestion des processus.
Il a pour but de coordoner le (re)démarrage et l'arrêt des différents processus
utilisés pour le bon fonctionnement d'Happyschool. Il s'installe avec
`easy_install` :
```
sudo apt install python-setuptools
sudo easy_install supervisor
```
*Supervisor* se configure avec le fichier `/etc/supervisord.conf` (à créer) :
 ```
unix_http_server]
file=/tmp/supervisor.sock   ; the path to the socket file

[supervisord]
logfile=/var/log/supervisord.log ; main log file; default $CWD/supervisord.log
logfile_maxbytes=20MB        ; max main logfile bytes b4 rotation; default 50MB
logfile_backups=10           ; # of main logfile backups; 0 means none, default 10
loglevel=info                ; log level; default info; others: debug,warn,trace
pidfile=/tmp/supervisord.pid ; supervisord pidfile; default supervisord.pid
#nodaemon=false               ; start in foreground if true; default false
minfds=1024                  ; min. avail startup file descriptors; default 1024
minprocs=200                 ; min. avail process descriptors;default 200

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket

[program:daphne]
command=/usr/local/bin/daphne -b 0.0.0.0 -p 8080 happyschool.asgi:application --access-log /var/log/daphne.log
directory=/home/path/to/happyschool           ; directory to cwd to before exec (def no cwd)
autostart=true                ; start at supervisord start (default: true)
autorestart=true        ; when to restart if exited after running (def: unexpected)

[program:celery]
command=celery -A happyschool worker -l info -f /var/log/celery.log
directory=/home/path/to/happyschool
autostart=true
autorestart=true
 ```
 Vérifiez que les chemins d'accès à Happyschool sont correctement configurés.

Pour s'assurer que supervisor est bien lancé au démarrage de la machine,
vous pouvez créer un service dans `/etc/systemd/system/supervisord.service`:
```
[Unit]
Description=Supervisor process control system for UNIX
Documentation=http://supervisord.org
After=network.target

[Service]
ExecStart=/usr/local/bin/supervisord -n -c /etc/supervisord.conf
ExecStop=/usr/local/bin/supervisorctl shutdown
ExecReload=/usr/local/bin/supervisorctl reload
KillMode=process
Restart=on-failure
RestartSec=50s

[Install]
WantedBy=multi-user.target
```
Que vous pouvez activer avec
```
sudo systemctl enable supervisord
sudo systemctl start supervisord
```

Nginx
-----
[Nginx](https://www.nginx.com/) va nous permettre de répartir les différentes
demandes entre les contenus dynamiques que va gérer daphne, et les contenus
statiques (images, css, js,…). Il s'installe simplement avec :
```
sudo apt install nginx
```
Ensuite pour le configurer, modifiez le fichier `/etc/nginx/sites-available/default`:
```
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name mon.domaine 10.32.141.6; # Nom de domaine du serveur, l'ip n'est pas nécessaire. À MODIFIER.
        client_max_body_size 100m;

        location /static/ {
                 alias /home/user/happyschool/static/; # Mettre le chemin vers les fichiers statiques. À MODIFIER.
        }

        location /media/ {
                 alias /home/user/happyschool/media/; # Mettre le chemin vers les fichiers media (upload,…). À MODIFIER.
        }

        location /favicon.ico {
                 alias /home/user/happyschool/static/favicon.ico; # Mettre le chemin correct.
        }

        # On transmet le reste à daphne.
        location / {
                 proxy_pass http://0.0.0.0:8080; # Le port d'écoute de daphne.
                 proxy_set_header Upgrade $http_upgrade;
                 proxy_set_header Connection "upgrade";

                 proxy_redirect     off;
                 proxy_set_header   Host $host;
                 proxy_set_header   X-Real-IP $remote_addr;
                 proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
                 proxy_set_header   X-Forwarded-Host $server_name;
        }
}
```
Pour vérifier qu'il n'y a pas de faute de syntaxe, la commande `sudo nginx -t`
est bien utile. Ensuite pour charger la nouvelle configuration :
```
sudo systemctl reload nginx
```

Happyschool devrait maintenant être accessible à l'adresse IP ou au nom de domaine
que vous avez choisi. La prochaine étape est de [configurer](/docs/configuration.md)
Happyschool que ce soit pour l'envoi automatique des courriels ou pour le choix des
applications.
