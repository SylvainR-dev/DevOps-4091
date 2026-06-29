# Commencer par hosts_aws

* Ligne 1 — Le groupe
all est un groupe spécial qui signifie "toutes les machines". Tu peux créer tes propres groupes, par exemple [webservers] ou [databases], pour cibler des machines spécifiques dans ton playbook.

* Ligne 2 — La machine cible

    C'est la définition de la machine avec 3 informations :
    - 54.242.221.254 → l'IP publique de l'EC2 sur AWS
    - ansible_ssh_user=ubuntu → l'utilisateur SSH à utiliser pour se connecter (sur Ubuntu c'est toujours ubuntu, pas root ni ec2-user)
    - ansible_ssh_private_key_file → le chemin vers la clé privée générée par Terraform, pour s'authentifier en SSH


# deploy.yml

* En-tête du playbook

    - Le "name", c’est juste une description pour dire ce que fait cette étape. 
    - Le "hosts : all" signifie que cette tâche s’applique à tous les serveurs que tu as définis. 
    - Le "become : true" veut dire qu’Ansible va utiliser des privilèges élevés, en général en devenant root, pour exécuter les commandes. Donc, c’est une première section qui pose le cadre pour la suite.


* Task 1 — Installer Nginx
    - apt → le gestionnaire de paquets d'Ubuntu
    - state: present → "installe si pas déjà installé"
    - update_cache: yes → fait un apt update avant d'installer

Ansible va exécuter une action pour installer Nginx sur les serveurs que tu as ciblés.
Nginx, c’est un logiciel qui sert à faire tourner un site web ou à faire passer des requêtes. AWS, lui, c’est un cloud entier qui te fournit l’infrastructure. Nginx, c’est juste un service qui tourne sur une machine.


* Task 2 — Créer le répertoire
    - Crée le dossier où sera déployée l'app Angular
    - mode: '0755' → permissions lecture/exécution pour tout le monde, écriture uniquement pour le propriétaire

Cette tâche, elle va créer un répertoire sur tes serveurs pour ton application (dans le cloud). Le "path", c’est l’emplacement exact de ce répertoire. "State: directory", ça dit qu’on veut un dossier (et non un fichier). Le "mode", c’est les permissions, par exemple qui peut lire, écrire ou exécuter.



* Task 3 — Copier l'app Angular
    - Copie les fichiers depuis ta machine locale vers l'EC2
    - src → chemin relatif depuis le playbook sur ta machine
    - dest → chemin sur l'EC2
    - mode: '0644' → permissions lecture pour tout le monde, écriture uniquement pour le propriétaire

D’abord, tu crées l’endroit où ton application va résider sur les serveurs (étape précédente). Ensuite, en copiant les fichiers, tu apportes ton application (par exemple ton projet Angular) depuis ton poste vers les serveurs. Ainsi, une fois copié, c’est prêt à être servi par Nginx ou tout autre service


* Task 4 — Copier la config Nginx
    - Copie le fichier de config Nginx dans sites-available
    - notify = déclenche le handler Redémarrer Nginx si cette task modifie quelque chose

Cette tâche consiste à prendre ton fichier de configuration Nginx que tu as localement et à le copier sur les serveurs. Ce fichier dit à Nginx comment servir ton application. En gros, c’est ce qui configure Nginx pour qu’il sache où et comment répondre aux requêtes.
Le "src" (source) est le fichier de configuration qui se trouve sur ta machine locale. Le "dest" (destination), c’est là où Ansible va le placer sur tes serveurs dans le cloud.


* Task 5 — Activer la config Nginx
    - Crée un lien symbolique de sites-available vers sites-enabled
    - C'est comme ça que Nginx active un site — il lit uniquement les configs dans sites-enabled
    - state: link → dit à Ansible de créer un lien symbolique

cette étape consiste à faire en sorte que Nginx utilise vraiment ton fichier de configuration. Typiquement, ça peut être un lien symbolique vers le répertoire des configurations actives ou la commande pour recharger Nginx. En clair, après avoir copié la config, cette étape s’assure que Nginx s’en sert réellement pour servir ton application.



* Handler — Redémarrer Nginx
    - Un handler s'exécute uniquement si une task l'a notifié avec notify
    - Et il s'exécute une seule fois à la fin du playbook, même si plusieurs tasks l'ont notifié
    - Ici il redémarre Nginx pour prendre en compte la nouvelle config


