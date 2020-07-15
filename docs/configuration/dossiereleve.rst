Configuration du dossier des élèves
===================================

Le dossier des élèves est permet de gérer les informations personnelles et éducatives (dont les sanctions) des élèves. La volonté derrière cette application est double. D'une part, d'avoir un accès rapide de l'historique d'un élève. D'autre part, d'avoir un suivi journalier des informations. Il permet ainsi le suivi des sanctions (la retenue a-t-elle bien été faite ?) ainsi que la communication, concernant un élève, aux professeurs et aux parents.

Paramètres
----------

Les paramètres sont gérés par le modèle ``DossierEleveSettingsModel``.

Demandes de sanction
^^^^^^^^^^^^^^^^^^^^

HappySchool propose deux modes de fonctionnement vis-à-vis des sanctions. Un mode "simple" sans suivi où ce qui ajouté au dossier est considéré comme fait. Et un mode de "demande" où certaines sanctions, typiquement les retenues, passent par une ou deux étapes de validation. Ainsi une sanction peut être validée par l'équipe éducative (conseil de discipline) avant sa communication avec l'élève et ses parents, mais elle peut aussi être actée après sa réalisation et ainsi s'assurer que ce qui se trouve dans le dossier correspond bien à la réalité.

Par défaut, c'est le mode "Demande" qui est activé avec le paramètre ``enable_submit_sanctions``.

Conseil de discipline
^^^^^^^^^^^^^^^^^^^^^

Si les demandes de sanctions activées, la possibilité de passer par une étape de confirmation (facultative) par l'équipe éducative peut être activée par le paramètre ``enable_disciplinary_council``.
