Développement
=============

Back-end
--------

Le cœur du *back-end* est pris en charge par Django, un framework python
abordable et complet. Sa
`documentation <https://docs.djangoproject.com/en/2.0/>`__ est très
fournie et est une aide précieuse pour le développement. Le stockage et
le traitement des données est quant à lui gérer par
`PostgreSQL <https://www.postgresql.org/>`__. Django propose une couche
d’abstraction qui génère en interne les commandes SQL, il n’y a donc pas
– ou très peu – d’interaction directe avec PostgreSQL. En fait, Django
s’inspire très largement du principe
`MVC <https://fr.wikipedia.org/wiki/Mod%C3%A8le-vue-contr%C3%B4leur>`__,
il propose ainsi cette couche d’abstraction pour gérer l’aspect *modèle*
ainsi que toute la logique autour des données – le *contrôleur*. Django
propose également un système de
`gabarit <https://docs.djangoproject.com/fr/2.0/topics/templates/>`__ –
pour la partie *vue*. Toutefois, la gestion du rendu côté serveur (et
donc par django et son système de gabarit) rend difficile et surtout peu
pratique le dynamisme de l’interface de l’utilisateur final (la page
web). C’est `Vue.js <https://fr.vuejs.org>`__, un framework javascript,
qui va se charger de la partie interface – la partie *vue*.
L’interaction entre les deux va se faire au travers d’une API
`REST <https://fr.wikipedia.org/wiki/Representational_state_transfer>`__
avec une sérialisation en JSON. C’est l’excellent `Django REST
framework <https://www.django-rest-framework.org/>`__ qui va permettre
la création de l’API et s’occuper de la sérialisation/désérialisation.

Front-end
---------

C’est donc le framework Vue.js qui va se charger de l’interface web, les
deux points forts de celui-ci sont, sa facilité de mise en œuvre et la
réactivité aux changements qu’il offre. Son principe est de définir une
série de données et les transformations sur la partie html lorsque ces
données changent. Cette façon de faire permet une séparation claire des
différentes parties du code et donc une meilleure vue d’ensemble (sans
mauvais jeu de mots). En ce qui concerne le style, le *css*, c’est le
très connu `Bootstrap <https://getbootstrap.com/docs/4.0>`__ qui est
utilisé et qui s’intègre à Vue.js avec le module
`Bootstrap-vue <https://bootstrap-vue.js.org/>`__. Finalement, c’est
`Webpack <https://webpack.js.org/>`__, un empaqueteur, qui orchestre
toute la partie javascript (interprétation, assemblage, minification,
etc).

Création d’une application
--------------------------

Au lieu d’expliquer techniquement point par point le fonctionnement
d’Happyschool, expliquons comment créer une application, tant la partie
*back-end* que *front-end*. Tout le code peut se retrouver sur notre
`dépôt <https://github.com/ISLNamur/happyschool/tree/tuto>`__.

Supposons que nous voulons créer une application simple de
présence/d’absence des élèves. La première étape est de créer les
fichiers de bases en python. Pour cela, Django propose une commande de
création, dans le dossier racine d’Happyschool :

::

   python3 manage.py startapp student_absence

Ceci va créer une arborescence dans un nouveau dossier
``student_absence``. Le fichier ``manage.py`` permet de faire `pas mal
de choses <https://docs.djangoproject.com/fr/2.0/ref/django-admin/>`__
en relation avec Django et le projet, comme un accès à un shell python
pour interagir avec les modèles créés ou encore d’appliquer des
changements de notre modèle.

Tout d’abord, créons notre modèle dans le fichier
``student_absence/models.py``:

::

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

Détaillons le code: - ``from django.db import models`` permet d’importer
la couche d’abstraction de Django concernant la base de donnée. -
``from core.models import StudentModel`` permet d’utiliser les étudiants
qui sont dans la base de donnée. -
``class StudentAbsenceModel(models.Model)`` est la déclaration de notre
modèle, elle hérite de ``models.Model`` qui est la couche d’abstraction
de django. Nous devons définir tous les champs de notre modèle (les
colonnes dans la base de donnée). -
``student = models.ForeignKey(StudentModel, on_delete=models.CASCADE)``
est notre premier champ, il permet de faire une liaison avec une autre
entrée de notre base de donnée, ici, un étudiant (``StudentModel``).
L’argument ``on_delete=models.CASCADE`` indique que si un étudiant est
supprimé, l’absence sera également supprimée. - ``date_absence_start``
et ``date_absence_end`` sont de simples champs indiquant la date de
début et de fin de l’absence. - ``morning`` et ``afternoon`` sont des
booléens qui indiquent si l’absence a lieu le matin et/ou l’après-midi.
- ``user``, ``datetime_creation`` et ``datetime_update`` enregistrent
des données concernant l’enregistrement d’une entrée. ``auto_now`` et
``auto_now_add`` permet d’automatiquement enregistrer la date et heure
de modification et création.

Une fois notre fichier sauvegardé, nous devons demander à Django de
créer le schéma correspondant dans la base de donnée. Il faut donc
d’abord spécifier à Django que nous voulons utiliser cette nouvelle
application. C’est dans le fichier ``happyschool/settings.py`` et plus
spécifiquement la variable ``INSTALLED_APPS`` auquel nous devons ajouter
notre nouvelle application :

::

   INSTALLED_APPS = [
       ...,
       'appels',
       'absence_prof',
       'dossier_eleve',
       'mail_notification',
       'mail_answer',
       'student_absence,
   ]

Cela fait, nous pouvons créer le schéma grâce à ``manage.py``, nous
pouvons exécuter les deux commandes suivantes :

::

   python3 manage.py makemigrations student_absence

qui va générer les commandes SQL nécessaire à la création/modification
de la base de donnée. Et finalement :

::

   python3 manage.py migrate student_absence

qui va executer les commandes SQL.

Passons maintenant à la logique autour du modèle et de ce qui sera
exposé par l’API REST.

Définissons d’abord ce qui sera exposé dans le modèle, pour cela créons
un fichier ``serializers.py`` :

::

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

Regardons le code, nous commonçons par importer toutes les classes qui
vont nous être nécessaire à notre propre *sérialiseur*. Ensuite, nous
créons notre *sérialiseur*, ``StudentAbsenceSerializer`` qui hérite de
``serializers.ModelSerializer`` un *sérialiseur* qui se base sur un
modèle.

