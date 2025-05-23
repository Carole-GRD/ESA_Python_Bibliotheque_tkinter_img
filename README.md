# ESA_Python_Bibliotheque

## Projet

Gestion d’une Bibliothèque Numérique

## Objectif

Développer un programme en Python permettant de gérer une bibliothèque
numérique à l’aide de dictionnaires et de sous-routines. Par manque de moyen, la
bibliothèque n’utilise pas de base de données mais un fichier JSON pour stocker les
informations concernant les livres et un fichier CSV concernant les personnes qui
empruntent les livres.

## Consignes générales

- Vous devrez implémenter un programme permettant d’ajouter, de supprimer et de rechercher des livres dans une bibliothèque numérique.


- Les livres seront stockés sous forme de dictionnaires avec les informations
suivantes :

        • Titre
        • Auteur
        • Année de publication
        • Genre
        • Nombre d’exemplaires disponibles

- Le programme devra proposer un menu interactif pour que l’utilisateur puisse :

        • Ajouter un nouveau livre
        • Supprimer un livre
        • Rechercher un livre (par titre, auteur ou genre)
        • Afficher tous les livres disponibles
        • Emprunter un livre (mettre à jour le nombre d’exemplaires et le fichier csv)
        • Rendre un livre (mettre à jour le nombre d’exemplaires et le fichier csv)
        • Quitter le programme

- De plus, il faudra pouvoir garder dans un fichier CSV la liste des personnes qui ont
emprunté un livre. Cette liste devra contenir les informations suivantes :

        • Prénom
        • Nom
        • Nombre de livres empruntés (avec un maximum de 3)
        • Titre·s du/des livre·s emprunté·s
        • Date d’emprunt
        • Date de retour


Attention, le fichier JSON devra être mis à jour à chaque modification (pas en quittant
le programme).


## Aspects techniques demandés :

1. Utilisation de dictionnaires :

        • Chaque livre est représenté par un dictionnaire.
        • La bibliothèque est une collection de livres stockée dans un dictionnaire.

2. Création de sous-routines (fonctions) pour la gestion des livres :

       • Une fonction pour ajouter un livre.
       • Une fonction pour supprimer un livre.
       • Une fonction pour rechercher un livre.
       • Une fonction pour afficher tous les livres.
       • Une fonction pour gérer l’emprunt et le retour des livres.
       • Une fonction pour afficher le menu et gérer les interactions.

3. Création de sous-routines (fonctions) pour la gestion du fichier csv :

        • Ajout nouvel emprunteur
        • Mise à jour d'un emprunteur
        • Sauvegarde dans le fichier csv


### Bonus qui dépasse largement le cadre du cours (pour les plus avancés qui s’ennuieraient) :

        • Interface graphique simple avec tkinter.
        • Ajout de la photo (image) de l’emprunteur


## Aides :

    • Vous devrez utiliser la librairie JSON (import json)
    • Séparez votre code comme on a vu au cours et, dans le package que vous créerez, vous devrez créer 3 fichiers :
            ◦ 1 pour gérer les livres
            ◦ 1 pour gérer les emprunteurs
            ◦ 1 pour la gestion des fichiers
    • Le programme principal ne contiendra que le menu, ni plus, ni moins, donc la
    collection devra se retrouver…

