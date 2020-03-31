.. _installation_developpement:

Installation de l’environnement de développement
************************************************

HappySchool propose deux solutions pour installer un environnement de
développement. Soit par une image Docker, soit par une installation manuelle.

Docker
======

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

Paquets système
---------------

Happyschool utilise principalement du python pour fonctionner mais pas
seulement. Il utilise entre autres ``git`` pour la collecte et les mises
à jour du code et un serveur ``redis`` pour communiquer entre différents
processus.

Pour les installer :

::

   sudo apt install python3.7 python3.7-dev libldap2-dev libsasl2-dev libssl1.0-dev python3-pip git python3-dateutil ttf-bitstream-vera redis-server npm

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

   sudo pip3 install --user pipenv
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

Finalement, pour la lancer le serveur de test :

::

   pipenv run ./manage.py runserver --nostatic

HappySchool devrait maintenant être accessible à l’adresse suivante:
`<http://127.0.0.1:8000>`_. La prochaine étape est la
:ref:`configuration_index` d'Happyschool.