Remarquez que le nom de notre classe suit une certaine convention de
nommage, l’écriture est de type `camel
case <serializers.ModelSerializer>`__ ensuite sa fonction est inclue
dans son nom, ``Serializer``, ainsi que ce à quoi elle se rapporte
``StudentAbsence``. Dans un projet collaboratif, il devient vite
nécessaire d’établir certaines conventions, le style d’écriture en fait
parti. HappySchool essaye tant bien que mal de suivre un style conforme
au `PEP8 <https://www.python.org/dev/peps/pep-0008/>`__ même si par
souci de clarté quelques entorses sont parfaitement autorisées.

Continuons notre analyse du code et passons directement à ``class Meta``
qui permet une génération de notre classe de manière dynamique. Nous
avons donc mis dans cette partie, le modèle auquel nous nous référons,
``StudentAbsenceModel``, les champs à exclure de la sérialisation,
``('user',)`` ainsi que les champs en lecture seul
``('datetime_creation', 'datetime_update',)``. Nous aurions pu au
contraire, spécifier les champs à exposer par la variable
``fields = ('un_champ', ...)``. Toute la documentation se sur la
sérialisation se trouve
`ici <https://www.django-rest-framework.org/api-guide/serializers/>`__.

Finalement, jetons un œil à ``student`` et ``student_id``. À priori, le
champ ``student`` doit normalement déjà être inclut dans la
sérialisation puisqu’il n’est pas mentionné dans ``exclude``. Cependant,
nous aimerions avoir un comportement différent pour la création/mise à
jour d’une entrée où nous voulons juste indiquer le matricule de
l’étudiant et pour la lecture d’une entrée où nous voulons avoir des
informations supplémentaires sur l’étudiant comme son nom, sa classe,
son établissement/enseignement. ``student`` sera donc le champ en
lecture seul avec toutes les informations et ``student_id`` sera le
champ du matricule de l’élève nécessaire uniquement pour la
création/modification d’une entrée dans la base de donnée.

Avant d’arriver à la partie *vue* de notre application, mettons en place
un système de configuration pour notre application pour, par exemple,
spécifier l’enseignement/établissement qui aura accès aux absences. Afin
de profiter des possibilités de django, créons un modèle qui n’aura
qu’une seule entrée, les paramètres de StudentAbsence.

::

   from core.models import StudentModel, TeachingModel

   # Les paramètres de notre application.
   class StudentAbsenceSettingsModel(models.Model):
       # Les enseignements/établissements utilisés par l'application.
       # Ne pas oublier de mettre une valeur par défaut pour la création automatique.
       teachings = models.ManyToManyField(TeachingModel, default=None)

Ceci rajoute simplement un modèle, ``StudentAbsenceSettingsModel`` avec
un seul champ, ``teachings``, qui peut être relier à plusieurs instances
de ``TeachingModel``, d’où le ``ManyToManyField``. Par défaut, aucun
``TeachingModel`` ne sera sélectioné et aucune entrée ne sera affichée.
Il faudra donc que l’administrateur mette explicitement et manuellement
au moins une entrée.

Comme pour ``StudentAbsenceModel``, il faut appliquer les changements
sur notre base de donnée avec :

::

   python3 manage.py makemigrations
   python3 manage.py migrate

Passons maintenant au cœur de notre application avec la partie *vue*,
c’est-à-dire exposer notre modèle au travers d’une API REST. La classe
``ModelViewSet`` du DRF, permet de nous faciliter grandement le travail.
En effet, en lui donnant le *sérialiseur* ainsi que quelques paramètres,
il nous crée automatiquement une interface http en gérant les requêtes
``GET``, ``POST``, ``PUT``, ``DELETE``. Une des particularité
d’Happyschool étant de gérer les permissions d’accès, la classe
``BaseMovelViewSet`` va hériter de ``ModelViewSet`` et gérer les accès
automatiquement, un éducateur du 2ème niveau ne verra que les élèves de
ce niveau. Il est évidemment possible de passer outre en surchargeant la
méthode ``get_group_all_access`` qui attend comme retour un ``QuerySet``
de ``Group`` ayant accès à tous les niveaux. Les paramètres attendus par
notre class ``StudentAbsenceViewSet(BaseModelViewSet)`` sont, le
*sérialiseur* ``serializer_class``, la requête de base à la base de
donnée ``queryset`` (qui servira également de cache), les permissions
avec ``permission_classes``, les champs qui peuvent être ordonés
``ordering_fields`` et les filtres que nous pouvons appliquer sur nos
données, ``filter_class``, objet que détaillerons par la suite.

En ce qui concerne, ``permission_classes``, nous pouvons demander que
l’utilisateur soit connecté avec ``IsAuthenticated`` et utilisé le
système de permission de django pour gérer
l’écriture/modification/suppression qui accessible par l’interface
d’admin de django.

Finalement, intéressons-nous aux capacités de filtres. Le système offert
par l’application
```django_filters`` <https://django-filter.readthedocs.io/en/master/>`__
permet une grande souplesse dans les types de filtres. Pour cela la
classe fournie par Happyschool, ``BaseFilters`` qui hérite de
``django_filters``, permet d’indiquer les champs à filtrer de manière
exacte mais également des filtres personnalisés. Dans notre application
nous avons ajouté un filtre par classe.

Nous obtenons alors le code suivant :

::

   import json

   from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
   from django_filters import rest_framework as filters

   from django.contrib.auth.mixins import LoginRequiredMixin
   from django.views.generic import TemplateView

   from core.views import BaseModelViewSet, BaseFilters
   from core.models import ResponsibleModel
   from core.people import get_classes
   from core.utilities import get_menu

   from student_absence.models import StudentAbsenceModel, StudentAbsenceSettingsModel
   from student_absence.serializers import StudentAbsenceSerializer, StudentAbsenceSettingsSerializer

   class StudentAbsenceFilter(BaseFilters):
       classe = filters.CharFilter(method='classe_by')

       class Meta:
           fields_to_filter = ('student_id', 'date_absence_start', 'date_absence_end')
           model = StudentAbsenceModel
           # Permet de génèrer correctement les filtres avec prises en comptes des accents.
           fields = BaseFilters.Meta.generate_filters(fields_to_filter)
           filter_overrides = BaseFilters.Meta.filter_overrides

       def classe_by(self, queryset, name, value):
           if not value[0].isdigit():
               return queryset

           teachings = ResponsibleModel.objects.get(user=self.request.user).teaching.all()
           classes = get_classes(list(map(lambda t: t.name, teachings)), True, self.request.user)
           queryset = queryset.filter(student__classe__in=classes)

           if len(value) > 0:
               queryset = queryset.filter(student__classe__year=value[0])
               if len(value) > 1:
                   queryset = queryset.filter(student__classe__letter=value[1].lower())
           return queryset


   class StudentAbsenceViewSet(BaseModelViewSet):
       queryset = StudentAbsenceModel.objects.filter(student__isnull=False)

       serializer_class = StudentAbsenceSerializer
       permission_classes = (IsAuthenticated, DjangoModelPermissions,)
       filter_class = StudentAbsenceFilter
       ordering_fields = ('datetime_creation',)

