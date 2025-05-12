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
from utils.custom_form_window import resize_form_window
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
        if nom.capitalize() == p['nom'] and prenom.capitalize() == p['prenom']:
            return p
    personne = {
        "nom": nom.capitalize(),
        "prenom": prenom.capitalize(),
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
    form_window = custom_form_window(root, "Emprunter un livre", "600x350")
    custom_font = tkfont.Font(family="Helvetica", size=16)

    # Variables globales au scope de la fonction
    photo_path = tk.StringVar()
    photo_image = None  # Référence nécessaire pour éviter la collecte par le garbage collector

    # Champs Nom
    (ttk.Label(form_window, text="Nom : ", font=custom_font, width=15, anchor="e")
        .grid(row=0, column=0, padx=5, pady=5, sticky="e"))
    nom_entry = ttk.Entry(form_window, font=custom_font)
    nom_entry.grid(row=0, column=1, padx=10, pady=10)

    # Champs Prénom
    (ttk.Label(form_window, text="Prénom : ", font=custom_font, width=15, anchor="e")
        .grid(row=1, column=0, padx=5, pady=5, sticky="e"))
    prenom_entry = ttk.Entry(form_window, font=custom_font)
    prenom_entry.grid(row=1, column=1, padx=10, pady=10)

    def check_person():
        """Vérifie si la personne existe et affiche les champs correspondants."""
        nom = nom_entry.get().strip().capitalize()
        prenom = prenom_entry.get().strip().capitalize()

        if not (nom and prenom):
            custom_messagebox(form_window, "Erreur", "Le nom et le prénom sont obligatoires !")
            return

        personne = trouver_ou_creer_personne(personnes, nom, prenom)
        est_une_nouvelle_personne = len(personne['emprunts']) == 0 and not personne["photo_id"]

        # Supprimer les champs nom et prénom pour faire place aux nouveaux champs
        for widget in form_window.winfo_children():
            widget.destroy()

        preview_label = ttk.Label(form_window)

        def select_photo():
            """Ouvre une boîte de dialogue pour sélectionner une photo et affiche un aperçu."""
            nonlocal photo_image
            chemin = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
            if chemin:
                photo_path.set(chemin)
                photo_label.config(text=os.path.basename(chemin))
                img = Image.open(chemin)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                photo_image = ImageTk.PhotoImage(img)
                preview_label.config(image=photo_image)
                preview_label.image = photo_image  # Conserver la référence
                form_window.update()  # Forcer le rafraîchissement de l'interface

        if est_une_nouvelle_personne:
            # Cas : Nouvelle personne
            nouvelles_dimensions = resize_form_window(root, 800, 800)
            form_window.geometry(nouvelles_dimensions)

            custom_title = tkfont.Font(family="Georgia", size=24, weight="bold")
            (ttk.Label(form_window, text=f"{prenom} {nom}", font=custom_title, background="#f0f0f0", foreground="darkblue")
                .grid(row=0, column=0, padx=200, pady=20))

            # Sélection de la photo (créer un Frame pour regrouper les éléments)
            frame = ttk.Frame(form_window)
            frame.grid(row=1, column=0, padx=25, pady=10)

            # Placer les éléments dans le Frame avec pack pour un agencement vertical
            ttk.Label(frame, text="Photo : ", font=custom_font, width=15, anchor="center").pack(pady=5)
            ttk.Button(frame, text="Choisir une photo", command=select_photo, style="Custom.TButton").pack(pady=5)
            photo_label = ttk.Label(frame, text="Aucune image sélectionnée", font=custom_font, width=30,
                                    anchor="center")
            photo_label.pack(pady=5)

            # Afficher la photo
            preview_label.grid(row=2, column=0, padx=5, pady=5)

            # Champ pour les livres
            (ttk.Label(form_window, text="Titres des livres : ", font=custom_font, width=20, foreground='')
             .grid(row=3, column=0, padx=100, pady=20))
            livres_text = tk.Text(form_window, height=4, width=30, font=custom_font)
            livres_text.grid(row=4, column=0, padx=100, pady=20)
        else:
            # Cas : Personne existante
            custom_title = tkfont.Font(family="Georgia", size=24, weight="bold")
            (ttk.Label(form_window, text=f"{prenom} {nom}", font=custom_title, background="#f0f0f0", foreground="darkblue")
                .grid(row=0, column=0, padx=200, pady=20))

            if personne["photo_id"]:
                # Afficher la photo s'il y en a une déjà enregistrée
                nouvelles_dimensions = resize_form_window(root, 650, 650)
                form_window.geometry(nouvelles_dimensions)
                photo_label = ttk.Label(form_window, anchor="center")
                photo_label.grid(row=1, column=0, padx=200, pady=20)
                existing_photo_path = os.path.join("data/photos", personne["photo_id"])
                if os.path.exists(existing_photo_path):
                    img = Image.open(existing_photo_path)
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)
                    photo_image = ImageTk.PhotoImage(img)
                    photo_label.config(image=photo_image)
                    photo_label.image = photo_image  # Garder la référence
                else:
                    photo_label.config(text="Photo non trouvée")
            else:
                # Option pour ajouter une photo si elle n'existe pas
                nouvelles_dimensions = resize_form_window(root, 650, 800)
                form_window.geometry(nouvelles_dimensions)

                # Créer un Frame pour regrouper les éléments
                frame = ttk.Frame(form_window)
                frame.grid(row=1, column=0, padx=25, pady=10)

                # Placer les éléments dans le Frame avec pack pour un agencement vertical
                ttk.Label(frame, text="Photo : ", font=custom_font, width=15, anchor="center").pack(pady=5)
                ttk.Button(frame, text="Choisir une photo", command=select_photo, style="Custom.TButton").pack(pady=5)
                photo_label = ttk.Label(frame, text="Aucune image sélectionnée", font=custom_font, width=30,
                                        anchor="center")
                photo_label.pack(pady=5)

                # Afficher la photo
                preview_label.grid(row=2, column=0, padx=5, pady=5)

            # Champ pour les livres à emprunter (uniquement une fois)
            (ttk.Label(form_window, text="Titres des livres à emprunter : ", width=30, font=('Verdana', 16),
                       foreground="darkblue", background="#f0f0f0", anchor='center')
             .grid(row=3, column=0, padx=100, pady=20))
            livres_text = tk.Text(form_window, height=4, width=30, font=custom_font)
            livres_text.grid(row=4, column=0, padx=100, pady=20)

        def submit():
            """Valide les informations saisies pour emprunter un livre et met à jour les données."""
            livres_input = livres_text.get("1.0", tk.END).strip().splitlines()
            livres_a_emprunter = [title.strip() for title in livres_input if title.strip()]

            if not livres_a_emprunter:
                custom_messagebox(form_window, "Erreur", "Aucun livre sélectionné !")
                return

            # Gérer la photo
            chemin_image = photo_path.get()
            if chemin_image and not personne["photo_id"]:
                personne["photo_id"] = copier_photo_emprunteur(nom, prenom, chemin_image)

            emprunts_en_cours = [e for e in personne['emprunts'].values() if not e['date_retour']]

            nbr_emprunts_actuels = sum(1 for e in personne['emprunts'].values() if not e['date_retour'])
            if nbr_emprunts_actuels + len(livres_a_emprunter) > 3:
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

            personne['nbr_livres_empruntes'] = sum(1 for e in personne['emprunts'].values() if not e['date_retour'])

            if nouveaux_emprunts:
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
                    result_text.insert(tk.END, f"👉 Retour avant le {date_retour_theorique.strftime('%d-%m-%Y')} (14 jours)\n")
                form_window.destroy()

        # row_numero = 4 if est_une_nouvelle_personne else 5
        (ttk.Button(form_window, text="Confirmer", command=submit, style="Custom.TButton")
            .grid(row=5, column=0, padx=200, pady=10))
        (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
            .grid(row=6, column=0, padx=200, pady=10))

    (ttk.Button(form_window, text="Continuer", command=check_person, style="Custom.TButton")
        .grid(row=2, column=0, columnspan=2, pady=10))
    (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
        .grid(row=3, column=0, columnspan=2))


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
    form_window = custom_form_window(root, "Rendre un livre", "600x350")
    custom_font = tkfont.Font(family="Helvetica", size=14)

    # Champs Nom
    ttk.Label(form_window, text="Nom :", font=custom_font, width=12, anchor="e").grid(row=0, column=0, padx=5, pady=5)
    nom_entry = ttk.Entry(form_window, font=custom_font)
    nom_entry.grid(row=0, column=1, padx=5, pady=5)

    # Champs Prénom
    ttk.Label(form_window, text="Prénom :", font=custom_font, width=12, anchor="e").grid(row=1, column=0, padx=5, pady=5)
    prenom_entry = ttk.Entry(form_window, font=custom_font)
    prenom_entry.grid(row=1, column=1, padx=5, pady=5)

    def submit():
        """Valide les informations saisies pour rendre un livre et affiche les emprunts dans la même fenêtre."""
        nom = nom_entry.get().strip().capitalize()
        prenom = prenom_entry.get().strip().capitalize()

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

        # Supprimer les widgets existants
        for widget in form_window.winfo_children():
            widget.destroy()

        if personne['photo_id']:
            nouvelles_dimensions = resize_form_window(root, 650, 800)
            form_window.geometry(nouvelles_dimensions)
        else:
            nouvelles_dimensions = resize_form_window(root, 650, 650)
            form_window.geometry(nouvelles_dimensions)

        custom_title = tkfont.Font(family="Georgia", size=24, weight="bold")
        (ttk.Label(form_window, text=f"{prenom} {nom}", font=custom_title, background="#f0f0f0", foreground="darkblue")
            .grid(row=0, column=0, columnspan=2, padx=30, pady=20))

        photo_label = ttk.Label(form_window)
        photo_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        afficher_photo(form_window, personne["photo_id"])

        (ttk.Label(form_window, text=f"Sélectionner les livres rapportés :", font=('Verdana', 16),
                   foreground="darkblue", background="#f0f0f0")
            .grid(row=2, column=0, columnspan=2, padx=50, pady=20))

        selected_books = []
        for i, retour in enumerate(retours, 1):
            var = tk.BooleanVar()
            (ttk.Checkbutton(form_window, text=f"{retour['titre']} (Emprunté le : {retour['date_emprunt']})",
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
                custom_messagebox(form_window, "Info", "Aucun livre sélectionné pour le retour !")
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

            form_window.destroy()

        (ttk.Button(form_window, text="Confirmer", command=confirm_return, style="Custom.TButton")
            .grid(row=len(retours) + 4, column=0, columnspan=2, pady=25))
        (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
            .grid(row=len(retours) + 5, column=0, columnspan=2))

    (ttk.Button(form_window, text="Continuer", command=submit, style="Custom.TButton")
        .grid(row=2, column=0, columnspan=2, pady=10))
    (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
        .grid(row=3, column=0, columnspan=2))


def modifier_personne(root, result_text, personnes, fichier_emprunt):
    """
    :param root: Fenêtre principale de l'application
    :param result_text: Widget de texte pour afficher le résultat
    :param personnes: Liste de dictionnaires contenant les données des personnes
    :param fichier_emprunt: Chaîne représentant le chemin du fichier des emprunts
    :return: Aucun
    """
    form_window = custom_form_window(root, "Modifier une personne", "600x350")
    custom_font = tkfont.Font(family="Helvetica", size=14)

    # Variables globales pour la photo
    photo_path = tk.StringVar()
    photo_image_old = None  # Référence pour l'ancienne photo
    photo_image_new = None  # Référence pour la nouvelle photo

    # Champs Nom
    ttk.Label(form_window, text="Nom :", font=custom_font, width=12, anchor="e").grid(row=0, column=0, padx=5, pady=5)
    nom_entry = ttk.Entry(form_window, font=custom_font)
    nom_entry.grid(row=0, column=1, padx=5, pady=5)

    # Champs Prénom
    ttk.Label(form_window, text="Prénom :", font=custom_font, width=12, anchor="e").grid(row=1, column=0, padx=5, pady=5)
    prenom_entry = ttk.Entry(form_window, font=custom_font)
    prenom_entry.grid(row=1, column=1, padx=5, pady=5)

    def continue_action():
        """Valide le nom et prénom de la personne et affiche les anciennes valeurs ainsi que les champs de modification."""
        nom = nom_entry.get().strip().capitalize()
        prenom = prenom_entry.get().strip().capitalize()

        if not (nom and prenom):
            custom_messagebox(form_window, "Erreur", "Le nom et le prénom sont obligatoires !")
            return

        personne = None
        for p in personnes:
            if nom == p['nom'] and prenom == p['prenom']:
                personne = p
                break

        if not personne:
            custom_messagebox(form_window, "Erreur", f"Aucune personne trouvée du nom de {prenom} {nom} !")
            return

        # Supprimer les widgets initiaux
        print("Destruction des widgets initiaux...")
        for widget in form_window.winfo_children():
            widget.destroy()

        # Redimensionner et centrer la fenêtre
        nouvelles_dimensions = resize_form_window(root, 750, 900)  # Augmenté la hauteur pour les deux photos
        form_window.geometry(nouvelles_dimensions)

        # Créer un Frame pour regrouper les éléments
        frame = ttk.Frame(form_window)
        frame.grid(row=0, column=0, padx=25, pady=10, sticky="nsew")

        # Configurer la grille du frame
        form_window.columnconfigure(0, weight=1)
        form_window.rowconfigure(0, weight=1)

        # Créer une variable pour les anciennes valeurs
        preview_content = (
            f"Nom : {personne['nom']}\n"
            f"Prénom : {personne['prenom']}\n"
            f"Photo : {personne['photo_id'] if personne['photo_id'] else 'Aucune'}"
        )
        print("Contenu des anciennes valeurs:", preview_content)

        # Afficher les anciennes valeurs
        custom_title = tkfont.Font(family="Georgia", size=24, weight="bold")
        (ttk.Label(frame, text="Anciennes valeurs :", font=custom_title, background="#f0f0f0", foreground="darkblue")
            .pack(pady=5, anchor="w"))
        preview_label = ttk.Label(frame, text=preview_content, font=custom_font, wraplength=500, justify="left")
        preview_label.pack(pady=5, anchor="w")
        print("preview_label créé:", preview_label)

        # Afficher l'ancienne photo (si elle existe)
        old_photo_preview_label = ttk.Label(frame)
        old_photo_preview_label.pack(pady=5)
        if personne["photo_id"]:
            photo_path_existing = os.path.join("data/photos", personne["photo_id"])
            if os.path.exists(photo_path_existing):
                img = Image.open(photo_path_existing)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                nonlocal photo_image_old
                photo_image_old = ImageTk.PhotoImage(img)
                old_photo_preview_label.config(image=photo_image_old)
                old_photo_preview_label.image = photo_image_old  # Garder la référence
            else:
                old_photo_preview_label.config(text="Photo non trouvée")

        # Forcer le rafraîchissement
        form_window.update()
        form_window.update_idletasks()
        print("Interface mise à jour après création de preview_label")

        # Champs pour les nouvelles valeurs
        (ttk.Label(frame, text="Nouvelles valeurs :", font=custom_title, background="#f0f0f0", foreground="darkblue")
            .pack(pady=5, anchor="w"))

        ttk.Label(frame, text="Nouveau nom :", font=custom_font).pack(pady=5, anchor="w")
        nouveau_nom_input = ttk.Entry(frame, font=custom_font)
        nouveau_nom_input.pack(pady=5, fill="x")

        ttk.Label(frame, text="Nouveau prénom :", font=custom_font).pack(pady=5, anchor="w")
        nouveau_prenom_input = ttk.Entry(frame, font=custom_font)
        nouveau_prenom_input.pack(pady=5, fill="x")

        # Sélection de la nouvelle photo
        ttk.Label(frame, text="Nouvelle photo :", font=custom_font).pack(pady=5, anchor="w")
        photo_label = ttk.Label(frame, text="Aucune image sélectionnée", font=custom_font)
        photo_label.pack(pady=5, anchor="w")

        # Label pour afficher la nouvelle photo choisie
        new_photo_preview_label = ttk.Label(frame)
        new_photo_preview_label.pack(pady=5)

        def select_photo():
            """Ouvre une boîte de dialogue pour sélectionner une nouvelle photo et affiche un aperçu."""
            nonlocal photo_image_new
            chemin = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png")])
            if chemin:
                photo_path.set(chemin)
                photo_label.config(text=os.path.basename(chemin))
                img = Image.open(chemin)
                img = img.resize((150, 150), Image.Resampling.LANCZOS)
                photo_image_new = ImageTk.PhotoImage(img)
                new_photo_preview_label.config(image=photo_image_new)
                new_photo_preview_label.image = photo_image_new  # Conserver la référence
                form_window.update()

        ttk.Button(frame, text="Choisir une photo", command=select_photo, style="Custom.TButton").pack(pady=5)

        # Forcer un autre rafraîchissement après ajout des champs
        form_window.update()
        form_window.update_idletasks()
        print("Interface mise à jour après ajout des champs")

        def submit():
            """Valide les informations saisies pour modifier une personne et met à jour les données."""
            nouveau_nom = nouveau_nom_input.get().strip().capitalize()
            nouveau_prenom = nouveau_prenom_input.get().strip().capitalize()
            chemin_image = photo_path.get()

            # Vérifier que au moins une modification est prévue
            if not chemin_image and nouveau_nom == personne['nom'] and nouveau_prenom == personne['prenom']:
                custom_messagebox(form_window, "Erreur", "Aucune modification détectée !")
                return

            # Sauvegarder les anciennes valeurs avant de modifier
            anciennes_valeurs = {
                'Nom': personne['nom'],
                'Prénom': personne['prenom'],
                'Photo': personne['photo_id'] if personne['photo_id'] else 'Aucune'
            }

            # Mettre à jour les informations
            if nouveau_nom:
                personne['nom'] = nouveau_nom
            if nouveau_prenom:
                personne['prenom'] = nouveau_prenom

            # Gérer la photo
            if chemin_image:
                # Supprimer l'ancienne photo si elle existe
                if personne['photo_id']:
                    ancienne_photo_path = os.path.join("data/photos", personne['photo_id'])
                    if os.path.exists(ancienne_photo_path):
                        os.remove(ancienne_photo_path)
                # Copier la nouvelle photo avec les nouveaux nom et prénom
                personne['photo_id'] = copier_photo_emprunteur(personne['nom'], personne['prenom'], chemin_image)
            elif personne['photo_id'] and (
                    nouveau_nom != anciennes_valeurs['Nom'] or nouveau_prenom != anciennes_valeurs['Prénom']):
                # Si une photo existe et que le nom ou le prénom a changé, renommer l'ancienne photo
                ancienne_photo_path = os.path.join("data/photos", personne['photo_id'])
                if os.path.exists(ancienne_photo_path):
                    # Extraire l'extension du nom actuel
                    extension = os.path.splitext(personne['photo_id'])[1]
                    nouveau_nom_fichier = (f"{personne['nom'].lower()}_{personne['prenom'].lower()}"
                                           f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}{extension}")
                    nouveau_photo_path = os.path.join("data/photos", nouveau_nom_fichier)
                    os.rename(ancienne_photo_path, nouveau_photo_path)
                    personne['photo_id'] = nouveau_nom_fichier

            sauvegarder_emprunts(personnes, fichier_emprunt)
            form_window.destroy()
            clear_result(result_text)
            result_text.insert(tk.END, f'La personne "{nouveau_prenom} {nouveau_nom}" a été modifiée avec succès !\n')
            result_text.insert(tk.END, f'Anciennes valeurs : Nom="{anciennes_valeurs["Nom"]}", '
                                       f'Prénom="{anciennes_valeurs["Prénom"]}", '
                                       f'Photo="{anciennes_valeurs["Photo"]}"\n')
            result_text.insert(tk.END, f'Nouvelles valeurs : Nom="{personne["nom"]}", '
                                       f'Prénom="{personne["prenom"]}", '
                                       f'Photo="{personne["photo_id"] if personne["photo_id"] else "Aucune"}"\n')

        ttk.Button(frame, text="Modifier", command=submit, style="Custom.TButton").pack(pady=5)
        ttk.Button(frame, text="Annuler", command=form_window.destroy, style="Custom.TButton").pack(pady=5)

        # Dernier rafraîchissement après ajout des boutons
        form_window.update()
        form_window.update_idletasks()
        print("Interface mise à jour après ajout des boutons")

    # Boutons initiaux
    (ttk.Button(form_window, text="Continuer", command=continue_action, style="Custom.TButton")
        .grid(row=2, column=0, columnspan=2, pady=10))
    (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
        .grid(row=3, column=0, columnspan=2))