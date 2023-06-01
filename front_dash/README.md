# Projet-NY-News - Front-Dash
Ce projet a été réalisé par Alexis Peron, Edouard Loiseau et Louis Petat Lenoir dans le cadre de la formation Data Engineer de Datascientest.

L’objectif de ce projet est d'utiliser le portail développeur du journal américain NY Times, qui propose plusieurs API à explorer, pour créer sa propre API.

Ce repository contient le code du frontend de l'application, qui consiste en un tableau de bord interactif développé avec l'outil Dash. Le tableau de bord affiche des informations synthétiques basées sur les données collectées à partir des API du NY Times.

## Architecture
Le frontend de l'application est organisé dans le dossier front_dash. Il contient le script Python dashboard.py qui génère le tableau de bord en utilisant l'outil Dash.

Le tableau de bord est composé de plusieurs éléments :

-Une barre de navigation en haut de la page avec le titre de l'application.
-Différents onglets permettant de visualiser les graphiques et les tableaux de données.
-Des sélecteurs pour filtrer les données, tels que la recherche par mot-clé, la sélection de catégorie et la plage de dates.
-Des graphiques interactifs qui affichent les données en fonction des sélections de l'utilisateur.
-Des tableaux de données qui affichent les titres et les liens des derniers articles enregistrés.


## Comment exécuter l'application
Pour exécuter le frontend de l'application, suivez les étapes suivantes :

Assurez-vous d'avoir Python 3 et pip installés sur votre machine.
Clonez ce repository sur votre machine.
Accédez au dossier front_dash.
Installez les dépendances en exécutant la commande suivante :
```
pip install -r requirements.txt
```
Lancez l'application en exécutant la commande suivante :
```
python dashboard.py
```

Ouvrez un navigateur web et accédez à l'adresse http://localhost:5000 pour visualiser le tableau de bord.
Note : Assurez-vous que le backend de l'application est également en cours d'exécution pour que le frontend puisse récupérer les données correctement.

Ce projet a été réalisé dans le cadre de la formation Data Engineer de Datascientest. L'objectif était de mettre en pratique nos compétences en collecte de données, en traitement des données, en développement d'API et en création de tableaux de bord interactifs.
Nous avons utilisé les API du NY Times pour collecter les données et Dash pour créer le tableau de bord. 
Nous espérons que ce projet démontre notre capacité à explorer et à exploiter des sources de données externes, ainsi qu'à développer des applications de visualisation des données.

