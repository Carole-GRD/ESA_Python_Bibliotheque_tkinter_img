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
    title_entry = ttk.Entry(form_window, font=custom_font)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    def submit():
        """Valide le titre saisi pour supprimer un livre et met à jour la bibliothèque."""
        title = title_entry.get().strip().lower()
        found_title = None
        for t in livres:
            if t.lower() == title:
                found_title = t
                break

        if found_title:
            del livres[found_title]
            sauvegarder_bibliotheque(livres, fichier_bibliotheque)
            form_window.destroy()
            clear_result(result_text)
            result_text.insert(tk.END, f'Le livre "{found_title}" a été supprimé de la bibliothèque !\n')
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
        found_books = {}

        if filter_type == "Titre":
            for title, info in livres.items():
                if term in title.lower():
                    found_books[title] = info
        else:
            for title, info in livres.items():
                if term in str(info[filter_type]).lower():
                    found_books[title] = info

        clear_result(result_text)
        if found_books:
            result_text.insert(tk.END, "Titre, Auteur, Date de publication, Genre, Exemplaires\n")
            result_text.insert(tk.END, "--------------------------------------------------------\n")
            for title, info in found_books.items():
                result_text.insert(tk.END,
                                   f"{title}, {info['Auteur']}, {info['Année']}, {info['Genre']}, "
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
