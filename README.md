**Happy School**
================

Objectif
========

Ce document est destiné à l’installation et la mise en place de
l’application HappySchool, il s’agira de la mise en œuvre de
l’environnement de développement ainsi que la mise en fonctionnement du
serveur web afin de rendre fonctionnel les différentes applications
d’HappySchool.

Prérequis
=========

Happy School a été prévu pour fonctionner sur le plus d'environnement
possible, il peut donc techniquement tourner sur Windows, OSX, linux.
Cependant, il a été activement développé sous linux et c'est donc ce
type système d'exploitation, et en particulier Ubuntu qui est recommandé
et qui sera utilisé dans ce manuel.

**Configuration minimale : **

- Ubuntu 16.04 (sans interface graphique)
- 1GO de mémoire vive

**Configuration recommandée :**

- Ubuntu 16.04
- 2GO de mémoire vive

Installation
============

Il y a deux types d'installations, une pour le développement et une
pour la mise en production.

Installation de l’environnement de développement
------------------------------------------------
**Base de donnée**

Happy School utilise une base de donnée *postgresql* avec une extension
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

**Paquets système**

Happy School utilise principalement du python pour fonctionner mais pas
seulement. Il utilise `git` pour la collecte et les mises à jour du code, un
serveur `redis` pour communiquer entre différents processus.

Pour les installer :
```
sudo apt install python-dev libldap2-dev libsasl2-dev libssl-dev python3-pip git python3-dateutil ttf-bitstream-vera redis-server
```

**NodeJS**
Une partie de l'interface, et à terme toute l'interface, est en javascript.
Elle utilise le framework [Vue.js](https://vuejs.org/) et a besoin d'être
transformé pour être lisible et légère pour le navigateur client.
Pour cela, Happy School utilise *webpack* qui s'installe avec [Node.js](https://nodejs.org/en/)
à travers *npm*. Pour installer une version récente :
```
curl -sL https://deb.nodesource.com/setup\_8.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Django et paquets python**

Happy School s'appuie sur le framework [Django](https://www.djangoproject.com/)
ainsi que toutes une série de modules python. Pour les installer :
```
sudo pip3 install django django-crispy-forms z3c.rml django_auth_ldap ldap3 unidecode coverage celery django-webpack-loader djangorestframework channels psycopg2-binary django-filter asgi_redis channels_redis
```
À noter que l'installation se fait sur le système tout entier, pour gérer
différentes versions il est alors mieux d'utiliser `virtualenv` ou apparenté.

Par ailleurs, Happy School utilise son propre système de widget pour le
calendrier. Même s'il est en cours de remplacement, il est encore
nécessaire de l'installer. Pour cela, la commande suivante va télécharger
le code dans le dossier courant puis l'installer :
```
git clone https://github.com/Supermanu/django-bootstrap3-datetimepicker && cd django-bootstrap3-datetimepicker && sudo python3 setup.py install && cd ..
```

**Happy School**

Le code d'Happy School est disponible sur [github](https://github.com/ISLNamur/happyschool.git).
Pour l'installer, placez-vous dans le dossier où vous vous voulez l'installer
puis récupérer le code avec git :
```
cd /home/user/mon/dossier
git clone https://github.com/ISLNamur/happyschool.git
```
Il existe plusieurs niveaux de configurations pour Happy School, le plus
bas niveau est `happyschool/settings.py` (chemin relatif au dossier racine
d'Happy School). Un fichier exemple est disponible et peut être copié :
```
cp happyschool/settings.example.py happyschool/settings.py
```
Dans celui-ci vous retrouverez la possibilité d'activer/désactiver une
application, configurer l'accès à la base de donnée, configurer le
serveur d'envoi d'email, configurer authentification pour un serveur
LDAP/ActiveDirectory, etc.

Pour installer les dépendances javascript et les compiler, dans le dossier
racine (cela peut prendre un peu de temps):
```
npm install
./node_modules/.bin/webpack --config webpack.dev.js
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
---------------------------------------------
En cours d'écriture…

Configuration
=============

En cours d'écriture…
