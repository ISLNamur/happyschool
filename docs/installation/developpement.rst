.. _installation_developpement:

Développement
************************************************

HappySchool propose deux solutions pour installer un environnement de
développement. Soit par une image Docker, soit par une installation manuelle.

Docker
======
`Docker <https://fr.wikipedia.org/wiki/Docker_(logiciel)>`__ est une solution
de conteneurisation qui permet d'embarquer tous les logiciels nécessaire au
bon fonctionnement d'HappySchool, il peut être vu comme une solution *légère*
de virtualisation. Il permet ainsi de lancer HappySchool de manière
indépendante par rapport au système.

Prérequis
---------

La première étape est donc d'`installer
<https://docs.docker.com/engine/install/>`__ Docker et `docker-compose 
<https://docs.docker.com/compose/install/>`__. Par exemple, sur ubuntu la
commande suivante devrait installer les deux logiciels.

::

   sudo apt install docker.io docker-compose

HappySchool
-----------

L'étape suivante est de télécharger le code d'HappySchool avec le logiciel git.
La commande suivante va télécharger et créer un dossier happyschool avec la
dernière version d'HappySchool dans le répertoire courant.

::

   git clone https://github.com/ISLNamur/happyschool

Il faut ensuite préparer le fichier de configuration d'HappySchool. Placez-vous
dans le nouveau dossier ``happyschool`` et créer votre fichier de configuration
à partir du fichier exemple avec la commande suivante.

::

   cp happyschool/settings.example.py happyschool/settings.py

Construire les images docker
----------------------------

Tout est maintenant prêt pour créer les conteneurs avec la commande suivante.
Par défaut dans ubuntu, la commande ``docker`` doit être utilisé avec les
droits administrateurs d'où l'utilisation de ``sudo`` dans les prochaines
commandes.

::

   sudo docker-compose build --no-cache --force-rm

Démarrer les images
-------------------

Pour démarrer les images dockers, il nous reste plus qu'à lancer :

::

   sudo docker-compose up

Vous pouvez maintenant accéder à HappySchool sur http://127.0.0.1:8000 et
vous connecter avec l'utilisateur `admin` et le mot de passe `admin`.

Si vous voulez accéder au conteneur pour créer/appliquer une migration django
ou bien pour générer le code javascript. La commande suivante vous-y donnera
accès (vous pouvez faire ``sudo docker ps`` pour voir quelles sont les
conteneurs actifs à accéder).

::

   sudo docker exec -ti happyschool-django-1 bash


Les commandes utiles à lancer dans le conteneur sont :

::

   # Regénère le code javascript au moindre changement.
   uv run npm run dev -- --host

   # Démarre celery pour gérer les tâches asynchrones.
   uv run celery -A happyschool worker -l info

Mises à jour
------------

Pour mettre à jour les dépendances (python et js), il suffit de reconstruire
l'image docker et de relancer :

::
   sudo docker-compose up --build

Installation manuelle
=====================

Base de donnée
--------------

Happyschool utilise une base de donnée *postgresql* avec une extension
pour gérer les caractères accentués.

Pour l’installer :

::

   sudo apt install postgresql postgresql-contrib


Ensuite il faut créer un utilisateur et une base de donnée. Accéder au
shell ``psql``:

::

   sudo -u postgres bash -c "psql"

Et introduire les commandes SQL suivantes en spécifiant utilisateur, mot
de passe et nom de la base de donnée :

::

   CREATE USER newuser WITH PASSWORD 'yourpassword';
   CREATE DATABASE mydb WITH OWNER newuser;
   ALTER USER newuser CREATEDB;
   \quit

Paquets système
---------------

Happyschool utilise principalement du python pour fonctionner mais pas
seulement. Il utilise entre autres ``git`` pour la collecte et les mises
à jour du code et un serveur ``redis`` pour communiquer entre différents
processus.

Pour les installer :

::

   sudo apt install curl
   curl -sL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
   sudo apt install libldap2-dev libsasl2-dev python3-pip git python3-dateutil ttf-bitstream-vera redis-server build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev nodejs libcairo2-dev
   

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
de modules python. Afin des les gérer ainsi que leur versions, *uv*                                           
est utilisé. Pour l'installer avec un shell bash :

::

   curl -LsSf https://astral.sh/uv/install.sh | sh                                                                                          
   uv sync


Il existe plusieurs niveaux de configurations pour Happyschool, le plus
bas niveau est ``happyschool/settings.py`` (chemin relatif au dossier
racine d’Happyschool). Un fichier exemple est disponible et peut être copié :

::

   cp happyschool/settings.example.py happyschool/settings.py

Dans celui-ci vous retrouverez la possibilité d’activer/désactiver les
applications, configurer l’accès à la base de donnée (pensez à mettre le
nom de la db, l’utilisateur et le mot de passe définit plus haut !),
configurer le serveur d’envoi d’email, configurer l'authentification à
un serveur LDAP/ActiveDirectory, etc. Plus de détails sont disponibles
dans la section :ref:`configuration_index`.

Pour installer les dépendances javascript et les compiler, dans le
dossier racine (cela peut prendre un peu de temps):

::

   npm install
   uv run npm run dev

Pour écrire les schémas dans la base de donnée :

::

   uv run ./manage.py migrate

Certaines applications ont besoin que les groupes soient déjà
accessibles pour pouvoir fonctionner. La commande suivante permet de les
générer à partir du fichier ``happyschool/settings.py``:

::

   uv run ./manage.py creategroups

Vous pouvez créer un super utilisateur en répondant aux questions posées
par :

::

   uv run ./manage.py createsuperuser

Finalement, pour la lancer le serveur de test :

::

   uv run ./manage.py runserver

HappySchool devrait maintenant être accessible à l’adresse suivante:
`<http://127.0.0.1:8000>`_. La prochaine étape est la
:ref:`configuration_index` d'Happyschool.
