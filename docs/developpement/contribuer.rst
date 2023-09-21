Contribuer
==========

HappySchool est un logiciel libre où chacun peut contribuer. Afin de créer un logiciel
cohérent, il est demandé aux développeurs de suivre toute une série de bonnes pratiques
que ce soit sur le code en lui-même (le style et la cohérence du code), ou encore la
manière dont les patchs sont soumis (git, messages des commits, etc). Ce ne sont pas des
règles à proprement parler, mais des recommandations qui permettent d'établir des repères
techniques et sociaux, une culture somme toute qui n'est ni exacte, ni immuable.

Style du code
-------------

Utiliser `black` pour python et `eslint` pour le javascript. Un linter comme `ruff`
(python) peut être utile pour éviter des erreurs.
Pour utiliser ses outils, il est nécessaire d'avoir un terminal ouvert. Si vous utiliser Docker pour faire tourner le projet alors il faudra vous connecter au container :
::

   sudo docker exec -ti happyschool-django-1 bash


Une fois arrivé dans le terminal, si vous n'avez pas encore installé les packages, lancer la commande suivante :
::

    pipenv install --dev

Cela devrait normalement installer les packages nécessaires et un fichier Pipfile.lock sera créé.


Black
-----
Black est un outils qui permet de formatter le code selon des règles de style.
A chaque modification d'un fichier python dans le projet, il faudra appeler cet outils afin de formatter le code sans quoi cela va provoquer une erreur lors du build de la PR.

Pour formatter le code :

::

    pipenv run black [OPTIONS] SRC 

Par exemple pour formatter le fichier `appels/serializers.py`

::

    pipenv run black appels/serializers.py


eslint
------

Eslint est un outils qui permet de formatter un fichier javascript selon des règles de style. 
La documentation officielle se trouve `ici <https://eslint.org/docs/latest/use/getting-started>`_.
Comme pour black et les fichiers python il faut l'utiliser pour les fichiers javascript modifiés avant de faire sa PR.
Pour s'en servir rien de bien compliqué :
::

    npx eslint fichier_a_formatter.js

Exemple pour le fichier `assets/js/members.js`

::

    npx eslint assets/js/members.js

On peut aussi formatter tous les fichiers javascript d'un répertoire. Par exemple si on veut formatter tous les fichiers javascript du répertoire `assets/js` :

::

    npx eslint assets/js/*


ruff
----

Ruff est un linter et à la différence de black, il permet de détecter aussi les éventuelles erreurs et problèmes dans le code.
Pour l'utiliser :

::

    pipenv run ruff SRC 

Par exemple pour linter tous les fichiers python dans le dossier `appels`

::

    pipenv run ruff appels/*

Plus d'info dans la `documentation officielle <https://github.com/astral-sh/ruff>`_


Git et les commits
------------------

autocrlf
--------
La configuration `autocrlf` doit être mise à false sinon git va d'office mettre CRLF en fin de chaque fichier :

::

    git config core.autocrlf false

Pour vérifier la configuration :

::

    git config core.autocrlf


Règles pour créer une PR
------------------------

1) Un seul commit doit figurer dans l'historique de la branche.
Si plusieurs commits ont été faits sur la branche, il est toujours possible de retravailler l'historique et cela se fait idéalement avant de créer la PR.
Pour se faire utiliser la commande `git rebase -i` 
Par exemple si doit retravailler les 3 derniers commit :

::

    git rebase -i HEAD~3

Ensuite il faut utiliser `squash` pour faire merger chaque commit dans le précédent et `reword` pour reformuler un commit message

2) Précéder le commit message et le titre de la PR de ce qu'il impacte (application ou autre). 
Le message du commit doit être explicite mais doit rester bref (50 caractères maximum est idéal). 
Par exemple de commit message pour l'application `Absence prof` :

::

    ABSENCE_PROF: Migrate custom access permission to view permission

Il faut essayer de respecter les bonnes pratiques expliquées `ici <https://fr.wikibooks.org/wiki/Git/%C3%89crire_des_messages_de_commit>`_