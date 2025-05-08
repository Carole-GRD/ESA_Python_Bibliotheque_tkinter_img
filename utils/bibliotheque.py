"""
    Module bibliotheque : gestion des livres

    Fonctions :
        • ajouter_livre
        • supprimer_livre
        • chercher_livre (par titre, auteur ou genre)
        • afficher_livres
        • emprunter_livre (mettre à jour le nombre d’exemplaires et le fichier csv)
        • rendre_livre (mettre à jour le nombre d’exemplaires et le fichier csv)
        • afficher_menu (+ gestion des interactions)
"""
from datetime import date
from datetime import timedelta

from utils.emprunt import ajouter_personne
from utils.emprunt import creer_emprunt
from utils.emprunt import creer_retour
from utils.emprunt import selectionner_retour
from utils.emprunt import retours_possibles
from utils.emprunt import verifier_emprunts_en_cours

from utils.gestion_fichiers import sauvegarder_bibliotheque
from utils.gestion_fichiers import sauvegarder_emprunts


def ajouter_livre(livres, fichier_bibliotheque):
    """
    :param livres: (dict) un dictionnaire contenant tous les livres disponibles
    :param fichier_bibliotheque:  (str) le chemin vers le fichier bibliotheque.json
    :return: ne retourne rien, ajoute un livre au dictionnaire "livres"
    """
    titre = input("\nTitre : ").strip()
    auteur = input("Auteur : ").strip()

    while True:
        try:
            annee = int(input("Année : "))
            if annee < 0 or annee > date.today().year:
                print("Année invalide !")
                continue
            break
        except ValueError:
            print("L'année doit être un nombre !")

    genre = input("Genre : ").strip()

    while True:
        try:
            exemplaires = int(input("Nombre d'exemplaire : "))
            if exemplaires < 0:
                print("Le nombre d'exemplaires ne peut pas être négatif !")
                continue
            break
        except ValueError:
            print("Le nombre d'exemplaires doit être un nombre !")

    livres[titre] = {
        "Auteur": auteur,
        "Année": annee,
        "Genre": genre,
        "Exemplaires": exemplaires
    }

    sauvegarder_bibliotheque(livres, fichier_bibliotheque)
    print(f'Le livre : "{titre}" a été ajouté à la bibilothèque !')


def supprimer_livre(livres, fichier_bibliotheque):
    """
    :param livres: (dict) un dictionnaire contenant tous les livres disponibles
    :param fichier_bibliotheque: (str) le chemin vers le fichier bibliotheque.json
    :return: ne retourne rien, supprime un livre du dictionnaire "livres"
    """
    livre_a_supprimer = input("\nTitre du livre à supprimer : ").lower()
    titre_a_supprimer = ''
    for titre in livres:
        if titre.lower() == livre_a_supprimer:
            titre_a_supprimer = titre
            livres.pop(titre, None)
            break

    sauvegarder_bibliotheque(livres, fichier_bibliotheque)
    print(f'Le livre : "{titre_a_supprimer}" a été supprimé de la bibilothèque !')


def filtrer_livres(livres, filtre):
    """
    L'utilisateur est invité à entrer soit le titre, l'auteur ou le genre du livre qu'il recherche
    en fonction du filtre qu'il a choisi.

    :param livres: (dict) un dictionnaire contenant tous les livres disponibles
    :param filtre: (str) le filtre qui sert à rechercher des livres (Titre, Auteur, Genre)
    :return: ne retourne rien, sert à filtrer les livres
    """
    valeur_cherche = input(f"\n{filtre} recherché : ").lower()

    livres_cherches = {}

    if filtre == 'Titre':
        for titre, infos in livres.items():
            if valeur_cherche in titre.lower():
                livres_cherches[titre] = infos
    else:
        for titre, infos in livres.items():
            if valeur_cherche in infos[filtre].lower():
                livres_cherches[titre] = infos

    if livres_cherches:
        afficher_livres(livres_cherches)
    else:
        print(f"\n{filtre} non trouvé !")


def rechercher_livre(livres):
    """
    :param livres: (dict) un dictionnaire contenant les livres disponibles
    :return: ne retourne rien, cette fonction sert à afficher les livres recherchés
    """
    while True:
        filtre = input("\nChercher par : titre - auteur - genre : ").capitalize()
        if filtre in ['Titre', 'Auteur', 'Genre']:
            filtrer_livres(livres, filtre)
            break
        print('\n❌ ERREUR : La recherche se fait par "titre", "auteur" ou "genre" !')


