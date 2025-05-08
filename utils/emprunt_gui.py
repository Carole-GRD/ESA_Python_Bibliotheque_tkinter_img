"""
    Module emprunts : gestion des emprunteurs

    Fonctions :
        • clear_result
        • afficher_photo
        • trouver_ou_creer_personne
        • copier_photo_emprunteur
        • emprunter_livre
        • rendre_livre
"""
import os
import shutil
from datetime import date, timedelta, datetime

import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.font as tkfont
from PIL import Image, ImageTk

from utils.custom_messagebox import custom_messagebox
from utils.custom_form_window import custom_form_window
from utils.gestion_fichiers import sauvegarder_bibliotheque
from utils.gestion_fichiers import sauvegarder_emprunts


def clear_result(result_text):
    """
    :param result_text: Widget de texte à vider
    :return: Aucun
    """
    result_text.delete(1.0, tk.END)


def afficher_photo(select_window, photo_id):
    """
    :param select_window: Fenêtre Toplevel pour afficher la photo
    :param photo_id: Chaîne représentant le nom du fichier photo ou vide si aucune photo
    :return: Aucun
    """
    photo_label = ttk.Label(select_window)
    photo_label.grid(row=1, column=0, columnspan=2, padx=30, pady=5)
    photo_image = None  # Référence nécessaire pour éviter la collecte par le garbage collector
    if photo_id:
        photo_path = os.path.join("data/photos", photo_id)
        if os.path.exists(photo_path):
            img = Image.open(photo_path)
            img = img.resize((180, 180), Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(img)
            photo_label.config(image=photo_image)
            photo_label.image = photo_image  # Garder la référence
        else:
            photo_label.config(text="Photo non trouvée")
    else:
        photo_label.config(text="Aucune photo")


def trouver_ou_creer_personne(personnes, nom, prenom):
    """
    :param personnes: Liste de dictionnaires contenant les données des personnes
    :param nom: Chaîne représentant le nom de famille de la personne
    :param prenom: Chaîne représentant le prénom de la personne
    :return: Dictionnaire représentant la personne
    """
    for p in personnes:
        if nom == p['nom'] and prenom == p['prenom']:
            return p
    personne = {
        "nom": nom,
        "prenom": prenom,
        "nbr_livres_empruntes": 0,
        "emprunts": {},
        "photo_id": ""
    }
    personnes.append(personne)
    return personne


def copier_photo_emprunteur(nom, prenom, chemin_image):
    """
    :param nom: Chaîne représentant le nom de famille de la personne
    :param prenom: Chaîne représentant le prénom de la personne
    :param chemin_image: Chaîne représentant le chemin vers le fichier image
    :return: Chaîne représentant le nouveau nom de fichier photo ou chaîne vide si aucune image
    """
    if not chemin_image:
        return ""
    photos_dir = "data/photos"
    if not os.path.exists(photos_dir):
        os.makedirs(photos_dir)
    extension = os.path.splitext(chemin_image)[1]
    nom_fichier = f"{nom.lower()}_{prenom.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}"
    chemin_destination = os.path.join(photos_dir, nom_fichier)
    shutil.copy(chemin_image, chemin_destination)
    return nom_fichier


def emprunter_livre(root, result_text, livres, fichier_bibliotheque, personnes, fichier_emprunt):
    """
    :param root: Fenêtre principale de l'application
    :param result_text: Widget de texte pour afficher le résultat
    :param livres: Dictionnaire contenant les données des livres
    :param fichier_bibliotheque: Chaîne représentant le chemin du fichier de la bibliothèque
    :param personnes: Liste de dictionnaires contenant les données des personnes
    :param fichier_emprunt: Chaîne représentant le chemin du fichier des emprunts
    :return: Aucun
    """
    form_window = custom_form_window(root, "Emprunter un livre", "900x500")

    custom_font = tkfont.Font(family="Helvetica", size=16)

    # Champs Nom
    (ttk.Label(form_window, text="Nom : ", font=custom_font, width=15, anchor="e")
        .grid(row=0, column=0, padx=5, pady=5, sticky="e"))
    nom_entry = ttk.Entry(form_window, font=custom_font)
    nom_entry.grid(row=0, column=1, padx=5, pady=5)

    # Champs Prénom
    (ttk.Label(form_window, text="Prénom : ", font=custom_font, width=15, anchor="e")
        .grid(row=1, column=0, padx=5, pady=5, sticky="e"))
    prenom_entry = ttk.Entry(form_window, font=custom_font)
    prenom_entry.grid(row=1, column=1, padx=5, pady=5)

    # Sélection de la photo
    (ttk.Label(form_window, text="Photo : ", font=custom_font, width=15, anchor="e")
        .grid(row=2, column=0, padx=5, pady=5, sticky="e"))
    photo_label = ttk.Label(form_window, text="Aucune image sélectionnée", font=custom_font)
    photo_label.grid(row=2, column=1, padx=5, pady=5, sticky="w")
    photo_path = tk.StringVar()
    photo_image = None  # Référence nécessaire pour éviter la collecte par le garbage collector

    def select_photo():
        """Ouvre une boîte de dialogue pour sélectionner une photo et affiche un aperçu."""
        nonlocal photo_image
        chemin = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if chemin:
            photo_path.set(chemin)
            photo_label.config(text=os.path.basename(chemin))
            # Afficher un aperçu
            img = Image.open(chemin)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(img)
            preview_label.config(image=photo_image)
            preview_label.image = photo_image  # Conserver la référence

    (ttk.Button(form_window, text="Choisir une photo", command=select_photo, style="Custom.TButton")
        .grid(row=2, column=2, padx=5, pady=5))

    # Aperçu de la photo
    preview_label = ttk.Label(form_window)
    preview_label.grid(row=3, column=1, padx=5, pady=5)

    # Titres des livres
    (ttk.Label(form_window, text="Titres des livres : ", font=custom_font, width=15, anchor="e")
        .grid(row=3, column=0, padx=5, pady=5, sticky="e"))
    livres_text = tk.Text(form_window, height=4, width=30, font=custom_font)
    livres_text.grid(row=3, column=1, padx=5, pady=5)

    def submit():
        """Valide les informations saisies pour emprunter un livre et met à jour les données."""
        nom = nom_entry.get().strip()
        prenom = prenom_entry.get().strip()
        livres_input = livres_text.get("1.0", tk.END).strip().splitlines()
        livres_a_emprunter = [title.strip() for title in livres_input if title.strip()]

        if not (nom and prenom):
            custom_messagebox(form_window, "Erreur", "Le nom et le prénom sont obligatoires !")
            return

        if not livres_a_emprunter:
            custom_messagebox(form_window, "Erreur", "Aucun livre sélectionné !")
            return

        personne = trouver_ou_creer_personne(personnes, nom, prenom)

        # Gérer la photo
        chemin_image = photo_path.get()
        if chemin_image and not personne["photo_id"]:  # Ajouter la photo si elle n'existe pas encore
            personne["photo_id"] = copier_photo_emprunteur(nom, prenom, chemin_image)

        emprunts_en_cours = [e for e in personne['emprunts'].values() if not e['date_retour']]

        nbr_emprunts_actuels = sum(1 for e in personne['emprunts'].values() if not e['date_retour'])
        if nbr_emprunts_actuels + len(livres_a_emprunter) >= 3:
            message = (f"Impossible d'emprunter {len(livres_a_emprunter)} livre(s). Limite de 3 livres atteinte "
                       f"(actuellement {nbr_emprunts_actuels} livres empruntés) !\n\n")
            if nbr_emprunts_actuels == 3:
                for e in emprunts_en_cours:
                    dt_date_emprunt = datetime.strptime(e['date_emprunt'], "%Y-%m-%d")
                    message = message + f"📖 {e['titre']} emprunté le {dt_date_emprunt.strftime('%d-%m-%Y')}\n"
            custom_messagebox(form_window, "Erreur", message, geometry="550x400",
                              parent_to_destroy=form_window if len(emprunts_en_cours) == 3 else None)
            return

        nouveaux_emprunts = []
        for title in livres_a_emprunter:
            livre_trouve = livres.get(title, None)
            if not livre_trouve:
                custom_messagebox(form_window, "Erreur", f"Livre '{title}' non trouvé !")
                return
            elif livre_trouve['Exemplaires'] == 0:
                custom_messagebox(form_window, "Erreur", f"Pas de copies disponibles pour '{title}' !")
                return
            else:
                emprunt_id = str(max([int(k) for k in personne['emprunts'].keys()] + [0]) + 1)
                personne['emprunts'][emprunt_id] = {
                    "titre": title,
                    "date_emprunt": date.today().strftime("%Y-%m-%d"),
                    "date_retour": ""
                }
                livre_trouve['Exemplaires'] -= 1
                nouveaux_emprunts.append(title)

        # Recalculer le nombre de livres empruntés (en cours) après les éventuels ajouts
        personne['nbr_livres_empruntes'] = sum(1 for e in personne['emprunts'].values() if not e['date_retour'])

        if nouveaux_emprunts:  # Fermer form_window uniquement si des livres ont été empruntés
            sauvegarder_emprunts(personnes, fichier_emprunt)
            sauvegarder_bibliotheque(livres, fichier_bibliotheque)

            date_retour_theorique = date.today() + timedelta(days=14)

            clear_result(result_text)
            if not emprunts_en_cours:
                result_text.insert(tk.END, f"Aucun emprunt en cours pour {prenom} {nom} !\n")
            else:
                result_text.insert(tk.END, f"Livre(s) emprunté(s) par {prenom} {nom} :\n")
                for e in emprunts_en_cours:
                    dt_date_emprunt = datetime.strptime(e['date_emprunt'], "%Y-%m-%d")
                    result_text.insert(tk.END, f"📖 {e['titre']} emprunté le {dt_date_emprunt.strftime('%d-%m-%Y')}\n")
            result_text.insert(tk.END, f"- - -\n")
            if len(nouveaux_emprunts) > 0:
                result_text.insert(tk.END, f"{len(nouveaux_emprunts)} livre(s) emprunté(s) aujourd'hui :\n")
                for title in nouveaux_emprunts:
                    result_text.insert(tk.END, f"📗 {title}\n")
                result_text.insert(tk.END, f"👉 Retour avant le {date_retour_theorique.strftime('%d-%m-%Y')} "
                                           f"(14 jours)\n")
            form_window.destroy()

    (ttk.Button(form_window, text="Confirmer", command=submit, style="Custom.TButton")
        .grid(row=4, column=0, columnspan=2, pady=10))
    (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
        .grid(row=5, column=0, columnspan=2))


def rendre_livre(root, result_text, livres, fichier_bibliotheque, personnes, fichier_emprunt):
    """
    :param root: Fenêtre principale de l'application
    :param result_text: Widget de texte pour afficher le résultat
    :param livres: Dictionnaire contenant les données des livres
    :param fichier_bibliotheque: Chaîne représentant le chemin du fichier de la bibliothèque
    :param personnes: Liste de dictionnaires contenant les données des personnes
    :param fichier_emprunt: Chaîne représentant le chemin du fichier des emprunts
    :return: Aucun
    """
    form_window = custom_form_window(root, "Rendre un livre", "400x200")

    custom_font = tkfont.Font(family="Helvetica", size=14)

    ttk.Label(form_window, text="Nom :", font=custom_font, width=12, anchor="e").grid(row=0, column=0, padx=5, pady=5)
    nom_entry = ttk.Entry(form_window, font=custom_font)
    nom_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(form_window, text="Prénom :", font=custom_font, width=12, anchor="e").grid(row=1, column=0, padx=5, pady=5)
    prenom_entry = ttk.Entry(form_window, font=custom_font)
    prenom_entry.grid(row=1, column=1, padx=5, pady=5)

    def submit():
        """Valide les informations saisies pour rendre un livre et ouvre la fenêtre de sélection des emprunts."""
        nom = nom_entry.get().strip()
        prenom = prenom_entry.get().strip()

        if not (nom and prenom):
            custom_messagebox(root, "Erreur", "Tous les champs sont requis!")
            return

        personne = None
        for p in personnes:
            if nom == p['nom'] and prenom == p['prenom']:
                personne = p
                break

        if not personne:
            custom_messagebox(form_window, "Erreur", f"Aucune personne trouvée du nom de {prenom} {nom}",
                              geometry="550x150")
            return

        retours = [
            {"emprunt_id": num, **emprunt}
            for num, emprunt in personne['emprunts'].items()
            if not emprunt['date_retour']
        ]

        if not retours:
            custom_messagebox(form_window, "Erreur", f"{prenom} {nom} n'a aucun emprunt en cours !",
                              geometry="450x350", personne=personne, parent_to_destroy=form_window)
            return

        select_window = custom_form_window(form_window, "Emprunts en cours", "600x700")

        # Étiquette Prénom Nom
        custom_title = tkfont.Font(family="Georgia", size=24)
        (ttk.Label(select_window, text=f"{prenom} {nom}", font=custom_title)
            .grid(row=0, column=0, columnspan=2, padx=30, pady=20))

        afficher_photo(select_window, personne["photo_id"])

        # Étiquette pour sélectionner les livres
        custom_label = tkfont.Font(family="Comic Sans MS", size=16)
        (ttk.Label(select_window, text=f"Sélectionner les livres rapportés :", font=custom_label)
            .grid(row=2, column=0, columnspan=2, padx=50, pady=20))

        selected_books = []
        for i, retour in enumerate(retours, 1):
            var = tk.BooleanVar()
            (ttk.Checkbutton(select_window, text=f"{retour['titre']} (Emprunté le : {retour['date_emprunt']})",
                             variable=var, style="Custom.TCheckbutton")
                .grid(row=i+2, column=0, columnspan=2, sticky="ew", padx=50, pady=10))
            selected_books.append((var, retour))

        def confirm_return():
            """Confirme le retour des livres sélectionnés et calcule les éventuelles pénalités."""
            montant_total = 0
            returned_books = []

            for var, retour in selected_books:
                if var.get():
                    emprunt = personne['emprunts'][retour['emprunt_id']]
                    emprunt['date_retour'] = date.today().strftime("%Y-%m-%d")
                    livre = livres.get(emprunt['titre'], None)
                    if livre:
                        livre['Exemplaires'] += 1

                    date_emprunt = datetime.strptime(emprunt['date_emprunt'], "%Y-%m-%d")
                    date_retour_theorique = date_emprunt + timedelta(days=14)
                    date_retour = datetime.strptime(emprunt['date_retour'], "%Y-%m-%d")

                    if date_retour > date_retour_theorique:
                        jours_supplementaires = (date_retour - date_retour_theorique).days
                        montant_total += 0.10 * jours_supplementaires
                        returned_books.append(
                            f"{emprunt['titre']} : "
                            f"{jours_supplementaires} jour(s) de retard, {0.10 * jours_supplementaires:.2f}€")
                    else:
                        returned_books.append(f"{emprunt['titre']} : Rendu à temps")

            if not returned_books:
                custom_messagebox(select_window, "Info", "Aucun livre sélectionné pour le retour !")
                return

            personne['nbr_livres_empruntes'] = sum(1 for e in personne['emprunts'].values() if not e['date_retour'])
            sauvegarder_emprunts(personnes, fichier_emprunt)
            sauvegarder_bibliotheque(livres, fichier_bibliotheque)

            clear_result(result_text)
            result_text.insert(tk.END, "Livres rendus :\n")
            for book in returned_books:
                result_text.insert(tk.END, f"📗{book}\n")
            if montant_total > 0:
                result_text.insert(tk.END, "- - -\n")
                result_text.insert(tk.END, f"Pénalité totale : {montant_total:.2f}€\n")

            select_window.destroy()
            form_window.destroy()

        (ttk.Button(select_window, text="Confirmer", command=confirm_return, style="Custom.TButton")
            .grid(row=len(retours) + 4, column=0, columnspan=2, pady=25))
        (ttk.Button(select_window, text="Annuler", command=select_window.destroy, style="Custom.TButton")
            .grid(row=len(retours) + 5, column=0, columnspan=2))

    (ttk.Button(form_window, text="Continuer", command=submit, style="Custom.TButton")
        .grid(row=2, column=0, columnspan=2, pady=10))
    (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
        .grid(row=3, column=0, columnspan=2))
