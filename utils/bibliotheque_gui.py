"""
    Module bibliotheque : gestion des livres

    Fonctions :
        • clear_result
        • ajouter_livre
        • supprimer_livre
        • chercher_livre (par titre, auteur ou genre)
        • afficher_livres
        • emprunter_livre (mettre à jour le nombre d’exemplaires et le fichier csv)
        • rendre_livre (mettre à jour le nombre d’exemplaires et le fichier csv)
        • afficher_menu (+ gestion des interactions)
"""
import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.font as tkfont
from datetime import date

from utils.custom_messagebox import custom_messagebox
from utils.custom_form_window import custom_form_window
from utils.custom_form_window import resize_form_window
from utils.gestion_fichiers import sauvegarder_bibliotheque


def clear_result(result_text):
    """
    :param result_text: Widget de texte à vider
    :return: Aucun
    """
    result_text.delete(1.0, tk.END)


def ajouter_livre(root, result_text, livres, fichier_bibliotheque):
    """
    :param root: Fenêtre principale de l'application
    :param result_text: Widget de texte pour afficher le résultat
    :param livres: Dictionnaire contenant les données des livres
    :param fichier_bibliotheque: Chaîne représentant le chemin du fichier de la bibliothèque
    :return: Aucun
    """
    form_window = custom_form_window(root, "Ajouter un livre", "600x300")

    # Définir une police personnalisée
    custom_font = tkfont.Font(family="Helvetica", size=14)

    fields = ["Titre", "Auteur", "Année de publication", "Genre", "Nombre d'exemplaires"]
    entries = {}

    for i, field in enumerate(fields):
        (ttk.Label(form_window, text=f"{field} : ", font=custom_font, width=20, anchor="e")
            .grid(row=i, column=0, padx=5, pady=5))
        entries[field] = ttk.Entry(form_window, font=custom_font)
        entries[field].grid(row=i, column=1, padx=5, pady=5)

    def submit():
        """Valide les informations saisies pour ajouter un livre et met à jour la bibliothèque."""
        try:
            title = entries["Titre"].get().strip()
            author = entries["Auteur"].get().strip()
            year = int(entries["Année de publication"].get())
            genre = entries["Genre"].get().strip()
            copies = int(entries["Nombre d'exemplaires"].get())

            if year < 0 or year > date.today().year:
                custom_messagebox(form_window, "Erreur", "Année invalide !")
                return
            if copies < 0:
                custom_messagebox(form_window, "Erreur", "Le nombre d'exemplaires ne peut pas être négatif !")
                return
            if not title:
                custom_messagebox(form_window, "Erreur", "Le titre est obligatoire !")
                return

            livres[title] = {
                "Auteur": author,
                "Année": year,
                "Genre": genre,
                "Exemplaires": copies
            }
            sauvegarder_bibliotheque(livres, fichier_bibliotheque)

            form_window.destroy()
            clear_result(result_text)
            result_text.insert(tk.END, f'Le livre "{title}" a été ajouté à la bibliothèque !\n')
        except ValueError:
            custom_messagebox(form_window, "Erreur", "année et exemplaires doivent être des nombres !")

    (ttk.Button(form_window, text="Ajouter", command=submit, style="Custom.TButton")
        .grid(row=len(fields), column=0, columnspan=2, pady=10))
    (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
        .grid(row=len(fields) + 1, column=0, columnspan=2))


