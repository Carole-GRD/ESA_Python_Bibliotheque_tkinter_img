"""
    Module fichier : gère les différents fichiers de données (bibliotheque.py et emprunt.py)
"""
import csv
import json
import os


def lire_bibliotheque(fichier_bibliotheque):
    """
    :param fichier_bibliotheque: (str) le chemin vers le fichier bibliotheque.json
    :return: (dict) les données (les livres de la bibliothèque) lues à partir du fichier
    """
    try:
        with open(fichier_bibliotheque, "r", encoding="UTF-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print('Fichier non trouvé !')
        return {}


def sauvegarder_bibliotheque(bibliotheque, fichier_bibliotheque):
    """
    :param bibliotheque: (dict) un dictionnaire contenant la bibliotheque (les livres sont formes de dictionnaires)
    :param fichier_bibliotheque: (str) le chemin vers le fichier bibliotheque.json
    :return: rien, permet de sauvegarder les données
    """
    try:
        with open(fichier_bibliotheque, "w", encoding="UTF-8") as file:
            json.dump(bibliotheque, file, default=str, indent=4, ensure_ascii=False)
    except FileNotFoundError:
        print('Fichier non trouvé !')


def lire_emprunts(fichier_emprunt):
    """
    :param fichier_emprunt: (str) Chemin vers le fichier emprunt.csv
    :return: (list) Liste de dictionnaires contenant les informations concernant les emprunteurs
    """
    # Créer le fichier s'il n'existe pas
    if not os.path.isfile(fichier_emprunt):
        with open(fichier_emprunt, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file,
                                    fieldnames=[
                                        "nom",
                                        "prenom",
                                        "nbr_livres_empruntes",
                                        "photo_id",
                                        "emprunt_id",
                                        "titre",
                                        "date_emprunt",
                                        "date_retour"
                                    ], delimiter=";")
            writer.writeheader()

    personnes = []
    current_person = None
    try:
        with open(fichier_emprunt, "r", encoding="utf-8", newline="") as file:
            reader: csv.DictReader = csv.DictReader(file, delimiter=";")
            for row in reader:
                nom = row["nom"]
                prenom = row["prenom"]
                # Nouvelle personne si nom et prénom sont présents
                if nom and prenom:
                    current_person = {
                        "nom": nom,
                        "prenom": prenom,
                        "nbr_livres_empruntes": int(row["nbr_livres_empruntes"]),
                        "photo_id": row.get("photo_id", ""),
                        "emprunts": {}
                    }
                    personnes.append(current_person)
                # Ajouter l'emprunt à la personne actuelle
                if current_person:
                    emprunt_id = row["emprunt_id"]
                    current_person["emprunts"][emprunt_id] = {
                        "titre": row["titre"],
                        "date_emprunt": row["date_emprunt"],
                        "date_retour": row["date_retour"]
                    }
    except csv.Error as e:
        print(f"Erreur lors de la lecture du fichier CSV : {e}")

    return personnes


def sauvegarder_emprunts(emprunts, fichier_emprunt):
    """
    Écrit les emprunts dans le fichier emprunt.csv avec une ligne principale par personne
    et des lignes secondaires pour les emprunts.

    :param emprunts: (list) Liste de dictionnaires contenant les emprunts
    :param fichier_emprunt: (str) Chemin vers le fichier emprunt.csv
    :return: None
    """
    with open(fichier_emprunt, "w", encoding="utf-8", newline="") as file:
        fieldnames = ["nom", "prenom", "nbr_livres_empruntes", "photo_id", "emprunt_id", "titre", "date_emprunt",
                      "date_retour"]
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()

        for personne in emprunts:
            emprunts_dict = personne["emprunts"]
            # Calculer nbr_livres_empruntes (nombre d'emprunts sans date_retour)
            nbr_livres = sum(1 for emprunt in emprunts_dict.values() if not emprunt["date_retour"])
            for i, (num, emprunt) in enumerate(emprunts_dict.items(), 1):
                row = {
                    "emprunt_id": num,
                    "titre": emprunt["titre"],
                    "date_emprunt": emprunt["date_emprunt"],
                    "date_retour": emprunt["date_retour"]
                }
                if i == 1:
                    # Ligne principale
                    row.update({
                        "nom": personne["nom"],
                        "prenom": personne["prenom"],
                        "nbr_livres_empruntes": nbr_livres,
                        "photo_id": personne.get("photo_id", "")
                    })
                else:
                    # Ligne secondaire
                    row.update({
                        "nom": "",
                        "prenom": "",
                        "nbr_livres_empruntes": "",
                        "photo_id": ""
                    })
                writer.writerow(row)
