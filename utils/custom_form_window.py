"""
    Création de formulaire
"""
import tkinter as tk


def custom_form_window(parent, title, geometry):
    """
    :param parent: Fenêtre parente de l'application
    :param title: Chaîne représentant le titre de la fenêtre
    :param geometry: Chaîne représentant les dimensions de la fenêtre (ex: "600x300")
    :return: Fenêtre Toplevel créée
    """
    form_window = tk.Toplevel(parent)
    form_window.title(title)
    form_window.geometry(geometry)

    # Centrer la fenêtre par rapport à la fenêtre parente
    form_window.transient(parent)
    form_window.grab_set()
    form_window.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() - form_window.winfo_width()) // 2
    y = parent.winfo_y() + (parent.winfo_height() - form_window.winfo_height()) // 2
    form_window.geometry(f"+{x}+{y}")

    return form_window