def afficher_livres(livres):
    """
    :param livres: (dict) un dictionnaire contenant les livres disponibles
    :return: ne retourne rien, cette fonction sert à afficher les livres
    """
    print("\nTitre, Auteur, Date de publication, exemplaires")
    print("------------------------------------------------")
    for titre, infos in livres.items():
        livre = ''
        livre += titre
        for key, value in infos.items():
            livre += ", " + str(value)
        print(livre)


def emprunter_livre(livres, fichier_bibliotheque, personnes, fichier_emprunt):
    """
    Enregistre un nouvel emprunt et met à jour le nombre d'exemplaires des livres empruntés.

    :param livres: (dict) un dictionnaire contenant les livres disponibles
    :param fichier_bibliotheque: (str) le chemin vers le fichier bibliotheque.json
    :param personnes: (list) Liste des dictionnaires contenant les emprunts enregistrés
    :param fichier_emprunt: (str) le chemin vers le fichier emprunt.csv
    :return: rien, enregistre un nouvel emprunt et met à jour le nombre d'exemplaires des livres empruntés
    """
    # afficher_livres(livres)

    # Créer ou trouver la personne
    est_deja_enregistree, personne = ajouter_personne(personnes)

    # Vérifier les emprunts en cours
    if verifier_emprunts_en_cours(personne) == 3:
        print("Impossible d'emprunter : limite de 3 livres atteinte.")
        return

    # Création du nouvel emprunt avec décrémentation des nouveaux livres empruntés
    personne = creer_emprunt(personne, livres)

    # Ajouter le nouvel emprunt à la liste des emprunts et ensuite sauvegrader les emprunts
    if not est_deja_enregistree:
        personnes.append(personne)
    sauvegarder_emprunts(personnes, fichier_emprunt)

    # Sauvegarder les livres avec le nombre d'exemplaires des livres empruntés mis à jour
    sauvegarder_bibliotheque(livres, fichier_bibliotheque)

    # Afficher la date de retour théorique
    date_retour_theorique = date.today() + timedelta(days=14)
    print(f"\nEmprunt gratuit jusqu'au {date_retour_theorique.strftime('%d/%m/%Y')} (14 jours)."
          f"\nAu-delà de cette date, vous devrez payer 0.10€ par jour supplémentaire."
          f"\nBonne lecture !")


def rendre_livre(livres, fichier_bibliotheque, personnes, fichier_emprunt):
    """
    :param livres: (dict) un dictionnaire contenant les livres disponibles
    :param fichier_bibliotheque: (str) le chemin vers le fichier bibliotheque.json
    :param personnes: (list) Liste des dictionnaires contenant les emprunts enregistrés
    :param fichier_emprunt: (str) le chemin vers le fichier emprunt.csv
    :return: rien, enregistre les emprunts et livres mis à jour après retour
    """
    # Récupérer les éventuels emprunts en cours
    retours_eventuels, personne = retours_possibles(personnes)
    if not retours_eventuels:
        return

    # Sélectionner les emprunts qui correspondent aux livres que la personne souhaite rendre
    retours_selectionnes = selectionner_retour(retours_eventuels)
    if not retours_selectionnes:
        return

    # Création du retour avec incrémentation des livres rendus et ajout de la date de retour
    creer_retour(retours_selectionnes, personnes, personne, livres)

    # Enregistrer les emprunts mis à jour suite aux retours
    sauvegarder_emprunts(personnes, fichier_emprunt)

    # Sauvegarder les livres avec le nombre d'exemplaires des livres rendus mis à jour
    sauvegarder_bibliotheque(livres, fichier_bibliotheque)

    print(f"\n------------------------------------------------------"
          f"\nNous espérons que vous avez appréciez la lecture !")


def menu():
    """
    :return: -1 si le choix est problématique sinon le choix de l'utilisateur
    """
    try:
        while True:
            choix = int(input(f"\n\n  -------- 📜 MENU 📜 ---------\n\n"
                              f"1: Ajouter un livre\n"
                              f"2: Supprimer un livre\n"
                              f"3: Rechercher un livre\n"
                              f"4: Afficher les livres\n"
                              f"5: Emprunter des livres\n"
                              f"6: Rendre des livres\n"
                              f"7: Quitter le programme\n"
                              f"\n       Votre choix : "))
            if 1 <= choix <= 7:
                return choix
            print("\n❌ ERREUR : Entrer un nombre entre 1 et 7 !")
    except ValueError as ve:
        print(f"\n❌ ERREUR : Entrer un nombre ! \n➡️ MESSAGE : {ve}")
        return -1
