.. _configuration_settingspy:


settings.py
===========

Ce fichier python se situe dans le dossier ``happyschool`` et **doit**
être configuré pour assurer le bon fonctionnement d’Happyschool.

-  ``SECRET_KEY`` est utilisé pour la protection des mots de passes. Si
   vous utilisez directement le système d’authentification de django
   (sans passer par un serveur LDAP/ActiveDirectory) vous **devez**
   générer vous-même une clé aléatoire.
-  ``DEBUG`` comme son nom l’indique permet d’afficher des informations
   de … debug lorsqu’il y a une erreur. À mettre sur ``True`` uniquement
   lorsque vous développez.
-  ``ALLOWED_HOSTS`` indique l’ip ou le nom de domaine avec lequel les
   utilisateurs se connectent. Vous pouvez utiliser un joker comme ceci
   ``ALLOWED_HOSTS = ['*']``.
-  ``INSTALLED_APPS`` est la liste des applications installées. Par
   défaut, seul l’annuaire est activé. Il vous suffit de décommenter les
   applications que vous désirez (n’oubliez pas d’effectuer la
   création/migration de la base de donnée si vous ajoutez une
   application).
-  ``DATABASES`` vous permet de configurer l’accès à votre base de
   donnée, vous pouvez ainsi spécifier le nom de la base de donnée
   (``NAME``), l’utilisateur (``USER``) et le mot de passe
   (``PASSWORD``) pour y accéder.
-  ``AUTHENTICATION_BACKENDS`` reprend tous les types de système
   d’authentification. Par défaut, le *backend* LDAP et le *backend*
   intégré à django sont activés.
-  ``LOCAL_DOMAIN``, ``REMOTE_DOMAIN`` sont utilisées dans le cas où
   vous disposez d’une instance locale avec des données confidentielles
   et instance sur internet pour la notification et réponse à l’envoi de
   courriels.
-  ``EMAIL_ADMIN`` est le courriel de l’administrateur. Il est
   principalement utilisé pour tout ce qui debug et administration.
-  ``EMAIL_HOST``, ``EMAIL_PORT``, ``EMAIL_HOST_USER``,
   ``EMAIL_HOST_PASSWORD``, ``EMAIL_FROM`` pour la configuration du
   serveur d’envoi du courriel. Il n’est pas utilisé pour l’envoi de
   masse avec l’application ``mail_notification``.
-  Les variables ``****_GROUP`` font correspondre le nom des groupes
   utilisés dans Happyschool et ceux dans le serveur
   LDAP/ActiveDirectory.
-  ``USE_LDAP_INFO`` active la prise en compte de l’utilisation d’un
   serveur LDAP/ActiveDirectory.
-  ``LDAP_HOST`` et ``LDAP_DOMAIN`` renseignent le serveur
   LDAP/ActiveDirectory.
-  ``AUTH_LDAP_***`` permettent de configurer l’accès au serveur
   LDAP/ActiveDirectory et sont utilisées par
   `django-auth-ldap <https://django-auth-ldap.readthedocs.io/en/latest/>`__.
-  ``MAILGUN_KEY`` et ``SPARKPOST_KEY``. Mailgun et Sparkpost sont pour
   le moment les deux services supportés pour l’envoi de masse de
   courriels. Ces deux variables vous permettent de configurer votre
   accès à ces services.
-  ``MEDIA_SYNC`` est la commande de synchronisation entre le serveur
   local et distant pour les pièces jointes des courriels.
-  ``MAIL_ANSWER`` est la commande de synchronisation entre les modèles
   du serveur local et distant.
-  ``SYNC_FDB`` active la synchronisation de ProEco avec libreschoolfdb.
