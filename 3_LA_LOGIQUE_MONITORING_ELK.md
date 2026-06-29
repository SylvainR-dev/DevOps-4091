
# Le flux simplifié : 

Serveurs (logs bruts)
      │
      ▼
Filebeat (collecte)
      │
      ▼
Logstash (transformation)
      │
      ▼
Elasticsearch (stockage)
      │
      ▼
Kibana (visualisation)




1. Collecter les logs

Un agent comme Filebeat tourne sur chaque serveur
Il lit les fichiers de logs en temps réel (Nginx, Apache, app, etc.)
Il les envoie vers Logstash



2. Transformer les logs (Logstash)

Logstash reçoit les logs bruts
Il les parse et les structure (extrait l'IP, la date, le verbe HTTP, etc.)
Il les envoie vers Elasticsearch

3. Stocker et indexer (Elasticsearch)

Elasticsearch reçoit les données structurées
Il les indexe pour les rendre recherchables rapidement
C'est lui qui stocke tout

4. Visualiser (Kibana)

Kibana se connecte à Elasticsearch
Tu crées des dashboards, des graphiques, des alertes
Tu explores tes données en temps réel







# Le flux détaillé : 

main.tf
   │
   │ (décrit l'infrastructure souhaitée)
   ▼
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
   │
   │ (authentification auprès d'AWS)
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




# Les composants de la stack ELK

La stack ELK est composée de 3 outils qui travaillent ensemble :

* E — Elasticsearch

C'est le moteur de stockage et de recherche. Il reçoit les données structurées, les indexe et les rend recherchables très rapidement. Dans notre projet, c'était le domaine AWS OpenSearch qui jouait ce rôle. C'est lui qui stockait les 14 490 logs Nginx.

* L — Logstash

C'est le pipeline de transformation. Il reçoit les logs bruts, les parse et les structure avant de les envoyer à Elasticsearch. Dans notre projet on l'a remplacé par un script Python qui faisait le même travail — parser les lignes du fichier nginx-access.log et les envoyer à Elasticsearch via l'API Bulk.

* K — Kibana

C'est l'interface de visualisation. Il se connecte à Elasticsearch pour lire les données et permet de créer des dashboards, graphiques et alertes. Dans notre projet on y a créé 3 visualisations (donut, histogramme, histogramme cumulé).