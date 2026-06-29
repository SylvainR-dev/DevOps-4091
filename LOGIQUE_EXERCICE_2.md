# 1/ Export des clés : 

cd ~/Bureau/DevOps-4091/Exercice_2/aws
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
terraform init
terraform apply


# 2 Résolution du problème d'accès Kibana

Modifié le main.tf plusieurs fois pour ajouter une access_policies. Puis j'ai configuré le fine-grained access control directement depuis la console AWS (interface graphique) avec :

Utilisateur : 
Password : 


# 3. Import des logs
Téléchargement du fichier de logs 

curl -O https://raw.githubusercontent.com/.../nginx-access.log


* Création du script Python import_logs.py qui :

Parsait chaque ligne du fichier avec une regex
Envoyait tous les logs en une seule requête via l'API Bulk Elasticsearch
Créait l'index nginx-access avec le bon mapping de dates


* Les logs sont stockés dans : 
~/Bureau/DevOps-4091/Exercice_2/nginx-access.log



Exécution :
python3 import_logs.py

Résultat : 14 490 documents importés.

* lit ce fichier et envoie les données vers Elasticsearch
* Elasticsearch se trouve sur le cloud AWS , c'est le domaine OpenSearch qu'on a déployé avec Terraform



# 4. Kibana

Accès = https://search-openclassrooms-p5-edo-xxx.us-east-1.es.amazonaws.com/_dashboards
Puis Id +MDP


Dans l'interface Kibana :

Création de l'index pattern nginx-access
Création d'un dashboard avec 3 visualisations



- Kibana ne touche jamais à ton fichier local nginx-access.log
- Kibana lit uniquement les données déjà stockées dans Elasticsearch
- C'est le script Python qui a fait le pont entre ton fichier local et Elasticsearch
- Une fois l'import terminé, tu pouvais même supprimer nginx-access.log de ta machine = Kibana aurait continué à fonctionner car les données étaient dans Elasticsearch sur AWS