Il ne nous reste plus qu’à exposer notre API par un accès http, une URL.
Nous voulons tout d’abord que tout ce qui concerne notre application
soit de la forme ``http://mon.domaine.org/student_absence/…``, pour cela
il faut ajouter au fichier ``happyschool/urls.py``, l’application
``student_absence`` à la liste ``app`` du fichier. Ensuite, créons le
fichier ``/student_absence/urls.py`` et mettons-y :

::

   from rest_framework.routers import DefaultRouter

   from . import views

   urlpatterns = [
   ]

   router = DefaultRouter()
   router.register(r'api/student_absence', views.StudentAbsenceViewSet)

   urlpatterns += router.urls

qui va se charger de créer les bonnes urls. Ainsi pour avoir la liste
des absences il faudra faire
http://localhost:8000/student_absence/api/student_absence/ si vous avez
lancé le serveur de développement en local. Pour accéder à une entrée en
particulier, qui a comme *id* 42, nous irons sur
http://localhost:8000/student_absence/api/student_absence/42/. DRF crée
automatiquement une interface web de notre API accessible depuis un
navigateur, il suffit d’aller sur les liens précédents.

Pour tester notre API, django fournit un serveur de développement qui
peut être lancer avec :

::

   python3 manage.py runserver

et qui se rechargera à chaque modification de fichiers.

Nous avons maintenant notre partie *back-end* prête à l’emploi, il nous
reste à développer la partie *front-end* qui sera principalement écrite
en javascript avec le framework
`Vue.js <https://vuejs.org/v2/guide/>`__. Pour la suite, il est
conseillé d’avoir lu, au moins en partie, sa
`documentation <https://vuejs.org/v2/guide/>`__ et sa philosophie.

Pour notre *front-end* nous avons tout d’abord besoin d’un point
d’entrée, une page html pour servir notre code javascript ainsi que le
contexte de notre application *i.e.* ses paramètres. Pour cela, ajoutons
à notre fichier ``views.py`` les éléments suivants:

::

   def get_settings():
       settings_student_absence = StudentAbsenceSettingsModel.objects.first()
       if not settings_student_absence:
           # Create default settings.
           StudentAbsenceSettingsModel.objects.create().save()

       return settings_student_absence


   class StudentAbsenceView(LoginRequiredMixin,
                            TemplateView):
       template_name = "student_absence/student_absence.html"
       filters = [
           {'value': 'student_id', 'text': 'Matricule'},
           {'value': 'classe', 'text': 'Classe'},
           {'value': 'date_absence_start', 'text': 'Début absence'},
           {'value': 'date_absence_end', 'text': 'Fin absence'},
       ]

       def get_context_data(self, **kwargs):
           # Add to the current context.
           context = super().get_context_data(**kwargs)
           context['menu'] = json.dumps(get_menu(self.request, "student_absence"))
           context['filters'] = json.dumps(self.filters)
           context['settings'] = json.dumps((StudentAbsenceSettingsSerializer(get_settings()).data))
           return context

La fonction ``get_settings()`` permet de rapatrier les paramètres de
l’application et de créer le modèle correspondant s’il ne l’est pas
encore. Quant à la classe ``StudentAbsenceView`` va exposer notre page
html. Django utilise un système de
`template <https://docs.djangoproject.com/fr/2.1/topics/templates/>`__
(ou gabarit) qui permet de générer dynamiquement une page pour y
introduire quelques variables (paramètres, utilisateur, etc). Notre
template aura la forme suivante
(``student_absence/templates/student_absence/student_absence.html``) :

::

   {% extends "core/base_vue.html" %}

   {% block header %}
   <title>HappySchool : Absence des élèves</title>
   {% endblock %}
   {% block content %}
   <script>
       const current_app = "student_absence";
       const settings = JSON.parse('{{ settings|safe }}');
       const menu = {{ menu|safe }};
       const filters = JSON.parse('{{ filters|safe }}');
   </script>
   <div id="vue-app"></div>
   {% load render_bundle from webpack_loader %}
   {% render_bundle 'student_absence' %}

   {% endblock %}

Le langage de gabarit utilisé par django permet non seulement d’insérer
des variables avec ``{{ ma_variable }}`` mais également de faire des
opérations logiques ``{% function/logique %}``. La première ligne hérite
d’un autre gabarit ``core/base_vue.html`` qui s’occupe de charger les
certaines librairies commune à toutes les applications mais également
d’exposer l’utilisateur et les groupes auxquels il appartient.
``{% block header %}...{% endblock %}`` permet d’insérer du code html
dans la partie header de la page, ici le titre de la page. Quant à
``{% block content %}...{% endblock %}`` il permet d’insérer du code
html dans la balise ``<body>`` de la page. C’est dans la balise
``<script>`` que le *context* de la page va être *traduit* en javascript
(``{{ settings|safe }}``, …), le filtre
```safe`` <https://docs.djangoproject.com/fr/2.1/ref/templates/builtins/#safe>`__
indique à django de ne pas échapper les caractères (accent, guillement,
etc).

``<div id="vue-app"></div>`` servira à Vue.js comme nous le verons par
la suite. Quant à ``{% load render_bundle from webpack_loader %}`` et
``{% render_bundle 'student_absence' %}``, ils insérent le code généré
par Vue.js.

Revenons maintenant à notre fichier ``views.py`` et notre class
``StudentAbsenceView``. Tout d’abord, elle hérite de
``LoginRequiredMixin`` et de ``TemplateView``. La première classe
implique qu’il faut être connecté en tant qu’utilisateur pour afficher
la page. La seconde est une `classe
générique <https://docs.djangoproject.com/fr/2.1/ref/class-based-views/base/>`__
fournie par Django pour afficher une page basée sur un gabarit. Elle
demande juste de fournir le chemin vers le template avec la variable
``template_name``. La fonction ``get_context_data()`` quant à elle,
permet de passer au gabarit certaines variables, ici les paramètres, les
applications à afficher dans le menu ainsi que les filtres disponibles
pour l’application.

Pour que l’url sur notre classe il rajouter la ligne suivante dans le
fichier ``urls.py`` :

::

   from django.urls import path

   urlpatterns = [
       path('', views.StudentAbsenceView.as_view(), name='student_absence'),
   ]

