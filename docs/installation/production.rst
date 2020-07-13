.. _installation_production:

Production
*********************************************

La manière la plus rapide et la plus simple est d'utiliser un playbook ansible
pour automatiser l'installation et la configuration d'HappySchool. Cependant
celle-ci se limite à ubuntu 18.04. Pour une installation sur un autre système
ou plus poussé, une installation manuelle est décrite ci-dessous.

Ansible
=======

`Ansible <https://www.ansible.com/>`__ est un outil puissant qui permet
d'automatiser l'installation et la configuration d'un ou plusieurs serveurs.
En règle générale, il s'utilise à distance à travers une session *ssh* vers
le ou les serveurs mais peut très bien s'utiliser en local. Un *playbook*
pour installer HappySchool est disponible pour n'importe quelle utilisation.
Un script *shell* est également fourni pour faciliter l'installation en local.
Pour télécharger le playbook clonez le dépôt correspondant:

::

   git clone https://github.com/ISLNamur/happyschool-ansible

Le fichier de configuration (superutilisateur, applications actives, etc) se
trouve dans ``vars/custom.yml``, modifiez-le à votre convenance. Ensuite, à
la racine du dépôt exécutez le script suivant:

::

   ./recipe.sh

Celui-ci devrait vous demander votre mot de passe pour l'installation des
paquets système. Au final, HappySchool sera installé dans
``/home/utilisateur/happyschool``.

Installation manuelle
=====================

Base de donnée
--------------

Happyschool utilise une base de donnée *postgresql* avec une extension
pour gérer les caractères accentués.

Pour l’installer :

::

   sudo apt install postgresql postgresql-contrib

Pour activer l’extension pour toutes les futures base de données :

::

   sudo -u postgres bash -c "psql -U postgres -d 'template1' -c 'CREATE EXTENSION unaccent;'"

Puis créer un utilisateur et une base de donnée. D’abord accéder au
shell ``psql``:

::

   sudo -u postgres bash -c "psql"

Et introduire les commandes SQL suivantes en spécifiant utilisateur, mot
de passe et nom de la base de donnée :

::

   CREATE USER newuser WITH PASSWORD 'yourpassword';
   CREATE DATABASE mydb WITH OWNER newuser;
   \quit

.. _paquets-système-1:

Paquets système
---------------

Happyschool utilise principalement du python pour fonctionner mais pas
seulement. Il utilise entre autres ``git`` pour la collecte et les mises
à jour du code et un serveur ``redis`` pour communiquer entre différents
processus.

Pour les installer :

::

   sudo apt install python3.7 python3.7-dev libldap2-dev libsasl2-dev libssl1.0-dev python3-pip git python3-dateutil ttf-bitstream-vera redis-server npm nginx

.. _happyschool-1:

HappySchool
-----------

Le code d’Happyschool est disponible sur
`github <https://github.com/ISLNamur/happyschool.git>`__. Pour
l’installer, placez-vous dans le dossier où vous vous voulez l'installer
puis récupérer le code avec git :

::

   cd /home/user/mon/dossier
   git clone https://github.com/ISLNamur/happyschool.git

HappySchool s’appuie sur le framework
`Django <https://www.djangoproject.com/>`__ ainsi que toutes une série
de modules python. Pour les installer :

::

   pip3 install --user pipenv
   cd happyschool
   pipenv install


Il existe plusieurs niveaux de configurations pour Happyschool, le plus
bas niveau est ``happyschool/settings.py`` (chemin relatif au dossier
racine d’Happyschool). Un fichier exemple est disponible et peut être copié :

::

   cp happyschool/settings.example.py happyschool/settings.py

Dans celui-ci vous retrouverez la possibilité d’activer/désactiver une
application, configurer l’accès à la base de donnée (pensez à mettre le
nom de la db, l’utilisateur et le mot de passe définit plus haut),
configurer le serveur d’envoi d’email, configurer l'authentification à
un serveur LDAP/ActiveDirectory, etc. Plus de détails sont disponibles
dans la section :ref:`configuration_index`.

