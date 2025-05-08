"""
    Programme principal : menu interactif
"""

from utils.bibliotheque import afficher_livres, supprimer_livre
from utils.bibliotheque import ajouter_livre
from utils.bibliotheque import emprunter_livre
from utils.bibliotheque import menu
from utils.bibliotheque import rechercher_livre
from utils.bibliotheque import rendre_livre
from utils.bibliotheque import supprimer_livre

from utils.gestion_fichiers import lire_bibliotheque
from utils.gestion_fichiers import lire_emprunts


fichier_bibliotheque = "data/bibliotheque.json"
fichier_emprunt = "data/emprunt.csv"

livres = lire_bibliotheque(fichier_bibliotheque)
personnes = lire_emprunts(fichier_emprunt)

while True:
    choix = menu()

    match choix:

        case 1:
            ajouter_livre(livres, fichier_bibliotheque)

        case 2:
            supprimer_livre(livres, fichier_bibliotheque)

        case 3:
            rechercher_livre(livres)

        case 4:
            afficher_livres(livres)

        case 5:
            emprunter_livre(livres, fichier_bibliotheque, personnes, fichier_emprunt)

        case 6:
            rendre_livre(livres, fichier_bibliotheque, personnes, fichier_emprunt)

        case 7:
            print("\nÀ bientôt 👋")
            break
