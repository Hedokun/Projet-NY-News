# Projet-NY-News

## Introduction
Le projet "Projet-NY-News" a été réalisé dans le cadre de la formation Data Engineer de Datascientest par Alexis Peron, Edouard Loiseau et Louis Petat Lenoir. L'objectif de ce projet était d'utiliser les API du journal américain NY Times pour créer notre propre API et apporter une valeur ajoutée aux données disponibles.

Ce projet s'articule autour de pluiseurs étapes pour lesquelles un livrable devra être rendu. Ces étapes sont :
        * Découverte des sources de données disponible
        * Organisation des données
        * Consommation des données
        * Déploiement
        * Automatisation des flux

## Problématique
Après avoir exploré les différentes API, nous devons donc répondre à une problématique à l'aide des données récoltées

Notre volonté était d'apporter une valeur ajoutée aux différentes API, de réaliser une application qui permettrait de valoriser ces données. Grâce aux informations communes aux livres et aux articles que nous avons relevés précédement, 
**nous estimerons la popularité d'un sujet sur le New York Times**

## Architecture :
Pour répondre à cette problématique, nous avons décidé de développer un DashBoard afin de synthétiser au moins l'information récoltée. Ce dernier affichera par exemple le nombre d'occurrences d'un mot sur une période donnée, les derniers articles publiées ou encore les catégories les plus citées.

Nous avons donc construit notre application de cette manière:

![Screenshot de l'application](./main/archi_glob2.png?raw=true)

Elle se décompose en deux parties principales.
Il y a la partie front_end dans le dossier front_dash. Ce dossier contient le script python renvoyant le tableau de bord à l'utilisateur, ce tableau de bord est réalisé avec l'outil Dash. 
Il y a la partie Back_end dans le dossier src. Il contient le coeur de l'application c'est à dire l'appel de l'API du New York Times, la création de la Base de données et la valorisation de ces données. Vous retrouverez aussi les notebooks qui nous ont permis de découvrir et explorer les API.

Les requêtes automatisées de L'API du New York Times sont dans le dossier request_NYT. Pour valoriser nos données, nous créerons une base de données NoSQL sur elasticsearch qui offre un système de requêtes performant sur des données textuelles. La connexion à cette base et les différentes requêtes permettant d'alimenter le Dashboard sont dans e dossier elastic. Enfin, le fichier test_App contient les tests de notre application.


## Installation et Exécution :
Pour installer et exécuter l'application, vous pouvez suivre les étapes suivantes :

Clonez ce dépôt GitHub sur votre machine locale.
Assurez-vous d'avoir les dépendances nécessaires installées. Vous pouvez les installer en exécutant la commande pip install -r requirements.txt.
Configurez les paramètres nécessaires, tels que les clés d'API du New York Times, dans les fichiers appropriés.
Exécutez le script principal pour lancer l'application Dash.

## Conclusion :
Grâce à ce projet, nous avons pu explorer les API du New York Times et créer notre propre API pour valoriser les données disponibles. Le Dashboard que nous avons développé permet de visualiser et d'analyser les informations extraites des articles du New York Times, offrant ainsi une meilleure compréhension de la popularité des sujets abordés. Ce projet nous a permis d'acquérir des compétences en collecte et en analyse de données, ainsi qu'en création d'applications utilisant des outils tels que Dash et Elasticsearch.
