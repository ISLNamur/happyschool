.. HappySchool documentation master file, created by
   sphinx-quickstart on Sun Mar  8 14:05:24 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentation HappySchool
=========================

HappySchool est une application web de gestion administrative et pédagogique
pour les écoles primaires et secondaires. Fruit d'une expérience de terrain,
elle se veut simple d'utilisation tout en restant configurable afin de s'adapter
aux particularités des établissements scolaires.

HappySchool est constitué d'une série d'applications indépendantes qui peuvent
être activés/désactivés selon les besoins:

- Un **annuaire** des élèves et des enseignants (la seule partie obligatoire). Elle
  permet de trouver une personne par nom/classe et d'afficher des informations
  la concernant,
  de générer un trombinoscope par classe ou encore d'avoir un rapide aperçu des
  aux autres applications.
- Un **dossier des élèves** qui permet d'assurer un suivi des élèves que ce
  soit au niveau des informations personnelles ou des sanctions. Il propose
  également de gérer le suivi des sanctions, les demandes, organiser des
  conseils disciplinaires ainsi que le vérifier la présence pour les retenues.
- Une prise des **absences des élèves** qui fonctionne sur tablette et
  hors-connexion. Deux interfaces ont été développées, une pour les éducateurs
  et une pour les enseignants.
- Une gestion des arrivées et sorties de l'**infirmerie** avec une notification
  automatique par courriel aux différents responsables de l'école.
- Une gestion des **appels** au travers de notifications. Par exemple, en notifiant
  un éducateur qu'un élève serait absent pour de cause de maladie suite à
  l'appel d'un parent.
- Un suivi des **absences des professeurs** pour la gestion administrative.
- Un suivi des **changements horaires** inhabituelles des enseignants afin
  d'avoir une connaissance centralisé d'où doivent se trouver les élèves.
  Ceux-ci peuvent être affichés sur un grand écran d'affichage.

HappySchool s'appuie sur toute une série de projets opensource dont les frameworks
`Django <https://www.djangoproject.com/>`_ et `Vue.js <https://vuejs.org/>`_.


.. _installation:

.. toctree::
   :maxdepth: 3

   installation/index

.. _configuration:

.. toctree::
   :maxdepth: 3

   configuration/index

.. _utilisation:

.. toctree::
   :maxdepth: 3

   utilisation/index

.. _developpement:

.. toctree::
   :maxdepth: 3

   developpement/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