def modifier_livre(root, result_text, livres, fichier_bibliotheque):
    """
    :param root: Fenêtre principale de l'application
    :param result_text: Widget de texte pour afficher le résultat
    :param livres: Dictionnaire contenant les données des livres
    :param fichier_bibliotheque: Chaîne représentant le chemin du fichier de la bibliothèque
    :return: Aucun
    """
    form_window = custom_form_window(root, "Modifier un livre", "600x500")
    custom_font = tkfont.Font(family="Helvetica", size=14)

    # Champ initial pour le titre original
    ttk.Label(form_window, text="Titre original :", font=custom_font).grid(row=0, column=0, padx=10, pady=10, sticky="e")
    titre_original_input = ttk.Entry(form_window, font=custom_font)
    titre_original_input.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    def continue_action():
        """Valide le titre original et affiche les anciennes valeurs ainsi que les champs de modification."""
        titre_original = titre_original_input.get().strip().lower()
        titre_trouve = None
        for titre in livres:
            if titre.lower() == titre_original:
                titre_trouve = titre
                break

        if not titre_trouve:
            custom_messagebox(form_window, "Erreur", "Livre non trouvé !")
            return

        # Supprimer les widgets initiaux
        print("Destruction des widgets initiaux...")
        for widget in form_window.winfo_children():
            widget.destroy()

        # Redimensionner et centrer la fenêtre
        nouvelles_dimensions = resize_form_window(root, 750, 750)
        form_window.geometry(nouvelles_dimensions)

        # Créer un Frame pour regrouper les éléments
        frame = ttk.Frame(form_window)
        frame.grid(row=0, column=0, padx=25, pady=10, sticky="nsew")

        # Configurer la grille du frame
        form_window.columnconfigure(0, weight=1)
        form_window.rowconfigure(0, weight=1)

        # Créer une nouvelle variable pour les anciennes valeurs
        preview_text = tk.StringVar()
        livre = livres[titre_trouve]
        preview_content = (
            f"Titre : {titre_trouve}\n"
            f"Auteur : {livre.get('Auteur', 'Inconnu')}\n"
            f"Année : {livre.get('Année', 'Inconnue')}\n"
            f"Genre : {livre.get('Genre', 'Inconnu')}\n"
            f"Exemplaires : {livre.get('Exemplaires', 0)}"
        )
        print("Contenu de preview_text avant set:", preview_content)
        preview_text.set(preview_content)
        print("Contenu de preview_text après set:", preview_text.get())

        # Afficher les anciennes valeurs (test avec texte statique pour débogage)
        custom_title = tkfont.Font(family="Georgia", size=24, weight="bold")
        (ttk.Label(frame, text="Anciennes valeurs :", font=custom_title, background="#f0f0f0", foreground="darkblue")
            .pack(pady=5, anchor="w"))
        preview_label = ttk.Label(frame, text=preview_content, font=custom_font, wraplength=500, justify="left")
        preview_label.pack(pady=5, anchor="w")
        print("preview_label créé avec texte statique:", preview_label)

        # Forcer le rafraîchissement
        form_window.update()
        form_window.update_idletasks()
        print("Interface mise à jour après création de preview_label")

        # Champs pour les nouvelles valeurs
        custom_title = tkfont.Font(family="Georgia", size=24, weight="bold")
        (ttk.Label(frame, text="Nouvelles valeurs :", font=custom_title, background="#f0f0f0", foreground="darkblue")
            .pack(pady=5, anchor="w"))

        ttk.Label(frame, text="Nouveau titre :", font=custom_font).pack(pady=5, anchor="w")
        nouveau_titre_input = ttk.Entry(frame, font=custom_font)
        nouveau_titre_input.pack(pady=5, fill="x")

        ttk.Label(frame, text="Auteur :", font=custom_font).pack(pady=5, anchor="w")
        auteur_input = ttk.Entry(frame, font=custom_font)
        auteur_input.pack(pady=5, fill="x")

        ttk.Label(frame, text="Année :", font=custom_font).pack(pady=5, anchor="w")
        annee_input = ttk.Entry(frame, font=custom_font)
        annee_input.pack(pady=5, fill="x")

        ttk.Label(frame, text="Genre :", font=custom_font).pack(pady=5, anchor="w")
        genre_input = ttk.Entry(frame, font=custom_font)
        genre_input.pack(pady=5, fill="x")

        ttk.Label(frame, text="Nombre d'exemplaires :", font=custom_font).pack(pady=5, anchor="w")
        exemplaires_input = ttk.Entry(frame, font=custom_font)
        exemplaires_input.pack(pady=5, fill="x")

        # Forcer un autre rafraîchissement après ajout des champs
        form_window.update()
        form_window.update_idletasks()
        print("Interface mise à jour après ajout des champs")

        def submit():
            """Valide les informations saisies pour modifier un livre et met à jour la bibliothèque."""
            nouveau_titre = nouveau_titre_input.get().strip()
            try:
                nouveaux_exemplaires = int(exemplaires_input.get().strip()) if exemplaires_input.get().strip() else None
                if nouveaux_exemplaires is not None and nouveaux_exemplaires < 0:
                    raise ValueError
                nouvelle_annee = int(annee_input.get().strip()) if annee_input.get().strip() else None
                if nouvelle_annee is not None and (nouvelle_annee < 0 or nouvelle_annee > 2025):
                    raise ValueError("L'année doit être entre 0 et 2025 !")
            except ValueError as e:
                custom_messagebox(form_window, "Erreur", f"Erreur de saisie : "
                                                         f"{e if e != '' else 'Les nombres doivent être valides !'}")
                return

            nouveau_auteur = auteur_input.get().strip() if auteur_input.get().strip() else None
            nouveau_genre = genre_input.get().strip() if genre_input.get().strip() else None

            # Sauvegarder les anciennes valeurs avant de modifier
            anciennes_valeurs = {
                'Titre': titre_trouve,
                'Exemplaires': livres[titre_trouve].get("Exemplaires", 0),
                'Auteur': livres[titre_trouve].get("Auteur", "Inconnu"),
                'Année': livres[titre_trouve].get("Année", "Inconnue"),
                'Genre': livres[titre_trouve].get("Genre", "Inconnu")
            }

            # Mettre à jour les informations
            titre_actuel = titre_trouve  # Par défaut, utiliser l'ancienne clé
            if nouveau_titre and nouveau_titre != titre_trouve:
                livres[nouveau_titre] = livres.pop(titre_trouve)
                titre_actuel = nouveau_titre
            if nouveaux_exemplaires is not None:
                livres[titre_actuel]['Exemplaires'] = nouveaux_exemplaires
            if nouveau_auteur:
                livres[titre_actuel]['Auteur'] = nouveau_auteur
            if nouvelle_annee is not None:
                livres[titre_actuel]['Année'] = nouvelle_annee
            if nouveau_genre:
                livres[titre_actuel]['Genre'] = nouveau_genre

            sauvegarder_bibliotheque(livres, fichier_bibliotheque)
            form_window.destroy()
            clear_result(result_text)
            result_text.insert(tk.END, f'Anciennes valeurs : Titre="{anciennes_valeurs["Titre"]}", '
                                       f'Auteur="{anciennes_valeurs["Auteur"]}", '
                                       f'Année={anciennes_valeurs["Année"]}, '
                                       f'Genre="{anciennes_valeurs["Genre"]}", '
                                       f'Exemplaires={anciennes_valeurs["Exemplaires"]}')
            result_text.insert(tk.END, f'\nNouvelles valeurs : Titre="{titre_actuel}", '
                                       f'Auteur="{livres[titre_actuel].get("Auteur", "Inconnu")}", '
                                       f'Année={livres[titre_actuel].get("Année", "Inconnue")}, '
                                       f'Genre="{livres[titre_actuel].get("Genre", "Inconnu")}", '
                                       f'Exemplaires={livres[titre_actuel].get("Exemplaires", 0)}')

        ttk.Button(frame, text="Modifier", command=submit, style="Custom.TButton").pack(pady=5)
        ttk.Button(frame, text="Annuler", command=form_window.destroy, style="Custom.TButton").pack(pady=5)

        # Dernier rafraîchissement après ajout des boutons
        form_window.update()
        form_window.update_idletasks()
        print("Interface mise à jour après ajout des boutons")

    # Bouton initial
    (ttk.Button(form_window, text="Continuer", command=continue_action, style="Custom.TButton")
        .grid(row=1, column=0, columnspan=2, pady=15))
    (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
        .grid(row=2, column=0, columnspan=2, pady=15))