Pour installer les dépendances javascript et les compiler, dans le
dossier racine (cela peut prendre un peu de temps):

::

   npm install
   ./node_modules/.bin/webpack --config webpack.dev.js

Pour écrire les schémas dans la base de donnée :

::

   pipenv run ./manage.py migrate

Certaines applications ont besoin que les groupes soient déjà
accessibles pour pouvoir fonctionner. La commande suivante permet de les
générer à partir du fichier ``happyschool/settings.py``:

::

   pipenv run ./manage.py creategroups

Vous pouvez créer un super utilisateur en répondant aux questions posées
par :

::

   pipenv run ./manage.py createsuperuser

Ensuite récupérez les fichiers statiques (css,…) utilisés par django et
ses applications. Pour cela, assurez-vous que ``DEBUG = FALSE`` dans
votre fichier ``happyschool/settings.py`` et lancez la commande suivante
:

::

   python3 manage.py collectstatic


Supervisord
-----------

`Supervisord <http://supervisord.org/>`__ est un système de gestion des
processus. Il a pour but de coordoner le (re)démarrage et l’arrêt des
différents processus utilisés pour le bon fonctionnement d’Happyschool.
Il s’installe avec ``pip`` :

::

   sudo pip3 install supervisor

*Supervisor* se configure avec le fichier ``/etc/supervisord.conf`` (à
créer) :

::

    [unix_http_server]
    file=/tmp/supervisor.sock

    [supervisord]
    logfile=/var/log/supervisord.log ; main log file
    logfile_maxbytes=20MB
    pidfile=/tmp/supervisord.pid

    [rpcinterface:supervisor]
    supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

    [supervisorctl]
    serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL for a unix socket

    [program:daphne]
    command=/home/user/.local/bin/pipenv run daphne -b 0.0.0.0 -p 8080 happyschool.asgi:application
    directory=/home/path/to/happyschool
    autorestart=true
    environment=HOME=“/home/user”,USER=“user” ; directory to

    [program:celery]
    command=/home/user/.local/bin/pipenv run celery -A happyschool worker -l info
    directory=/home/path/to/happyschool autostart=true
    autorestart=true
    environment=HOME="/home/user",USER="user"

Vérifiez que les chemins d’accès à
Happyschool ainsi que le nom d’utilisateur sont correctement configurés.

Pour s’assurer que supervisor est bien lancé au démarrage de la machine,
vous pouvez créer un service dans
``/etc/systemd/system/supervisord.service``:

::

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

Que vous pouvez activer avec

::

   sudo systemctl enable supervisord
   sudo systemctl start supervisord

Nginx
-----

`Nginx <https://www.nginx.com/>`__ va nous permettre de répartir les
différentes demandes entre les contenus dynamiques que va gérer daphne,
et les contenus statiques (images, css, js,…). Il s’installe simplement
avec :

::

   sudo apt install nginx

Ensuite pour le configurer, modifiez le fichier
``/etc/nginx/sites-available/default``:

::

   server {
           listen 80 default_server;
           listen [::]:80 default_server;
           server_name mon.domaine 10.32.141.6; # Nom de domaine du serveur, l'ip n'est pas nécessaire. À MODIFIER.
           client_max_body_size 100m;

           location /static/ {
                    add_header Service-Worker-Allowed "/";
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

Pour vérifier qu’il n’y a pas de faute de syntaxe, la commande
``sudo nginx -t`` est bien utile. Ensuite pour charger la nouvelle
configuration :

::

   sudo systemctl reload nginx

Happyschool devrait maintenant être accessible à l’adresse IP ou au nom
de domaine que vous avez choisi. La prochaine étape est la
:ref:`configuration_index` Happyschool que ce soit pour
l’envoi automatique des courriels ou pour le choix des applications.
