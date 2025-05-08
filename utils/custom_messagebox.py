"""
    Box personnalisé pour les différents messages à afficher (info, succès, erreur)
"""
import os

import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk


def afficher_photo(msg_window, photo_id):
    """
    :param msg_window: Fenêtre Toplevel pour afficher la photo
    :param photo_id: Chaîne représentant le nom du fichier photo ou vide si aucune photo
    :return: Aucun
    """
    photo_label = ttk.Label(msg_window)
    photo_label.grid(row=1, column=0, columnspan=2, padx=50, pady=5)
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


def custom_messagebox(parent, title, message, font=("Helvetica", 14), geometry="550x150",
                      personne=None, parent_to_destroy=None):
    """
    :param parent: Fenêtre parente de l'application
    :param title: Chaîne représentant le titre de la boîte de message
    :param message: Chaîne représentant le texte à afficher
    :param font: Tuple représentant la police et la taille (défaut: ("Helvetica", 14))
    :param geometry: Chaîne représentant les dimensions de la fenêtre (défaut: "550x150")
    :param personne: Dictionnaire contenant les données de la personne (optionnel)
    :param parent_to_destroy: Fenêtre parente à détruire après fermeture (optionnel)
    :return: Aucun
    """
    msg_window = tk.Toplevel(parent)
    msg_window.title(title)
    msg_window.geometry(geometry)

    # Assurer que la fenêtre utilise la couleur de fond par défaut du système
    msg_window.configure(bg=msg_window.cget("bg"))

    # Créer un label avec un style personnalisé sans couleur de fond
    (ttk.Label(msg_window, text=message, font=font, wraplength=450, style="Custom.TLabel")
        .grid(row=0, column=0, padx=50, pady=20))

    if personne:
        afficher_photo(msg_window, personne["photo_id"])

    def on_ok():
        """Ferme la boîte de message et, si spécifié, détruit la fenêtre parente."""
        msg_window.destroy()
        if parent_to_destroy:
            parent_to_destroy.destroy()

    (ttk.Button(msg_window, text="OK", command=on_ok, style="Custom.TButton")
     .grid(row=2, column=0, padx=50, pady=20))

    # Centrer la fenêtre par rapport à la fenêtre parente
    msg_window.transient(parent)
    msg_window.grab_set()
    msg_window.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() - msg_window.winfo_width()) // 2
    y = parent.winfo_y() + (parent.winfo_height() - msg_window.winfo_height()) // 2
    msg_window.geometry(f"+{x}+{y}")
