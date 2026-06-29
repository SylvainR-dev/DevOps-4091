# terraform init crée : 

* .terraform/ — dossier qui contient les plugins/providers téléchargés (AWS, TLS, local). C'est l'équivalent d'un node_modules en JavaScript. 
* .terraform.lock.hcl — fichier qui verrouille les versions exactes des providers utilisés, pour que tout le monde sur le projet ait les mêmes versions

# Terraform plan 
* Ca montre ce qui va être créé ou modifié. Ca évite les surprises. Et si j’utilise des variables, plan me montre aussi l’impact des valeurs avant de toucher à AWS. 

# terraform apply crée :
* terraform.tfstate — le fichier le plus important ! Il contient l'état actuel de ton infrastructure (IPs, IDs des ressources AWS, etc.). Terraform s'en sert pour savoir ce qui existe déjà sur AWS
* terraform.tfstate.backup — sauvegarde de l'état précédent

# terraform show
Affiche tout l'état de l'infrastructure : l'IP publique, l'IP privée, l'ID de l'instance, le security group, la clé SSH, etc. C'est pratique quand les outputs ne sont pas définis dans le main.tf ou pour avoir le détail complet.




C'est pour ça que le .gitignore du projet contient .terraform* — pour ne pas commiter le dossier .terraform/ ni le terraform.tfstate qui peut contenir des informations sensibles comme des clés privées.



# main.tf 
* décrit l'infrastructure souhaitée (instances, réseau, sécurité). Terraform lit ce fichier et crée les ressources correspondantes sur AWS.

Il contient 4 blocs principaux : 
* 1. Le provider — dit à Terraform d'utiliser AWS en région us-east-1
* 2. La ressource EC2 — crée l'instance Ubuntu
* 3. Le security group — ouvre les ports 22 (SSH) et 80 (HTTP)
* 4. La clé SSH — générée automatiquement et sauvegardée dans ~/.ssh/

* Bloc 1 — Configuration Terraform
C'est le bloc qui dit à Terraform : "j'ai besoin du provider AWS version 4.16 ou supérieure, et Terraform lui-même doit être en version 1.2.0 minimum". C'est ce que terraform init va télécharger.

C'est pour demander à AWS de me fournir des ressources : des serveurs, des bases de données, des réseaux, et tout ce dont mon infrastructure a besoin

* Bloc 2 — Provider AWS — dit à Terraform d'utiliser AWS en région us-east-1
un provider AWS, c’est un peu comme un traducteur entre ton code et le cloud d’AWS


* Bloc 3 — L'instance EC2
Dedans il y a : 
   - L’AMI, c’est l’image de machine, en gros, le modèle préconstruit du système (comme un OS avec des configurations), et l’instance type, c’est le gabarit (la taille) de la machine (par exemple, combien de CPU et de mémoire). Donc, ces deux paramètres disent à AWS quelle image utiliser et quelle taille de serveur lancer.
   - l’instance type (la taille du serveur) selon tes besoins.
   - tags = ils servent à identifier tes machines, faciliter le tri ou la gestion dans AWS.
   - le vpc_security_group_ids, c’est une manière d’indiquer à quelle règle de sécurité ton serveur doit se conformer.
   - key_name, c’est la clé SSH qui te permettra de te connecter à ton serveur.

* Bloc 4 — Le Security Group
   - INGRESS = ce qui autorise le trafic entrant vers tes serveurs. définis les ports, les protocoles, et les adresses IP qui sont autorisés à entrer.
      c’est une façon de définir quelles portes sont ouvertes et pour qui.
   - EGRESS =  c’est l’inverse : ça définit ce qui peut sortir de tes serveurs.
   - Dans l'exercice 1 = Port 22 entrant → connexion SSH (Ansible). Port 80 entrant → accès HTTP (l'app Angular)

* Bloc 5 — La variable
La variable sert à stocker une clé SSH, utilisée pour se connecter au serveur. Au lieu de répéter cette clé partout dans ton code, tu la définis à un seul endroit. Si tu dois la changer, tu modifies simplement la variable, et tout s’ajuste automatiquement. Ça rend ton projet plus flexible et plus facile à maintenir.

* Bloc 6 — Génération de la clé SSH
Ce bloc ressource, il te permet de créer automatiquement une clé SSH. L’algorithme, c’est le type de chiffrement utilisé, ici RSA, et rsa_bits, c’est la taille de la clé (sa complexité). En clair, ça te génère une clé sécurisée, prête à être utilisée pour te connecter à tes serveurs.

* Bloc 7 — Envoi de la clé publique sur AWS
   - ce bloc permet de enregistrer ta clé SSH sur AWS. Le key_name, c’est le nom que tu donnes à cette clé dans AWS (ce sera ta référence). La public_key, c’est la clé publique que tu viens de générer, celle que tu donnes à AWS pour qu’il la connaisse et te laisse te connecter. En gros, tu associes ta clé à ton compte AWS.
   - Dans ton fichier Terraform, tu peux demander à Terraform de la générer lui-même (comme avec la ressource de clé SSH), ou sinon, tu peux la créer sur ton terminal avec une commande SSH classique.
   - La commande classique, c’est souvent quelque chose comme « ssh-keygen », tout simplement. Tu la lances, elle te demande où enregistrer la clé, et elle te génère une paire de clés : une privée (à garder secrète) et une publique (que tu pourras fournir à AWS).

* Bloc 8 — Sauvegarde de la clé privée
Ce bloc te permet d’enregistrer quelque chose sur ta machine locale. Le filename, c’est le nom du fichier que tu vas créer. Les permissions, c’est qui a le droit de lire ou écrire. Et le contents, c’est ce que tu mets dans ce fichier. Par exemple, si tu veux sauvegarder une clé privée de manière sécurisée, tu peux le faire avec ce bloc.


* En résumé main.tf fait = 
Crée l'instance EC2
Configure le pare-feu
Génère une paire de clés SSH
Envoie la clé publique sur AWS
Sauvegarde la clé privée sur ta machine



# ORDRE LOGIQUE  
* Écrire le main.tf — Décire ce que je veux créer
* terraform init — Terraform lit le main.tf, voit quels providers sont nécessaires (AWS, TLS, etc.) et les télécharge
* terraform plan — prévisualise ce qui va être créé
* terraform apply — crée réellement les ressources sur AWS
* terraform show — vérifie ce qui a été créé



# LE FLUX

main.tf
   │
   │ (décrit l'infrastructure souhaitée) = Configuration Terraform, Provider AWS, L'instance EC2, Le Security Group,  La variable,  Génération de la clé SSH,     Envoi de la clé publique sur AWS, Sauvegarde de la clé privée
   ▼
terraform init
   │
   │ (télécharge les providers → crée .terraform/ et .terraform.lock.hcl)
   ▼
terraform plan
   │
   │ (prévisualise les changements, ne crée rien)
   ▼
terraform apply
   │
   │ (crée les ressources sur AWS → crée terraform.tfstate et terraform.tfstate.backup)
   ▼
terraform show
   │
   │ (affiche l'état de l'infrastructure depuis le terraform.tfstate)
   ▼
[Infrastructure active sur AWS]
   │
   │ (quand on a fini)
   ▼
terraform destroy
   │
   │ (supprime toutes les ressources sur AWS)
   ▼
[Infrastructure supprimée]


