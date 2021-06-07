Happy School
================
![Build Status](https://github.com/ISLNamur/happyschool/actions/workflows/django.yml/badge.svg)

.github/workflows/
HappySchool est une application web de gestion administrative et pédagogique
pour les écoles primaires et secondaires. Fruit d'une expérience de terrain,
il se veut simple d'utilisation tout en restant configurable afin de s'adapter
aux particularités des établissements scolaires.

HappySchool est constitué d'une série d'applications indépendantes qui peuvent
activés/désactivés selon les besoins:

- Un **annuaire** des élèves et des enseignants (la seule obligatoire). Elle permet de
  trouver une personne par nom/classe et d'afficher des informations la concernant,
  de générer un trombinoscope par classe ou encore d'avoir un rapide aperçu par
  rapport aux autres applications.
- Un **dossier des élèves** qui permet d'assurer un suivi des élèves que ce soit au niveau
  des informations personnelles que des sanctions. Il propose également de gérer le suivi
  des sanctions, les demandes, organiser des conseils disciplinaires ainsi que le
  vérifier la présence pour les retenues.
- Une prise des **absences des élèves** qui fonctionne sur tablette et hors-connexion.
  Deux interfaces ont été développées, une pour les éducateurs et une pour les enseignants.
- Une gestion des arrivées et sorties de l'**infirmerie** avec une notification automatique
  par courriel aux différents responsables de l'école.
- Une gestion des **appels** au travers d'une notification de la raison de l'appel par
  exemple, en notifiant un éducateur qu'un parent à prévenu que tel élève serait absent
  pour de cause de maladie.
- Un suivi des **absences des professeurs** pour la gestion administrative.
- Un suivi des **changements horaires** inhabituelles des enseignants afin d'avoir une
  connaissance centralisé d'où se trouve les élèves.

HappySchool s'appuie sur toute une série de projets opensource dont les frameworks
[Django](https://www.djangoproject.com/) et [Vue.js](https://vuejs.org/).


Ressources
----------

- [La documentation](https://happyschool.readthedocs.io/)
- [Serveur de test (libre accès)](https://test.happyschool.be/) (utilisateur/mot de passe : directeur/happyschool)
- [Site officiel](https://github.com/ISLNamur/happyschool)