Et c’est tout pour le code python. Passons au javascript !

Afin de structurer le code en différents modules, mutualiser le
chargement des librairies externes mais aussi minimiser le code pour le
rendre moins lourd à charger, nous utiliserons
`Webpack <https://webpack.js.org/>`__. Nous allons pour le moment nous
contenter de rajouter notre application et en particulier le code
javascript que nous allons écrire. Pour cela, regardons le fichier
``webpack.common.js`` et particulier les deux parties suivantes :

::

   entry: {
           babelPolyfill: "babel-polyfill",
           menu: './assets/js/menu',
           annuaire: './assets/js/annuaire',
           appels: './assets/js/appels',
           mail_notification: './assets/js/mail_notification',
           mail_notification_list: './assets/js/mail_notification_list',
           members: './assets/js/members',
           mail_answer: './assets/js/mail_answer',
           answer: './assets/js/answer',
           dossier_eleve: './assets/js/dossier_eleve',
           ask_sanctions: './assets/js/ask_sanctions',
           student_absence: './assets/js/student_absence',
       },

Où nous avons rajouter le point d’entrée
``./assets/js/student_absence``.

::

   name: "commons",
               chunks: ["menu", "schedule_change", "appels", "mail_notification",
                   "mail_notification_list", "members", "mail_answer", "dossier_eleve",
                   "ask_sanctions", "annuaire", "student_absence",
               ],

Où nous avons rajouter notre application dans la liste des applications
mutualisables.

Créons donc un simple point d’entrée :

::

   import Vue from 'vue';

   import StudentAbsence from '../student_absence/student_absence.vue';

   var studentAbsenceApp = new Vue({
       el: '#vue-app',
       data: {},
       template: '<student-absence/>',
       components: { StudentAbsence },
   })

La première ligne importe ``Vue`` et la deuxième notre composant, qui
sera le cœur de la partie front-end. Finalement, la variable
``studentAbsenceApp`` est une application *Vue.js* qui s’attache à
l’élément ``<div id="vue-app">`` de notre gabarit.

Ajoutons donc notre composant
``assets/student_absence/student_absence.vue`` :

::

   <template>
       <div>
           <div class="loading" v-if="!loaded"></div>
           <app-menu :menu-info="menuInfo"></app-menu>
           <b-container v-if="loaded">
               <b-row>
                   <h2>Absence des élèves</h2>
               </b-row>
               <b-row>
                   <b-col>
                       <b-form-group>
                           <div>
                               <b-btn variant="primary">
                                   <icon name="plus" scale="1" class="align-middle"></icon>
                                   Nouvelle absence
                               </b-btn>
                               <b-btn variant="outline-secondary">
                                   <icon name="search" scale="1"></icon>
                                   Ajouter des filtres
                               </b-btn>
                           </div>
                       </b-form-group>
                   </b-col>
               </b-row>
           </b-container>
       </div>
   </template>

   <script>
   import Vue from 'vue';
   import BootstrapVue from 'bootstrap-vue'
   Vue.use(BootstrapVue);

   import 'vue-awesome/icons'
   import Icon from 'vue-awesome/components/Icon.vue'
   Vue.component('icon', Icon);

   import Menu from '../common/menu.vue'

   export default {
       data: function () {
           return {
               menuInfo: {},
               loaded: false,
           }
       },
       methods: {
       },
       mounted: function () {
           this.menuInfo = menu;
           this.loaded = true;
       },
       components: {
           'app-menu': Menu,
       },
   }
   </script>

   <style>
   .loading {
     content: " ";
     display: block;
     position: absolute;
     width: 80px;
     height: 80px;
     background-image: url(/static/img/spin.svg);
     background-size: cover;
     left: 50%;
     top: 50%;
   }
   </style>

Un composant vue possède trois parties : ``<template>`` qui est
également un gabarit mais cette fois-ci pour le code js, ``<script>``
pour toute la partie logique et ``<style>`` pour le style *css*.

Pour dire à webpack de *compiler* le code, la commande suivante permet
de le faire ainsi que de relancer la compilation à chaque changement de
fichier :

::

   ./node_modules/.bin/webpack --config webpack.dev.js --watch

Si l’on pointe maintenant notre navigateur vers
http://localhost:8000/student_absence et si le serveur de développement
a été lancé (``python3 manage.py runserver``), notre application
s’affiche enfin ! Pour faciliter le développement, il existe une
`extension <https://github.com/vuejs/vue-devtools>`__ pour navigateurs
qui permet d’afficher l’état de notre application Vue.js, les composants
ainsi que les différentes variables. Il est fortement conseillé de
l’utiliser !

Dans ce premier jet, c’est une page simple avec un menu, un titre et
deux bouttons. La partie *template* utilise beaucoup de composants
venant de la librairie
```BootstrapVue`` <https://bootstrap-vue.js.org/docs>`__ mais également
le composant ``Menu`` qui est propre à HappySchool. Vous pouvez
remarquer que la page affiche une image de chargement. Celle-ci est liée
à la variable ``loaded`` qui initialement fausse et qui permute lorsque
le composant est chargé (dans la fonction ``mounted``).

La fonction principale étant d’afficher les absences, rajoutons une
méthode pour rapatrier les données et les assigner à ``entries``.
Profitons-en pour mettre ``loaded = true`` lorsque les données ont été
rapatriées.

::

       data: function () {
           return {
               menuInfo: {},
               entriesCount: 0,
               entries: [],
               loaded: false,
           }
       },
       methods: {
           loadEntries: function () {
               // Get current absences.
               axios.get('/student_absence/api/student_absence/')
               .then(response => {
                   this.entries = response.data.results;
                   // Everything is ready, hide the loading icon and show the content.
                   this.loaded = true;
               });
           },
       }

Et modifions ``mounted``:

::

       mounted: function () {
           this.menuInfo = menu;

           this.loadEntries();
       },

Si nous rechargeons la page, visuellement, rien n’a changé mais si nous
regardons dans les requêtes faites à notre serveur de développement,
nous voyons qu’une requête vers notre API a été effectuée. Pour le
moment aucune entrée n’a encore été créée donc rien n’est rapatrié. Pour
changer la donne, allons sur page d’administration de django et créons
une entrée manuellement. Une fois fait, notre page devrait rapatrier
notre première entrée. Vérifiez bien que cela est le cas en utilisant
l’extension vuejs devtools. Et vous verrez dans le composant
StudentAbsence : ``entries:Array[1]``.

Créons maintenant un composant pour afficher notre absence,
``assets/student_absence/studentAbsenceEntry.vue`` :