Un handler, c’est une action spéciale qu’Ansible déclenche uniquement si une tâche le demande. Ici, si ta config change, Ansible sait qu’il doit redémarrer Nginx. Le nom, c’est juste un repère, et le service, c’est Nginx avec son état, ici restart. En gros, c’est une manière d’automatiser des actions de maintenance, comme redémarrer le service après un changement.

Le handler est une action prédéfinie qu’Ansible n’exécute que si nécessaire, par exemple après un changement. Ça t’évite de redémarrer Nginx sans raison, et ça assure que tout reste cohérent après des modifications.


# COMMANDE = ansible-playbook -i hosts deploy.yml
tu dis à Ansible de se baser sur ton inventaire (le fichier hosts) pour savoir sur quels serveurs se connecter. Ensuite, il va appliquer toutes les tâches définies dans ton playbook deploy.yml sur ces serveurs, automatisant ainsi ton déploiement.

Sans préciser l’inventaire avec « -i hosts », Ansible ne saura pas sur quelles machines il doit travailler. Donc, l’inventaire, c’est ce qui fait le lien entre ton playbook et tes serveurs. Donc, toujours préciser l’inventaire


# Vérifier que l'app est bien accessible : 

* 1. tester la connectivité Ansible avec ping
ansible all -i hosts_aws -m ping

* 2. Vérifier que l'app était accessible, avec le navigateur avec l'IP publique



# LE FLUX

hosts_aws
   │
   │ (définit les machines cibles)
   ▼
deploy.yml
   │
   │ (définit ce qu'on fait sur ces machines)
   ▼
ansible-playbook -i hosts_aws deploy.yml
   │
   │ (exécute le playbook sur les machines de l'inventaire)
   ▼
[App déployée sur l'EC2]





# le flux du playbook - deploy

Installer Nginx
      │
      ▼
Créer le dossier /var/www/html/olympic-games-starter
      │
      ▼
Copier les fichiers Angular
      │
      ▼
Copier la config Nginx → notify
      │
      ▼
Activer la config Nginx → notify
      │
      ▼
[Handler] Redémarrer Nginx
      │
      ▼
App accessible sur http://IP







Résumé : Une fois que Terraform a déployé ton infrastructure, tu as ton serveur prêt avec ta clé publique. Tu t’assures que ta clé privée correspondante est prête à être utilisée en SSH. Et ensuite, Ansible se connectera via SSH à ces serveurs pour exécuter tes tâches.


# Question 1 : Quel est l'intérêt d'Ansbile pour le déploiement continu

C’est d’automatiser les tâches répétitives sur tes serveurs, de façon fiable et cohérente. Dans une stratégie de déploiement continu, ça te permet d’assurer que chaque déploiement se fait de la même façon, sans intervention manuelle.

on parle de tâches répétitives, c’est par exemple installer des logiciels, configurer des services, copier des fichiers, ou encore redémarrer des services. Plutôt que de le faire à la main sur chaque machine, Ansible s’en occupe en une seule commande.


Le CI/CD, c’est le pipeline qui automatise le test, l’intégration, puis le déploiement de ton code. Ansible intervient souvent dans la partie déploiement, en automatisant la configuration et la mise à jour des serveurs. Donc c’est complémentaire
Quand tu pousses ton code sur GitHub, un pipeline CI/CD peut se déclencher. Il va tester ton code, s’assurer qu’il est bon, puis utiliser des outils comme Ansible pour déployer automatiquement sur tes serveurs. Ainsi, du code jusqu’à l’appli en production, tout est automatisé


Résumé = CI, ça veut dire intégration continue, c’est-à-dire tester et intégrer ton code en permanence. CD, c’est déploiement continu, donc une fois que le code est validé, il est automatiquement mis en production. En gros, CI/CD, c’est une chaîne automatisée pour tester et déployer ton code sans intervention manuelle.



# Question 2 : Pourquoi l'automatisation des tâches d'installation et de config est importante pour la normalisation des infrastructures ? 


c’est crucial pour la normalisation parce qu’elle garantit que chaque serveur est configuré exactement de la même façon, sans variation humaine. Ça évite les erreurs et les écarts d’un serveur à l’autre. Tout est cohérent, prévisible et maintenable, ce qui simplifie la gestion et assure une qualité uniforme de ton infrastructure.
