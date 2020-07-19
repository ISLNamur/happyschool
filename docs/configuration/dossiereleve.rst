Dossier des élèves
==================

Le dossier des élèves est permet de gérer les informations personnelles et éducatives (dont les
sanctions) des élèves. La volonté derrière cette application est double. D'une part, d'avoir un
accès rapide de l'historique d'un élève. D'autre part, d'avoir un suivi journalier des
informations. Il permet ainsi le suivi des sanctions (la retenue a-t-elle bien été faite ?) ainsi
que la communication, concernant un élève, aux professeurs et aux parents.

Paramètres
----------

Les paramètres sont gérés par le modèle ``DossierEleveSettingsModel``.

Demandes de sanction
^^^^^^^^^^^^^^^^^^^^

HappySchool propose deux modes de fonctionnement vis-à-vis des sanctions. Un mode "simple" sans
suivi où ce qui ajouté au dossier est considéré comme fait. Et un mode de "demande" où certaines
sanctions, typiquement les retenues, passent par une ou deux étapes de validation. Ainsi une
sanction peut être validée par l'équipe éducative (conseil de discipline) avant sa communication
avec l'élève et ses parents, mais elle peut aussi être actée après sa réalisation et ainsi
s'assurer que ce qui se trouve dans le dossier correspond bien à la réalité.

Par défaut, c'est le mode "Demande" qui est activé avec le paramètre ``enable_submit_sanctions``.

Conseil de discipline
^^^^^^^^^^^^^^^^^^^^^

Si les demandes de sanctions activées, la possibilité de passer par une étape de confirmation
(facultative) par l'équipe éducative peut être activée par le paramètre ``enable_disciplinary_council``.

Visibilité
^^^^^^^^^^

Le dossier des élèves dispose d'un système relativement flexible d'accès à l'**information**. Ainsi il
est possible d'obliger certains groupes à donner la visibilité des infos à d'autres groupes ou de
laisser la possibilité à l'utilisateur de rendre accessible à d'autres groupes. Par exemple,
toute information laisser par un éducateur pourrait obligatoirement être visible aux membres de la
direction mais la visibilité aux professeurs se ferait au cas par cas. Ou encore, une information
ne pourrait être accessible qu'à celui qui l'a postée.

Pour le moment, les sanctions ne sont pas affectées par ce système de visibilité.

C'est la série de paramètres ``group_allow_visibility_to`` et ``group_force_visibility_to`` qui
permet de contrôler le comportement d'accès. ``group_allow_visibility_to`` indique la liste des
groupes qui seront visibles lors de l'ajout d'une information par le membre de ``group``. Tandis
que ``group_force_visibility_to`` oblige l'information à être visible par le groupe. Si un groupe
ce trouve simultanément dans ``allow`` et ``force``, le groupe sera bien dans la liste visible par
l'utilisateur mais sera coché et non-modifiable.

Accès enseignant
^^^^^^^^^^^^^^^^

Par défaut, seuls les titulaires ont accès aux informations de leurs élèves. Toutefois, il peut
être préférable que l'ensemble des professeurs qui ont la classe ou qui donnent cours à un élève
aient accès aux informations les concernant. Le paramètre ``filter_teacher_entries_by_tenure``
permet de gérer cet accès.

Courriel de l'enseignant
^^^^^^^^^^^^^^^^^^^^^^^^

Le paramètre ``use_school_email`` permet de choisir, lors de l'envoit de courriel, entre le
courriel personnel du professeur ou celui de l'école (champ ``email_school`` dans le modèle
``ResponsibleModel``).