::

   <template>
       <div>
           <transition appear name="fade">
               <b-card>
                   <b-row>
                       <b-col><strong><a href="#" @click="filterStudent">{{ rowData.student.display }}</a> : </strong>
                       Absent du {{ rowData.date_absence_start }} au {{ rowData.date_absence_end}}.</b-col>
                       <b-col sm="2"><div class="text-right">
                           <b-btn variant="light" size="sm" @click="editEntry" class="card-link">
                               <icon scale="1.3" name="edit" color="green" class="align-text-bottom"></icon>
                           </b-btn>
                           <b-btn variant="light" size="sm" @click="deleteEntry"class="card-link">
                               <icon scale="1.3" name="trash" color="red" class="align-text-bottom"></icon>
                           </b-btn>
                       </div></b-col>
                   </b-row>
               </b-card>
           </transition>
       </div>
   </template>

   <script>
   export default {
       props: {
           rowData : {type: Object},
       },
       data: function () {
           return {
           }
       },
       methods: {
           deleteEntry: function () {
               this.$emit('delete');
           },
           editEntry: function () {
               this.$emit('edit');
           },
           filterStudent: function () {
               this.$emit('filterStudent', this.rowData.student_id);
           },
       },
   }
   </script>

   <style>
   .fade-enter-active {
     transition: opacity .7s
   }
   .fade-enter, .fade-leave-to .fade-leave-active {
     opacity: 0
   }
   </style>

Analysons notre composant. Tout d’abord dans la partie *template*, la
balise ``<transition>`` permet d’ajouter un effet lors de l’apparition
du composant; effet qui est décrit dans la partie *style*. À
l’intérieur, le reste des balises servent principalement à décrire notre
entrée. À noter toutefois, l’appel des différentes méthodes lorsque les
bouttons sont pressés. Ce qui nous amène à la partie *script*, qui elle
comporte un *props*, les données brutes de l’absence fournie par le
composant parent et trois méthodes qui remontent au composant parent
(*StudentAbsence*), lorsqu’un des boutons est pressé.

Insérons donc notre composant dans notre application. Dans la partie
*template* en dessous de la ligne contenant les boutons :

::

               …
               <b-row>
                   <b-col>
                       <student-absence-entry
                       v-for="(entry, index) in entries"
                       v-bind:key="entry.id"
                       v-bind:row-data="entry"
                       @delete="askDelete(entry)"
                       @edit="editEntry(index)"
                       @filterStudent="filterStudent($event)"
                           >
                       </student-absence-entry>
                   </b-col>
               </b-row>
           </b-container>
           …

Dans la partie *script* :

