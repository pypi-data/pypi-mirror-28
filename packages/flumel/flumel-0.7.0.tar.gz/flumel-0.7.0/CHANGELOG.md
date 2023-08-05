# Journal des modifications

Ce fichier est généré automatiquement après chaque modification du dépôt. 
Les numéros indiqués correspondent aux [versions taggées](https://gitlab.com/canarduck/flumel/tags).

## Prochaine version

### 🆕 Nouveautés

* Detection des rejets dans les mails. [Renaud Canarduck]
* Init système de gestion des rejets mail en base. [Renaud Canarduck]
* Nom du flux en expéditeur du mail. [Renaud Canarduck]

### 🐛 Correctifs

* Tests sécurité requirements uniquement pour tags. [Renaud Canarduck]

## v0.6.1 (2017-12-31)

### 🆕 Nouveautés

* Init export opml. [Renaud Canarduck]

### ⇔ Changements

* Simplification du gabarits des mails html. [Renaud Canarduck]

### 🐛 Correctifs

* Utilisation seulement fulltext si > au flux. [Renaud Canarduck]

## v0.6.0 (2017-12-27)

### ⇔ Changements

* Remplacement newspaper par readability. [Renaud Canarduck]

## v0.5.2 (2017-12-26)

### 🐛 Correctifs

* Gestion erreur newspaper.download() [Renaud Canarduck]

## v0.4.9 (2017-12-26)

### ⇔ Changements

* Fin de l'utilisation du NLP pour extraire mots clés. [Renaud Canarduck]

## v0.4.8 (2017-12-26)

### ⇔ Changements

* Séparation login/mdp imap & smtp. [Renaud Canarduck]
* Séparation login/mdp imap & smtp. [Renaud Canarduck]

## v0.4.7 (2017-12-26)

### 🐛 Correctifs

* Ajout tpl email texte brut. [Renaud Canarduck]

## v0.4.6 (2017-12-26)

### ⇔ Changements

* Récupértion date entry via updated plutôt que published. [Renaud Canarduck]

## v0.4.5 (2017-12-26)

### 🐛 Correctifs

* Correction port par défaut imap / ssl. [Renaud Canarduck]

## v0.4.3 (2017-12-26)

### ⇔ Changements

* Utilisation de string.Template au lieu de string.format. [Renaud Canarduck]

### ∞ Autres

* Merge branch 'master' of gitlab.com:canarduck/flumel. [Renaud Canarduck]

## v0.4.2 (2017-12-26)

### ⇔ Changements

* Désactivation de l'interpolation  dans ConfigParser pour autoriser les % [Renaud Canarduck]

## v0.4.1 (2017-12-19)

### 🆕 Nouveautés

* Test des failles de sécurité des dépendances. [Renaud Canarduck]

### ⇔ Changements

* Test des failles de sécurité des dépendances dev. [Renaud Canarduck]

### 🐛 Correctifs

* Génération changelog. [Renaud Canarduck]

## v0.4.0 (2017-12-10)

### 🆕 Nouveautés

* Slogan de l'instance. [Renaud Canarduck]
* Us: ajout variable INSTANCE_NAME. [Renaud Canarduck]
* Intégration premailer. [Renaud Canarduck]
* Système de personalisation des gabarits. [Renaud Canarduck]
* Init du support des gabarits personnalisés. [Renaud Canarduck]

### 🐛 Correctifs

* Suppression des styles non standardisés dans html. [Renaud Canarduck]
* Gestion du on_delete cascade sur la clé feed des Subscription. [Renaud Canarduck]

## v0.3.0 (2017-11-29)

### 🆕 Nouveautés

* Utilisation de fake_useragent pour passer les bloquages des crawlers. [Renaud Canarduck]

### ⇔ Changements

* Mise à jour de la documention dédiée à l'installation. [Renaud Canarduck]
* Amélioration de la CLI. [Renaud Canarduck]
* La tâche init execute les 3 tâches d'initialisation de flumel. [Renaud Canarduck]
* Amélioration documentation dédiée à l'installation. [Renaud Canarduck]

### ∞ Autres

* Punkt. [Renaud Canarduck]

## v0.2.0 (2017-11-26)

### 🐛 Correctifs

* Regex abo/désabo. [Renaud Canarduck]
* Décodage sujet emails. [Renaud Canarduck]
* Typo sur url ww2w. [Renaud Canarduck]
* Mode TESTING. [Renaud Canarduck]
* SetUpClass pour les tests fonctionnels. [Renaud Canarduck]
* Le résultat d'une task huey est un objet. [Renaud Canarduck]
* Huey en mode thread plutôt que greenlet. [Renaud Canarduck]

## v0.1.0 (2017-11-19)

### 🆕 Nouveautés

* Coverage html report sur gitlab. [Renaud Canarduck]
* CLI pour amorcer le fichier de configuration. [Renaud Canarduck]
* Découplage des tâches et mise en place de huey. [Renaud Canarduck]
* Detection de flux sur une page. [Renaud Canarduck]
* Init tests subscriptions. [Renaud Canarduck]

### ⇔ Changements

* Docker dédié aux services mails. [Renaud Canarduck]

### 🐛 Correctifs

* Test sur les modèles. [Renaud Canarduck]
* Nettoyage imap avant vérification désinscription. [Renaud Canarduck]
* Pour peewee delete_instance au lieu de delete. [Renaud Canarduck]
* Test get_or_create feed avec 2 titres différents.. [Renaud Canarduck]
* Code de retour désabonnement. [Renaud Canarduck]
* Gestion smtp sans auth. [Renaud Canarduck]
* Gestion smtp sur port 25. [Renaud Canarduck]
* Nettoyage dépendances. [Renaud Canarduck]
* Gestion flux invalide. [Renaud Canarduck]
* Decorateur tasks. [Renaud Canarduck]
* Mise à jour de la documentation. [Renaud Canarduck]
* Simplification du service flumel. [Renaud Canarduck]
* Refactorisation. [Renaud Canarduck]
* Avancement tests subscribe / unsubscribe. [Renaud Canarduck]

## v0.0.2 (2017-11-12)

### 🆕 Nouveautés

* Logo. [Renaud Canarduck]
* Modèles de fichiers pour systemd. [Renaud Canarduck]
* Generateur de page d’info. [Renaud Canarduck]
* Interface en ligne de commande. [Renaud Canarduck]
* Init mkdocs sur readthedocs. [Renaud Canarduck]
* Boucle de traitement de la boite mail. [Renaud Canarduck]
* Settings pour logger. [Renaud Canarduck]
* Regex dans le fichier de config. [Renaud Canarduck]
* Envoi des articles par mail. [Renaud Canarduck]
* Templates pour les notifications de base. [Renaud Canarduck]
* Premier template de mail. [Renaud Canarduck]
* Mise en place d'un fichier de configuration. [Renaud Canarduck]
* Analyse des articles par newspaper. [Renaud Canarduck]
* Champs pour gérer les headers de modification des flux. [Renaud Canarduck]
* Vérification du flux avant abonnement. [Renaud Canarduck]
* Base pour les modèles & les notifications. [Renaud Canarduck]
* Init de la structure du projet. [Renaud Canarduck]

### 🐛 Correctifs

* Amélioration template page. [Renaud Canarduck]
* Ignorer build pypi. [Renaud Canarduck]
* Typo settings. [Renaud Canarduck]
* Simplification accueil de la doc et création d'une page pourquoi. [Renaud Canarduck]
* Correctif template article. [Renaud Canarduck]
* Suppression d'un flux quand plus personne n'y est abonné. [Renaud Canarduck]
* Suppression debug inutile. [Renaud Canarduck]
* Refaco regex bot. [Renaud Canarduck]
* Nettoyage arborescence. [Renaud Canarduck]
* Amélioration des emails. [Renaud Canarduck]
* Logger sur notification au lieu des print. [Renaud Canarduck]
* Simplification de la doc. [Renaud Canarduck]
* Simplification du model. [Renaud Canarduck]

### ∞ Autres

* Init. [Renaud Canarduck]