def supprimer_livre(root, result_text, livres, fichier_bibliotheque):
    """
    :param root: Fenêtre principale de l'application
    :param result_text: Widget de texte pour afficher le résultat
    :param livres: Dictionnaire contenant les données des livres
    :param fichier_bibliotheque: Chaîne représentant le chemin du fichier de la bibliothèque
    :return: Aucun
    """
    form_window = custom_form_window(root, "Supprimer un livre", "600x150")

    custom_font = tkfont.Font(family="Helvetica", size=14)

    ttk.Label(form_window, text="Titre du livre :", font=custom_font).grid(row=0, column=0, padx=5, pady=5)
    titre_input = ttk.Entry(form_window, font=custom_font)
    titre_input.grid(row=0, column=1, padx=5, pady=5)

    def submit():
        """Valide le titre saisi pour supprimer un livre et met à jour la bibliothèque."""
        titre = titre_input.get().strip().lower()
        titre_trouve = None
        for t in livres:
            if t.lower() == titre.lower():
                titre_trouve = t
                break

        if titre_trouve:
            del livres[titre_trouve]
            sauvegarder_bibliotheque(livres, fichier_bibliotheque)
            form_window.destroy()
            clear_result(result_text)
            result_text.insert(tk.END, f'Le livre "{titre_trouve}" a été supprimé de la bibliothèque !\n')
        else:
            custom_messagebox(form_window, "Erreur", "Livre non trouvé !")

    (ttk.Button(form_window, text="Supprimer", command=submit, style="Custom.TButton")
        .grid(row=1, column=0, columnspan=2, pady=10))
    (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
        .grid(row=2, column=0, columnspan=2))


