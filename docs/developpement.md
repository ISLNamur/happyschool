Développement
=============

![Architecture Happyschool](img/happyschool_architecture.png)

La volonté derrière l'architecture d'Happyschool est de garder une certaine
simplicité autour de composants matures et flexibles. De manière générale,
Happyschool peut être divisé en deux parties. Un *back-end* qui s'occupe du
stockage des données et de la logique interne. Et un *front-end* qui s'occupe
d'afficher les données à l'utilisateur final ainsi que de la logique de
l'interface.

Back-end
--------
Le cœur du *back-end* est pris en charge par Django, un framework python abordable
et complet. Sa [documentation](https://docs.djangoproject.com/en/2.0/) est très
fournie et est une aide précieuse pour le développement. Le stockage et le
traitement des données est quant à lui gérer par [PostgreSQL](https://www.postgresql.org/).
Django propose une couche d'abstraction qui génère en interne les commandes SQL,
il n'y a donc pas – ou très peu – d'interaction directe avec PostgreSQL. En fait,
Django s'inspire très largement du principe [MVC](https://fr.wikipedia.org/wiki/Mod%C3%A8le-vue-contr%C3%B4leur),
il propose ainsi cette couche d'abstraction pour gérer l'aspect *modèle*
ainsi que toute la logique autour des données – le *contrôleur*. Django
propose également un système de [gabarit](https://docs.djangoproject.com/fr/2.0/topics/templates/)
– pour la partie *vue*. Toutefois, la gestion du rendu côté serveur (et
donc par django et son système de gabarit) rend difficile et surtout peu
pratique le dynamisme de l'interface de l'utilisateur final (la page web).
C'est [Vue.js](https://fr.vuejs.org), un framework javascript, qui va se
charger de la partie interface – la partie *vue*. L'interaction entre les
deux va se faire au travers d'une API [REST](https://fr.wikipedia.org/wiki/Representational_state_transfer)
avec une sérialisation en JSON. C'est l'excellent [Django REST framework](https://www.django-rest-framework.org/)
qui va permettre la création de l'API et s'occuper de la sérialisation/désérialisation.

Front-end
---------
C'est donc le framework Vue.js qui va se charger de l'interface web, les
deux points forts de celui-ci sont, sa facilité de mise en œuvre et la
réactivité aux changements qu'il offre. Son principe est de definir une
série de données et les transformations sur la partie html lorsque ces
données changent. Cette façon de faire permet une séparation claire des
différentes parties du code et donc une meilleure vue d'ensemble (sans
mauvais jeu de mots). En ce qui concerne le style, le *css*, c'est le
très connu [Bootstrap](https://getbootstrap.com/docs/4.0) qui est utilisé
et qui s'intègre à Vue.js avec le module [Bootstrap-vue](https://bootstrap-vue.js.org/).
Finalement, c'est [Webpack](https://webpack.js.org/), un empaqueteur, qui
orchestre toute la partie javascript (interprétation, assemblage,
minification, etc).

Création d'une application
--------------------------
Au lieu d'expliquer techniquement point par point le fonctionnement
d'Happyschool, expliquons comment créer une application, tant la partie
*back-end* que *front-end*.

Supposons que nous voulons créer une application simple de présence/d'absence
des élèves. La première étape est de créer les fichiers de bases en python.
Pour cela, Django propose une commande de création, dans le dossier racine
d'Happyschool :
```
python3 manage.py startapp student_absence
```
Ceci va créer une arborescence dans un nouveau dossier `student_absence`.
Le fichier `manage.py` permet de faire [pas mal de choses](https://docs.djangoproject.com/fr/2.0/ref/django-admin/)
en relation avec Django et le projet, comme un accès à un shell python pour
interagir avec les modèles créés ou encore d'appliquer des changements de
notre modèle.

Tout d'abord, créons notre modèle dans le fichier `student_absence/models.py`:
```
# Notre modèle d'absence.
class StudentAbsenceModel(models.Model):
    # L'étudiant qui sera absent.
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)
    date_absence_start = models.DateField("Date de début de l'absence")
    date_absence_end = models.DateField("Date de fin de l'absence")
    # Indique si l'étudiant est absent le matin.
    morning = models.BooleanField("Absence le matin", default=True)
    # Indique si l'étudiant est absent l'après-midi.
    afternoon = models.BooleanField("Absence l'après-midi", default=True)
    user = models.CharField("Utilisateur qui a créé l'absence", max_length=100)
    datetime_creation = models.DateTimeField("Date et heure de création de l'absence",
                                             auto_now_add=True)
    datetime_update = models.DateTimeField("Date et heure de mise à jour de l'absence",
                                           auto_now=True)
```

Détaillons le code:
- `from django.db import models` permet d'importer la couche d'abstraction
de Django concernant la base de donnée.
- `from core.models import StudentModel` permet d'utiliser les étudiants
qui sont dans la base de donnée.
- `class StudentAbsenceModel(models.Model)` est la déclaration de notre
modèle, elle hérite de `models.Model` qui est la couche d'abstraction de
django. Nous devons définir tous les champs de notre modèle (les colonnes
dans la base de donnée).
- `student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)` est
notre premier champ, il permet de faire une liaison avec une autre entrée
de notre base de donnée, ici, un étudiant (`StudentModel`). L'argument
`on_delete=models.CASCADE` indique que si un étudiant est supprimé, l'absence
sera également supprimée.
- `date_absence_start` et `date_absence_end` sont de simples champs indiquant
la date de début et de fin de l'absence.
- `morning` et `afternoon`  sont des booléens qui indiquent si l'absence
a lieu le matin et/ou l'après-midi.
- `user`, `datetime_creation` et `datetime_update` enregistrent des données
concernant l'enregistrement d'une entrée. `auto_now` et `auto_now_add`
permet d'automatiquement enregistrer la date et heure de modification et
création.

Une fois notre fichier sauvegardé, nous devons demander à Django de creér
le schéma correspondant dans la base de donnée. Il faut donc d'abord spécifier
à Django que nous voulons utiliser cette nouvelle application. C'est dans
le fichier `happyschool/settings.py` et plus spécifiquement la variable
`INSTALLED_APPS` auquel nous devons ajouter notre nouvelle application :
```
INSTALLED_APPS = [
    ...,
    'appels',
    'absence_prof',
    'dossier_eleve',
    'mail_notification',
    'mail_answer',
    'student_absence,
]
```

Cela fait, nous pouvons créer le schéma grâce à `manage.py`,
nous pouvons exécuter les deux commandes suivantes :
```
python3 manage.py makemigrations student_absence
```
qui va générer les commandes SQL nécessaire à la création/modification
de la base de donnée. Et finalement :
```
python3 manage.py migrate student_absence
```
qui va executer les commandes SQL.

Passons maintenant à la logique autour du modèle et de ce qui sera exposé
par l'API REST.

Définissons d'abord ce qui sera exposé dans le modèle, pour cela créons un
fichier `serializers.py` :
```
from rest_framework import serializers

from core.serializers import StudentSerializer
from core.models import StudentModel
from student_absence.models import StudentAbsenceModel


class StudentAbsenceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(queryset=StudentModel.objects.all(),
                                                    source='student', required=False,
                                                    allow_null=True)

    class Meta:
        model = StudentAbsenceModel
        exclude = ('user',)
        read_only_fields = ('datetime_creation', 'datetime_update',)

```
Regardons le code, nous commonçons par importer toutes les classes qui
vont nous être nécessaire à notre propre *sérialiseur*. Ensuite, nous
créons notre *sérialiseur*, `StudentAbsenceSerializer` qui hérite de
`serializers.ModelSerializer` un *sérialiseur* qui se base sur un modèle.

Remarquez que le nom de notre classe suit une certaine convention de nommage,
l'écriture est de type [camel case](serializers.ModelSerializer) ensuite
sa fonction est inclue dans son nom, `Serializer`, ainsi que ce à quoi
elle se rapporte `StudentAbsence`. Dans un projet collaboratif, il devient
vite nécessaire d'établir certaines conventions, le style d'écriture en
fait parti. Happyschool essaye tant bien que mal de suivre un style
conforme au [PEP8](https://www.python.org/dev/peps/pep-0008/) même si
par souci de clarté quelques entorses sont parfaitement autorisées.

Continuons notre analyse du code et passons directement à `class Meta` qui
permet une génération de notre classe de manière dynamique. Nous avons
donc mis dans cette partie, le modèle auquel nous nous réferrons,
`StudentAbsenceModel`, les champs à exclure de la sérialisation, `('user',)`
ainsi que les champs en lecture seul `('datetime_creation', 'datetime_update',)`.
Nous aurions pu au contraire, spécifier les champs à exposer par la
variable `fields = ('un_champ', ...)`. Toute la documentation se sur la
sérialisation se trouve [ici](https://www.django-rest-framework.org/api-guide/serializers/).

Finalement, jetons un œil à `student` et `student_id`. À priori, le champ
`student` doit normalement déjà être inclut dans la sérialisation puisqu'il
n'est pas mentionné dans `exclude`. Cependant, nous aimerions avoir un
comportement différent pour la création/mise àjour d'une entrée où nous voulons
juste indiquer le matricule de l'étudiant et pour la lecture d'une entrée
où nous voulons avoir des informations supplémentaires sur l'étudiant
comme son nom, sa classe, son établissement/enseignement. `student` sera
donc le champ en lecture seul avec toutes les informations et `student_id`
sera le champ du matricule de l'élève nécessaire uniquement pour la
création/modification d'une entrée dans la base de donnée.
