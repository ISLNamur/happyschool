Configuration
=============

Happyschool disposent de trois différents niveaux de configuration :
- Le plus bas niveau, dans `happyschool/settings.py`, est la configuration
liée à django et se rapporte à la base de donnée, les applications utilisées,
le serveur de courriel sortant, etc.
- Le niveau intermédiare est simplement des entrées dans la base de donnée. Par
exemple, les types de sanctions ou les motifs des appels.
- Finalement, le plus haut niveau est accessible directement depuis l'interface
web.

settings.py
-----------

Ce fichier python se situe dans le dossier `happyschool` et **doit** être
configuré pour assurer le bon fonctionnement d'Happyschool.

- `SECRET_KEY` est utilisé pour la protection des mots de passes. Si vous utilisez
directement le système d'authentification de django (sans passer par un serveur
LDAP/ActiveDirectory) vous **devez** générer vous-même une clé aléatoire.
- `DEBUG` comme son nom l'indique permet d'afficher des informations de … debug
lorsqu'il y a une erreur. À mettre sur `True` uniquement lorsque vous développez.
- `ALLOWED_HOSTS` indique l'ip ou le nom de domaine avec lequel les utilisateurs se
connectent. Vous pouvez utiliser un joker comme ceci `ALLOWED_HOSTS = ['*']`.
- `INSTALLED_APPS` est la liste des applications installées.