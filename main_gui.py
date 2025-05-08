"""
    Programme principal : interface créée avec tkinter
"""
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from utils.bibliotheque_gui import afficher_livres
from utils.bibliotheque_gui import ajouter_livre
from utils.bibliotheque_gui import rechercher_livre
from utils.bibliotheque_gui import supprimer_livre
from utils.emprunt_gui import emprunter_livre, rendre_livre
from utils.gestion_fichiers import lire_bibliotheque, lire_emprunts

# Global variables
fichier_bibliotheque = "data/bibliotheque.json"
fichier_emprunt = "data/emprunt.csv"
livres = lire_bibliotheque(fichier_bibliotheque)
personnes = lire_emprunts(fichier_emprunt)
root = tk.Tk()
result_text = None


def setup_main_window():
    """Configure et initialise la fenêtre principale de l'application avec les boutons et le texte de résultat."""
    global root, result_text
    root.title("Bibliothèque")
    root.geometry("1165x670")

    # Définir une police personnalisée pour les widgets
    custom_font = tkfont.Font(family="Helvetica", size=14)

    # Configurer le style pour les boutons
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.TButton", font=custom_font)
    style.configure("Custom.TCheckbutton", font=custom_font, padding=5, foreground="#000000", background="#f0f0f0")

    main_frame = ttk.Frame(root, padding="10")
    main_frame.grid(row=0, column=0)

    buttons = [
        ("Ajouter un livre", lambda: ajouter_livre(root, result_text, livres, fichier_bibliotheque)),
        ("Supprimer un livre", lambda: supprimer_livre(root, result_text, livres, fichier_bibliotheque)),
        ("Chercher un livre", lambda: rechercher_livre(root, result_text, livres)),
        ("Afficher les livres", lambda: afficher_livres(result_text, livres)),
        ("Emprunter un livre",
         lambda: emprunter_livre(root, result_text, livres, fichier_bibliotheque, personnes, fichier_emprunt)),
        ("Rendre un livre",
         lambda: rendre_livre(root, result_text, livres, fichier_bibliotheque, personnes, fichier_emprunt)),
        ("Quitter", root.quit)
    ]

    for i, (text, command) in enumerate(buttons):
        (ttk.Button(main_frame, text=text, command=command, style="Custom.TButton")
            .grid(row=0, column=i, padx=5, pady=5))

    result_text = tk.Text(main_frame, height=20, width=100, font=custom_font, spacing1=3, spacing3=3)
    result_text.grid(row=1, column=0, columnspan=30, pady=20)


# Run the application
setup_main_window()
root.mainloop()