::

   <script>
   …
   import InfirmerieEntry from './infirmerieEntry.vue'
   Vue.component('infirmerie-entry', InfirmerieEntry);

   export default {
       data: function () {
           return {
               menuInfo: {},
               entriesCount: 0,
               entries: [],
               loaded: false,
               currentEntry: null,
           }
       },
       methods: {
           filterStudent: function (matricule) {
           },
           askDelete: function (entry) {
               this.currentEntry = entry;
           },
           editEntry: function(index) {
               this.currentEntry = this.entries[index];
           },
           deleteEntry: function () {
               const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
               axios.delete('/student_absence/api/student_absence/' + this.currentEntry.id + '/', token)
               .then(response => {
                   this.loadEntries();
               });

               this.currentEntry = null;
           },
           loadEntries: function () {
               // Get current absences.
               axios.get('/student_absence/api/student_absence/')
               .then(response => {
                   this.entries = response.data.results;
                   // Everything is ready, hide the loading icon and show the content.
                   this.loaded = true;
               });
           },
       mounted: function () {
           this.menuInfo = menu;

           this.loadEntries();
       },
       components: {
           'app-menu': Menu,
       },
   }
   </script>

Notons que la variable ``currentEntry`` a été ajoutée, elle permet de
retenir l’entrée en cours modification/suppression. Nous savons
maintenant enfin afficher une absence !

Afin de prévenir une suppression inopiné de la part de l’utilisateur, il
serait pertinent d’afficher une fenêtre demandant la confirmation de la
suppression d’où la méthode ``askDelete``. Une telle fenêtre s’appelle
un `modal <https://bootstrap-vue.js.org/docs/components/modal>`__. Ce
qui se traduit en code dans la partie *template* par :

::

           …
           </b-container>
           <b-modal ref="deleteModal" cancel-title="Annuler" hide-header centered
               @ok="deleteEntry" @cancel="currentEntry = null">
               Êtes-vous sûr de vouloir supprimer définitivement cette entrée ?
           </b-modal>
           …

Et pour la méthode ``askDelete`` :

::

           askDelete: function (entry) {
               this.currentEntry = entry;
               this.$refs.deleteModal.show();
           },

Après confirmation, le modal va appeler la méthode ``deleteEntry`` qui
supprimera pour de bon l’entrée.

Il est parfois utile de partager les données d’une variable entre tous
les composants, par exemple les paramètres de l’application ou les
filtres appliqués sur les requêtes. C’est l’excellente librairie
`Vuex <https://vuex.vuejs.org/fr/>`__ qui va nous offrir ces
possibilités, c’est-à-dire un gestionnaire d’état. Pour qu’il soit
utilisable par tous les composants, c’est dans l’application *root*
qu’il doit être implémenté (``assets/js/students_absence/``) :

::

   import Vue from 'vue';

   import Vuex from 'vuex';
   Vue.use(Vuex);

   import StudentAbsence from '../student_absence/student_absence.vue';

   const store = new Vuex.Store({
     state: {
       settings: settings,
       filters: [],
     },
     mutations: {
         addFilter: function (state, filter) {
             // If filter is a matricule, remove name filter to avoid conflict.
             if (filter.filterType === 'matricule_id') {
                 this.commit('removeFilter', 'name');
             }

             // Overwrite same filter type.
             this.commit('removeFilter', filter.filterType);

             state.filters.push(filter);
         },
         removeFilter: function (state, key) {
             for (let f in state.filters) {
                 if (state.filters[f].filterType === key) {
                     state.filters.splice(f, 1);
                     break;
                 }
             }
         }
     }
   });

   var studentAbsenceApp = new Vue({
       el: '#vue-app',
       data: {},
       store,
       template: '<student-absence/>',
       components: { StudentAbsence },
   })

C’est la définition de la variable ``store`` (qui est ajouté à notre
application Vue) qui va créer notre gestionnaire d’état. C’est donc tout
naturellement que ``state`` définit les différents états à gérer. Afin
de s’assurer d’une gestion robuste des états, tous les changements
d’état sont décrits explicitement. Dans notre cas, les paramètres,
``settings``, ne doivent en aucun être modifiés par l’utilisateur, il
n’y a donc rien à décrire. Par contre, les filtres doivent pouvoir être
dynamiquement ajoutés/retirés. D’où les méthodes ``addFilter`` et
``removeFilter`` dans les ``mutations``.

Voyons en pratique ce que cela donne et rajoutons un système de filtre à
notre application. HappySchool fournit un composant qui repose justement
sur l’utilisation du gestionnaire d’état. Le code dans *template* donne
:

::

               <b-row>
                   <b-col>
                       <b-form-group>
                           <div>
                               <b-btn variant="primary" @click="">
                                   <icon name="plus" scale="1" class="align-middle"></icon>
                                   Nouvelle absence
                               </b-btn>
                               <b-btn variant="outline-secondary" v-b-toggle.filters>
                                   <icon name="search" scale="1"></icon>
                                   Ajouter des filtres
                               </b-btn>
                           </div>
                       </b-form-group>
                   </b-col>
               </b-row>
               <b-row>
                   <b-col>
                       <b-collapse id="filters" v-model="showFilters">
                           <b-card>
                               <filters app="student_absence" model="student_absence" ref="filters" @update="applyFilter"></filters>
                           </b-card>
                       </b-collapse>
                   </b-col>
               </b-row>
               <b-pagination class="mt-1" :total-rows="entriesCount" v-model="currentPage" @change="changePage" :per-page="20">
               </b-pagination>
               <b-row>
                   <b-col>
                       <student-absence-entry
                       v-for="(entry, index) in entries"
                       v-bind:key="entry.id"
                       v-bind:row-data="entry"
                       @delete="askDelete(entry)"
                       @edit="editEntry(index)"
                       @filterStudent="filterStudent($event)"
                           >
                       </student-absence-entry>
                   </b-col>
               </b-row>

Et dans la partie *scripts* :

::

   import Filters from '../common/filters.vue'

   import StudentAbsenceEntry from './studentAbsenceEntry.vue'

   export default {
       data: function () {
           return {
               menuInfo: {},
               currentPage: 1,
               entriesCount: 0,
               entries: [],
               filter: '',
               ordering: '&ordering=-datetime_creation',
               loaded: false,
               showFilters: false,
               currentEntry: null,
           }
       },
       methods: {
           changePage: function (page) {
               this.currentPage = page;
               this.loadEntries();
               // Move to the top of the page.
               scroll(0, 0);
               return;
           },
           applyFilter: function () {
               this.filter = "";
               let storeFilters = this.$store.state.filters
               for (let f in storeFilters) {
                   if (storeFilters[f].filterType.startsWith("date")
                       || storeFilters[f].filterType.startsWith("time")) {
                       let ranges = storeFilters[f].value.split("_");
                       this.filter += "&" + storeFilters[f].filterType + "__gt=" + ranges[0];
                       this.filter += "&" + storeFilters[f].filterType + "__lt=" + ranges[1];
                   } else {
                       this.filter += "&" + storeFilters[f].filterType + "=" + storeFilters[f].value;
                   }
               }
               this.currentPage = 1;
               this.loadEntries();
           },
           filterStudent: function (matricule) {
               this.showFilters = true;
               this.$store.commit('addFilter',
                   {filterType: 'student_id', tag: matricule, value: matricule}
               );
               this.applyFilter()
           },
           loadEntries: function () {
               // Get current absences.
               axios.get('/student_absence/api/student_absence/?page=' + this.currentPage + this.filter + this.ordering)
               .then(response => {
                   this.entriesCount = response.data.count;
                   this.entries = response.data.results;
                   // Everything is ready, hide the loading icon and show the content.
                   this.loaded = true;
               });
           },
           …

En plus du filtre, un système de pagination a été ajouté, d’où la
définition des variables ``currentPage`` et ``entriesCount`` ainsi que
la méthode ``changePage``. Pour le filtre en lui-même, deux variables
ont été ajoutées, ``filter`` qui représente la chaîne finale à rajouter
à la requête et ``showFilters`` qui indique la visibilité du composant
``Filters``. Quant aux méthodes, ``applyFilter`` récupère du
gestionnaire d’état les filtres appliqués, produit la variable
``filter`` et recharge les entrées à afficher. ``filterStudent``, lui,
va juste ajouter un filtre manuellement.

Normalement, si l’on clique sur le nom de l’étudiant dans une entrée, le
filtre matricule devrait automatiquement être ajouté et le composant
filtre affiché.

Passons maintenant à notre dernier composant, l’ajout d’une entrée. Pour
cela, créons un nouveau composant,
``assets/student_absence/addStudentModal.vue``, qui proposera à
l’utilisateur d’ajouter/modifier une absence :

::


   <template>
   <div>
       <b-modal size="lg" title="Nouvelle absence"
           ok-title="Soumettre" cancel-title="Annuler"
           ref="addStudentModal"
           :ok-disabled="!student.matricule || (!form.morning && !form.afternoon)"
           @ok="addAbsence" @hidden="resetAbsence"
           >
           <b-form>
               <b-form-row>
                   <b-col sm="8">
                       <b-form-group label="Étudiant :" label-for="input-student" :state="inputStates.student">
                           <multiselect id="input-name"
                               :internal-search="false"
                               :options="studentOptions"
                               @search-change="getStudentOptions"
                               :loading="studentLoading"
                               placeholder="Rechercher un étudiant…"
                               select-label=""
                               selected-label="Sélectionné"
                               deselect-label=""
                               label="display"
                               track-by="matricule"
                               v-model="student"
                               >
                               <span slot="noResult">Aucune personne trouvée.</span>
                               <span slot="noOptions"></span>

                           </multiselect>
                           <span slot="invalid-feedback">{{ errorMsg('student_id') }}</span>
                       </b-form-group>
                   </b-col>
                   <b-col sm="4">
                       <b-form-group label="Matricule :" label-for="input-matricule">
                           <b-form-input id="input-matricule" type="text" v-model="student.matricule" readonly></b-form-input>
                       </b-form-group>
                   </b-col>
               </b-form-row>
               <b-form-row class="mt-4">
                   <b-col>
                       <b-form-row>
                           <b-form-group label="À partir du" :state="inputStates.date_absence_start">
                               <input type="date" v-model="form.date_absence_start" :max="form.date_absence_end"/>
                               <span slot="invalid-feedback">{{ errorMsg('date_absence_start') }}</span>
                           </b-form-group>
                       </b-form-row>
                   </b-col>
                   <b-col>
                       <b-form-row>
                           <b-form-group label="Jusqu'au" :state="inputStates.date_absence_end">
                               <input type="date" v-model="form.date_absence_end" :min="form.date_absence_start"/>
                               <span slot="invalid-feedback">{{ errorMsg('date_absence_end') }}</span>
                           </b-form-group>
                       </b-form-row>
                   </b-col>
               </b-form-row>
               <b-form-row>
                   <b-form-group label="Matin/Après-midi :">
                           <b-form-checkbox v-model="form.morning">
                               Matin
                           </b-form-checkbox>
                           <b-form-checkbox v-model="form.afternoon">
                               Après-midi
                           </b-form-checkbox>
                   </b-form-group>
               </b-form-row>
           </b-form>
       </b-modal>
   </div>
   </template>

   <script>
   import Multiselect from 'vue-multiselect'
   import 'vue-multiselect/dist/vue-multiselect.min.css'

   import axios from 'axios';
   window.axios = axios;
   window.axios.defaults.baseURL = window.location.origin; // In order to have httpS.

   export default {
       props: ['entry'],
       data: function () {
           return {
               form: {
                   student_id: null,
                   date_absence_start: null,
                   date_absence_end: null,
                   morning: true,
                   afternoon: true,
               },
               student: {matricule: null},
               studentOptions: [],
               studentLoading: false,
               inputStates: {
                   student: null,
                   date_absence_start: null,
                   date_absence_end: null,
               },
               errors: {},
               searchId: -1,
           }
       },
       watch: {
           'form.date_absence_start': function (date) {
               if (this.form.date_absence_end === null) this.form.date_absence_end = date;
           },
           entry: function (entry, oldEntry) {
               this.setEntry(entry);
           },
           errors: function (newErrors, oldErrors) {
               let inputs = Object.keys(this.inputStates);
               for (let u in inputs) {
                   if (inputs[u] in newErrors) {
                       this.inputStates[inputs[u]] = newErrors[inputs[u]].length == 0;
                   } else {
                       this.inputStates[inputs[u]] = null;
                   }
               }
           },
       },
       methods: {
           show: function () {
               this.$refs.addStudentModal.show();
           },
           hide: function () {
               this.$refs.addStudentModal.hide();
           },
           resetAbsence: function () {
               this.$emit('reset');

               this.form = {
                   student_id: null,
                   date_absence_start: null,
                   date_absence_end: null,
                   morning: true,
                   afternoon: true,
               };
               this.student =  {matricule: null};
           },
           setEntry: function (entry) {
               if (entry) {
                   this.student = entry.student;
                   this.form = {
                       student_id: entry.student.matricule,
                       date_absence_start: entry.date_absence_start,
                       date_absence_end: entry.date_absence_end,
                       morning: entry.morning,
                       afternoon: entry.afternoon,
                       id: entry.id,
                   }
               } else {
                   this.resetAbsence();
               }
           },
           addAbsence: function (evt) {
               // Prevent form to be sent.
               evt.preventDefault();

               this.form.student_id = this.student.matricule;

               let modal = this;
               const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
               let path = '/student_absence/api/student_absence/';
               if (this.entry) path += this.entry.id + '/'

               const send = this.entry ? axios.put(path, this.form, token) : axios.post(path, this.form, token);
               send.then(response => {
                   this.hide();
                   this.errors = {};
                   this.$emit('update');
               }).catch(function (error) {
                   modal.errors = error.response.data;
               });

               this.entry = null;
           },
           getStudentOptions: function (query) {
               let app = this;
               this.searchId += 1;
               let currentSearch = this.searchId;
               this.studentLoading = true;

               const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
               const data = {
                   query: query,
                   teachings: this.$store.state.settings.teachings,
                   people: 'student',
                   check_access: false,
               };
               axios.post('/annuaire/api/people/', data, token)
               .then(response => {
                   // Avoid that a previous search overwrites a faster following search results.
                   if (this.searchId !== currentSearch)
                       return;

                   const options = response.data.map(p => {
                       // Format entries.
                       let entry = {display: p.last_name + " " + p.first_name, matricule: p.matricule};
                       // It's a student.
                       entry.display += " " + p.classe.year + p.classe.letter.toUpperCase();
                       entry.display += " – " + p.teaching.display_name;
                       return entry;
                   });
                   this.studentLoading = false;
                   this.studentOptions = options;
               })
               .catch(function (error) {
                   alert(error);
                   app.studentLoading = false;
               });
           },
           errorMsg(err) {
               if (err in this.errors) {
                   return this.errors[err][0];
               } else {
                   return "";
               }
           },
       },
       components: {Multiselect},
       mounted: function () {
           if (this.entry) this.setEntry(this.entry);

           this.show();
       },
   }
   </script>

Il y a pas mal de chose à dire concernant ce composant. De manière
générale, il est composé de composants venant de *Bootstrap-vue* à
l’exception de ```multiselect`` <https://vue-multiselect.js.org/>`__ qui
propose un champ de recherche et de sélection modulable. Si nous y
regardons de plus près, la propriété ``@search-change`` indique quelle
méthode est appelée lorsqu’une recherche est effectué, dans notre cas
``getStudentOptions``. Celle-ci fait un appel à notre API
``/annuaire/api/people/`` puis formate la réponse reçue et assigne le
résultat à la variable ``studentOptions`` que le composant *multiselect*
va utiliser.

Autre particularité, la gestion des erreurs. En effet, s’il manque une
donnée ou que l’une d’entre-elles est mal formaté/incorrecte, le
*sérialiseur* de notre API va retourner une erreur et indiquer de quelle
type elle est. Nous pouvons voir dans la méthode ``addAbsence``, qu’en
cas d’erreur le retour est assigné à la variable ``errors`` du composant
:

::

   let modal = this;

   send.then(response => {
       this.hide();
       this.errors = {};
       this.$emit('update');
   }).catch(function (error) {
       modal.errors = error.response.data;
   });

Du côté de l’interface utilisateur, chaque ``input`` possède une
propriété ``state``, indiquant si le champ possède une erreur (trois
valeurs possible, ``null``, ``true``, ``false``). Vue permet de réagir
dès qu’une variable change, dès qu’une erreurs est détectée dans le
``watch`` du composant, l’état est mis à jour de manière appropriée. La
méthode ``errorMsg()`` quant à elle, permettra d’afficher la bonne
erreur pour l’\ *input* correspondant.

De manière similaire, si la *props* ``entry`` est modifiée, par exemple
lorsque l’utilisateur veut modifier une entrée, le formulaire sera
pré-rempli ou vidé après la création/modification d’une entrée afin de
préparer le prochain ajout/modification.

Il ne nous reste plus qu’à intégrer ce *modal* à notre instance Vue
principale :

::


   <template>
       <div>
           <div class="loading" v-if="!loaded"></div>
           <app-menu :menu-info="menuInfo"></app-menu>
           <b-container v-if="loaded">
               <b-row>
                   <h2>Absence des élèves</h2>
               </b-row>
               <b-row>
                   <b-col>
                       <b-form-group>
                           <div>
                               <b-btn variant="primary" @click="openDynamicModal('add-student-modal')">
                                   <icon name="plus" scale="1" class="align-middle"></icon>
                                   Nouvelle absence
                               </b-btn>
                               <b-btn variant="outline-secondary" v-b-toggle.filters>
                                   <icon name="search" scale="1"></icon>
                                   Ajouter des filtres
                               </b-btn>
                           </div>
                       </b-form-group>
                   </b-col>
               </b-row>
               <b-row>
                   <b-col>
                       <b-collapse id="filters" v-model="showFilters">
                           <b-card>
                               <filters app="student_absence" model="student_absence" ref="filters" @update="applyFilter"></filters>
                           </b-card>
                       </b-collapse>
                   </b-col>
               </b-row>
               <b-pagination class="mt-1" :total-rows="entriesCount" v-model="currentPage" @change="changePage" :per-page="20">
               </b-pagination>
               <b-row>
                   <b-col>
                       <student-absence-entry
                       v-for="(entry, index) in entries"
                       v-bind:key="entry.id"
                       v-bind:row-data="entry"
                       @delete="askDelete(entry)"
                       @edit="editEntry(index)"
                       @filterStudent="filterStudent($event)"
                           >
                       </student-absence-entry>
                   </b-col>
               </b-row>
           </b-container>
           <component
               v-bind:is="currentModal" ref="dynamicModal"
               :entry="currentEntry"
               @update="loadEntries"
               @reset="currentEntry = null">
           </component>
           <b-modal ref="deleteModal" cancel-title="Annuler" hide-header centered
               @ok="deleteEntry" @cancel="currentEntry = null">
               Êtes-vous sûr de vouloir supprimer définitivement cette entrée ?
           </b-modal>
       </div>
   </template>

   <script>
   import Vue from 'vue';
   import BootstrapVue from 'bootstrap-vue'
   Vue.use(BootstrapVue);

   import 'vue-awesome/icons'
   import Icon from 'vue-awesome/components/Icon.vue'
   Vue.component('icon', Icon);

   import axios from 'axios';

   import Filters from '../common/filters.vue'
   import Menu from '../common/menu.vue'

   import StudentAbsenceEntry from './studentAbsenceEntry.vue'
   import AddStudentModal from './addStudentModal.vue'

   export default {
       data: function () {
           return {
               menuInfo: {},
               currentPage: 1,
               entriesCount: 0,
               entries: [],
               filter: '',
               ordering: '&ordering=-datetime_creation',
               loaded: false,
               showFilters: false,
               currentModal: '',
               currentEntry: null,
           }
       },
       methods: {
           changePage: function (page) {
               this.currentPage = page;
               this.loadEntries();
               // Move to the top of the page.
               scroll(0, 0);
               return;
           },
           openDynamicModal: function (modal) {
               this.currentModal = modal;
               if ('dynamicModal' in this.$refs) this.$refs.dynamicModal.show();
           },
           applyFilter: function () {
               this.filter = "";
               let storeFilters = this.$store.state.filters
               for (let f in storeFilters) {
                   if (storeFilters[f].filterType.startsWith("date")
                       || storeFilters[f].filterType.startsWith("time")) {
                       let ranges = storeFilters[f].value.split("_");
                       this.filter += "&" + storeFilters[f].filterType + "__gt=" + ranges[0];
                       this.filter += "&" + storeFilters[f].filterType + "__lt=" + ranges[1];
                   } else {
                       this.filter += "&" + storeFilters[f].filterType + "=" + storeFilters[f].value;
                   }
               }
               this.currentPage = 1;
               this.loadEntries();
           },
           filterStudent: function (matricule) {
               this.showFilters = true;
               this.$store.commit('addFilter',
                   {filterType: 'student_id', tag: matricule, value: matricule}
               );
               this.applyFilter()
           },
           loadEntries: function () {
               // Get current absences.
               axios.get('/student_absence/api/student_absence/?page=' + this.currentPage + this.filter + this.ordering)
               .then(response => {
                   this.entriesCount = response.data.count;
                   this.entries = response.data.results;
                   // Everything is ready, hide the loading icon and show the content.
                   this.loaded = true;
               });
           },
           askDelete: function (entry) {
               this.currentEntry = entry;
               this.$refs.deleteModal.show();
           },
           editEntry: function(index) {
               this.currentEntry = this.entries[index];
               this.openDynamicModal('add-student-modal');
           },
           deleteEntry: function () {
               const token = { xsrfCookieName: 'csrftoken', xsrfHeaderName: 'X-CSRFToken'};
               axios.delete('/student_absence/api/student_absence/' + this.currentEntry.id + '/', token)
               .then(response => {
                   this.loadEntries();
               });

               this.currentEntry = null;
           },
       },
       mounted: function () {
           this.menuInfo = menu;

           this.loadEntries();
       },
       components: {
           'filters': Filters,
           'app-menu': Menu,
           'student-absence-entry': StudentAbsenceEntry,
           'add-student-modal': AddStudentModal,
       },
   }
   </script>

   <style>
   .loading {
     content: " ";
     display: block;
     position: absolute;
     width: 80px;
     height: 80px;
     background-image: url(/static/img/spin.svg);
     background-size: cover;
     left: 50%;
     top: 50%;
   }
   </style>

L’ajout est somme toute assez simple. Nous importons le composant et
nous rajoutons une méthode pour ouvrir le *modal*. Petite particularité,
non nécessaire pour notre application, nous avons laissé la possibilité
d’ouvrir différents *modals*. En effet, le type de *modal*, et donc de
composant, est dynamiquement chargé et affiché grâce à la propriété
``currentModal`` qui retient le composant courant en mémoire. Nous
aurions très bien pu utiliser ce mécanisme pour la demande de
suppression d’une entrée.

Ceci clôture cette première approche de la création d’une application.
Pour aller plus loin, un coup d’œil à l’application *infirmerie* ou,
encore plus complexe, *dossier_eleve* qui donnent une bonne vision de ce
que peut être en condition réelle une application dans HappySchool.
N’hésitez surtout pas à apporter des corrections à ces explications et à
HappySchool de manière générale.
