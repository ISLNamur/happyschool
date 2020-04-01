Interface admin django
======================

Django propose une interface d’administration pour gérer certains
éléments de la base de donnée comme les utilisateurs, groupes et
permissions mais également les objects utilisés par les différentes
applications. HappySchool stocke également la configuration des
applications dans la base de donnée et sont donc modifiable à partir de
cette interface.

Seules deux applications sont nécessaires au bon fonctionnement d'HappySchool,
``annuaire`` et ``core``. La première contient toutes les fonctionnalités de
recherches utilisées par la plupart des applications. Tandis que la deuxième,
comme son nom l'indique, est la brique centrale sur laquelle se construit les
autres applications.

L'interface d'administration Django est accessible à l'adresse suivante :
http://ip-du-serveur/admin

Core
----

Paramètres généraux
^^^^^^^^^^^^^^^^^^^

C'est l'objet ``CoreSettingsModel`` qui permet d'éditer les paramètres. S'il
n'existe aucun objet, créez-en un et **un seul**.

Vous pourrez ici modifier le nom de l'école qui apparaîtra à différents endroits
dont les documents générés ainsi que l'url d'accès d'HappySchool.

Si vous utilisez un serveur distant, vous pouvez également indiquer son url ainsi
que le *token* de l'utilisateur distant à utiliser pour la synchronisation.

Établissement/enseignement
^^^^^^^^^^^^^^^^^^^^^^^^^^

HappySchool permet de gérer plusieurs établissements et/ou enseignements afin
de compartimenter les accès en fonction des applications. Par exemple, une
école possédant deux établissements qui posséde une infirmerie commune
devra gérer les élèves des deux parties contrairement aux dossiers des élèves
qui seront traités de manière distinctes. Ceci se reflète dans les objects
``TeachingModel`` qui seront associés aux élèves, enseignants et classes.
Au moins un objet est nécessaire.

Responsables
^^^^^^^^^^^^

Les responsables représentent tous les non-étudiants, qu'ils soient
professeurs, éducateurs, membres de la direction ou encore secrétaires.
Ils ne pourront se connecter que si un utilisateur leur est associé. L'objet
associé est le ``ResponsibleModel``.

Étudiants
^^^^^^^^^

Les objets concernant les étudiants sont divisés en deux modèles. Le
``StudentModel`` contient les données essentielles de l'élève. Tandis
que ``AdditionalStudentInfo`` contient quant à lui les informations
personnelles/confidentielles. Le but étant d'avoir une distinction clair entre
les deux, HappySchool permettant de fonctionner en binôme entre un serveur
local à l'école et une instance dans le cloud avec un minimum
d'informations.

Courriels
^^^^^^^^^

Certaines applications permettent d'envoyer un courriel. Le modèle
``EmailModel`` permet de configurer ces différents courriels. En particulier,
le champ ``year`` indique la *responsabilité* vis à vis d'une année. Ainsi,
si une application envoie un courriel concernant un élève aux responsables de
l'élève, HappySchool va regarder la correspondance entre l'année dans laquelle
se trouve l'élève et le champ ``year`` de l'objet ``EmailModel`` pour savoir
s'il doit être envoyé à cette adresse.


Utilisateurs, groupes et permissions
------------------------------------

Une des volontés derrière HappySchool est de répondre au besoin de granularité
dans l'accès à l'information. Pour cela, HappySchool utilise le système de
permissions de Django. C'est la section *Authentification et autorisation* dans
l'interface d'administration qui contient tous les objects qui nous intéresse.

Même si l'authentification se fait par service externe (LDAP, GoogleAuth, …),
chaque utilisateur se retrouve ici. Il peut être intéressant de préenregistrer
tous les futures utilisateurs afin des les associer avec un objet
``ResponsibleModel``.

Afin de gérer les accès en lectures et/ou écritures pour chacune des applications,
HappySchool utilise des permissions au niveau des groupes. Ainsi chaque utilisateur
peut appartenir à un ou plusieurs groupes avec des permissions différentes.

De manière générale, la permission ``Can view model`` où ``model`` est le nom
du modèle principal de l'application, donne accès à l'application et
``Can add/change/delete model`` donne accès en écriture à l'application.

Direction et sysadmin
^^^^^^^^^^^^^^^^^^^^^

Afin de se concentrer sur l'information utile, les responsables n'ont accès
qu'aux informations concernant leurs élèves (déduit à partir de leurs classes et
années). Les groupes ``direction`` et ``sysadmin`` font exceptions à cette règle
et ont accès à tous les élèves. Il se peut également que l'application permette
d'outrepasser cette règle.
