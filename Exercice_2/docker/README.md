Exercice 2 - Option "locale"
Démarrer
Avec un terminal, se positionner dans le répertoire Exercice_2/docker

Exécuter la commande suivante:

 docker compose up
Une fois le déploiement terminé, les ressources suivantes devraient être disponibles:

http://localhost:5601/ - Interface Kibana
http://localhost:9200/ - Serveur ElasticSearch
http://localhost:8000/ - Application Web (extraite du P2)
Nettoyer son environnement après l'exercice
docker compose down --remove-orphans -v