def rechercher_livre(root, result_text, livres):
    """
    :param root: Fenêtre principale de l'application
    :param result_text: Widget de texte pour afficher le résultat
    :param livres: Dictionnaire contenant les données des livres
    :return: Aucun
    """
    form_window = custom_form_window(root, "Chercher un livre", "600x200")

    custom_font = tkfont.Font(family="Helvetica", size=14)

    # Menu déroulant pour choisir le filtre (titre - auteur - genre)
    (ttk.Label(form_window, text="Recherche par : ", font=custom_font, width=20, anchor="e")
        .grid(row=0, column=0, padx=5, pady=5))
    search_var = tk.StringVar(value="Titre")
    search_type = tk.OptionMenu(form_window, search_var, "Titre", "Auteur", "Genre")
    search_type.config(font=custom_font)
    search_type.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    # Appliquer la police au menu déroulant
    search_type["menu"].config(font=custom_font)

    # Les termes recherchés
    (ttk.Label(form_window, text="Que recherchez-vous ? ", font=custom_font, width=20, anchor="e")
        .grid(row=1, column=0, padx=5, pady=5))
    search_term = ttk.Entry(form_window, font=custom_font)
    search_term.grid(row=1, column=1, padx=5, pady=5)

    def submit():
        """Effectue la recherche d'un livre selon le critère et le terme saisis, puis affiche les résultats."""
        filter_type = search_var.get()
        term = search_term.get().strip().lower()
        livres_trouves = {}

        if filter_type == "Titre":
            for titre, info in livres.items():
                if term in titre.lower():
                    livres_trouves[titre] = info
        else:
            for titre, info in livres.items():
                if term in str(info[filter_type]).lower():
                    livres_trouves[titre] = info

        clear_result(result_text)
        if livres_trouves:
            result_text.insert(tk.END, "Titre, Auteur, Date de publication, Genre, Exemplaires\n")
            result_text.insert(tk.END, "--------------------------------------------------------\n")
            for titre, info in livres_trouves.items():
                result_text.insert(tk.END,
                                   f"{titre}, {info['Auteur']}, {info['Année']}, {info['Genre']}, "
                                   f"{info['Exemplaires']}\n")
        else:
            result_text.insert(tk.END, f"Aucun livre trouvé pour "
                                       f"{'l\'' if filter_type == 'Auteur' else 'le '}"
                                       f"{filter_type.lower()} : {term}\n")
        form_window.destroy()

    (ttk.Button(form_window, text="Rechercher", command=submit, style="Custom.TButton")
        .grid(row=2, column=0, columnspan=2, pady=10))
    (ttk.Button(form_window, text="Annuler", command=form_window.destroy, style="Custom.TButton")
        .grid(row=3, column=0, columnspan=2))


def afficher_livres(result_text, livres):
    """
    :param result_text: Widget de texte pour afficher le résultat
    :param livres: Dictionnaire contenant les données des livres
    :return: Aucun
    """
    clear_result(result_text)
    result_text.insert(tk.END, "Titre, Auteur, Date de publication, Genre, Exemplaires\n")
    result_text.insert(tk.END, "--------------------------------------------------------\n")
    for title, info in livres.items():
        result_text.insert(tk.END,
                           f"{title}, {info['Auteur']}, {info['Année']}, {info['Genre']}, {info['Exemplaires']}\n")
