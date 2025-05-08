"""
    Module emprunts : gestion des emprunteurs

    Fonctions :
        • ajouter_personne
        • verifier_emprunts_en_cours
        • creer_emprunt
        • retours_possibles
        • selectionner_retour
        • creer_retour
        • modifier_personne (image ????)
"""
from datetime import date
from datetime import datetime
from datetime import timedelta


def ajouter_personne(personnes):
    """
    Recherche une personne existante dans la liste ou en crée une nouvelle.

    :param personnes: (list) Liste de dictionnaires représentant les personnes et leurs emprunts
    :return: (tuple)
        - (bool) True si la personne existe déjà, False sinon
        - (dict) Dictionnaire contenant les informations de la personne (existante ou nouvellement créée)
    """
    print('\n--- Nouvel emprunt ---')
    nom = input('Nom : ').strip()
    prenom = input('Prénom : ').strip()

    for personne in personnes:
        if nom == personne['nom'] and prenom == personne['prenom']:
            return True, personne

    personne = {
        "nom": nom,
        "prenom": prenom,
        "nbr_livres_empruntes": 0,
        "emprunts": {}
    }

    return False, personne


def verifier_emprunts_en_cours(personne):
    """
    Affiche un message pour avertir des emprunts déjà en cours.

    :param personne: (dict)
            Un dictionnaire contenant les informations sur la personne et ses éventuels emprunts en cours
    :return: (int) le nombre de livres non rendus
    """
    # Vérifier si des livres sont déjà empruntés (pas encore rendus)
    livres_non_rendus = []

    emprunts_dict = personne["emprunts"]
    for i, (num, emprunt) in enumerate(emprunts_dict.items(), 1):
        if not emprunt['date_retour']:
            livres_non_rendus.append(emprunt['titre'])

    match len(livres_non_rendus):
        case 0:
            print("\nPas d'emprunt en cours => 3 livres max !")
            return 0

        case 1:
            print("\nUn livre est déjà emprunté :")
            print(f"📗 {livres_non_rendus[0]}")
            print("=> 2 livres max !")
            return 1

        case 2:
            print("\nDeux livres sont déjà empruntés : ")
            for livre in livres_non_rendus:
                print(f"📚 {livre}")
            print("=> 1 livre max !")
            return 2

        case 3:
            print("\nTrois livres sont déjà empruntés :")
            for livre in livres_non_rendus:
                print(f"📚 {livre}")
            print("=> Pas de nouvel emprunt possible !")
            return 3


def creer_emprunt(personne, livres):
    """
    Emprunter des livres (en fonction du nombre de livres non rendus).

    :param personne: (dict) Informations sur la personne et ses emprunts
    :param livres: (dict) Dictionnaire contenant tous les livres de la bibliothèque
    :return: (dict) Personne mise à jour avec le nouvel emprunt
    """
    # Vérifier si la bibliothèque contient ce livre, ainsi que le nombre d'exemplaires disponibles
    while personne['nbr_livres_empruntes'] < 3:
        livre = input('\nTitre du livre : ').strip()
        livre_trouve = livres.get(livre, None)
        if not livre_trouve:
            print("Livre non trouvé !")
            continue
        if livre_trouve['Exemplaires'] == 0:
            print("Ce livre n'est pas disponible pour le moment !")
            continue

        # Ajouter le livre aux emprunts
        emprunt_id = str(max([int(k) for k in personne['emprunts'].keys()] + [0]) + 1)
        personne['emprunts'][emprunt_id] = {
            "titre": livre,
            "date_emprunt": date.today().strftime("%Y-%m-%d"),
            "date_retour": "",
        }

        # Décrémenter le nombre d'exemplaires
        livre_trouve['Exemplaires'] -= 1

        # Incrémenter le nombre de livres empruntés
        personne['nbr_livres_empruntes'] += 1

        # Recalculer nbr_livres_empruntes
        personne['nbr_livres_empruntes'] = sum(1 for emprunt in personne['emprunts'].values()
                                               if not emprunt["date_retour"])

        # Vérifier si un autre livre doit être emprunté
        if personne['nbr_livres_empruntes'] < 3:
            continuer = ''
            while not (continuer == 'o' or continuer == 'n'):
                continuer = input('\nEmprunter un autre livre (o/n) ? ').strip()
            if continuer == 'o':
                continue
            elif continuer == 'n':
                break
        else:
            break

    return personne


def retours_possibles(personnes):
    """
    Identifie les emprunts en cours pour une personne.

    :param personnes: (list) Liste des dictionnaires contenant les emprunts enregistrés
    :return: (list) liste de tous les emprunts en cours (livres non rendus)
    """
    print('\n--- Retour de livres ---')
    nom = input('Nom : ').strip()
    prenom = input('Prénom : ').strip()

    for personne in personnes:
        if nom == personne['nom'] and prenom == personne['prenom']:
            retours = [
                {"emprunt_id": num, **emprunt}
                for num, emprunt in personne['emprunts'].items()
                if not emprunt['date_retour']
            ]
            if not retours:
                print(f"Pas d'emprunt en cours trouvé pour {prenom} {nom} !")
                return [], personne
            return retours, personne

    print(f"Personne {prenom} {nom} non trouvée !")
    return [], {"nom": nom, "prenom": prenom}


def selectionner_retour(retours_eventuels):
    """
    Permet de sélectionner les emprunts à rendre parmi les emprunts en cours.

    :param retours_eventuels:  (list) liste de tous les emprunts en cours
    :return: (list) la liste des emprunts sélectionnés parmi les emprunts en cours
    """
    # Afficher les emprunts en cours afin de pouvoir choisir les retours
    print('\n--- Emprunts en cours ---')
    for i, retour in enumerate(retours_eventuels, 1):
        print(f"{i}. 📚 Emprunt en date du {retour['date_emprunt']} : {retour['titre']}")

    # S'il n'y a qu'un seul emprunt en cours, demander confirmation pour le retour
    if len(retours_eventuels) == 1:
        confirmation = ''
        while not (confirmation == 'o' or confirmation == 'n'):
            confirmation = input("\nConfirmer le retour (o/n) : ").strip()
        if confirmation == 'n':
            print("\nRetour annulé !")
            return []
        if confirmation == 'o':
            return retours_eventuels

    # Sélectionner le numéro de l'emprunt en cours dont on souhaite rendre les livres
    selection_numeros = []
    while True:
        selection_input = input("\nSélectionner un numéro d'emprunt : ").strip()

        if not selection_input.isdigit():
            print("Un nombre est attendu !")
            continue

        selection = int(selection_input)

        if not (0 < int(selection_input) <= len(retours_eventuels)):
            print(f"Invalide ! Entrer un nombre entre 1 et {len(retours_eventuels)}")
            continue

        if selection not in selection_numeros:
            selection_numeros.append(selection)
        else:
            print(f"Vous avez déjà sélectionné le numéro {selection} !")

        if len(selection_numeros) < len(retours_eventuels):
            continuer = ''
            while continuer != 'o' and continuer != 'n':
                continuer = input("Voulez-vous sélectionner un autre emprunt (o/n) ? ").strip()
            if continuer == 'o':
                continue
            if continuer == 'n':
                break
        else:
            break

    # Créer la liste des emprunts sélectionnés parmi les emprunts en cours
    retours_selectionnes = []
    for numero in selection_numeros:
        retours_selectionnes.append(retours_eventuels[numero - 1])

    return retours_selectionnes


def calculer_montant_total(emprunt, montant_total):
    """
    :param emprunt: (dict) dictionnaire contenant les informations concernant l'emprunt concerné (livres rendus)
    :param montant_total: (float) Montant total accumulé des pénalités avant cet emprunt.
    :return: (float) Montant total mis à jour après ajout de la pénalité de cet emprunt, si retard.
    """
    date_emprunt = datetime.strptime(emprunt['date_emprunt'], "%Y-%m-%d")
    date_retour_theorique = date_emprunt + timedelta(days=14)

    date_retour = datetime.strptime(emprunt['date_retour'], "%Y-%m-%d")

    montant_a_payer: float = 0
    jours_supplementaires = 0

    if date_retour > date_retour_theorique:
        jours_supplementaires = (date_retour - date_retour_theorique).days
        montant_a_payer += 0.10 * jours_supplementaires
        montant_total += montant_a_payer

    print(f"------------------------------------------------------"
          f"\n📚 Emprunt du {date_emprunt.strftime('%d/%m/%Y')} : {emprunt['titre']}")

    if not montant_a_payer:
        print(f"    Retour avant le {date_retour_theorique.strftime('%d/%m/%Y')} => rien à payer.")
    else:
        print(f"    {jours_supplementaires} jour(s) de retard "
              f"=> {"{:.2f}".format(0.10 * jours_supplementaires)}€ de pénalités")

    return montant_total


def creer_retour(retours_selectionnes, personnes, personne, livres):
    """
    Enregistre les retours en mettant à jour les dates de retour et les exemplaires.

    :param retours_selectionnes: (list) liste des emprunts en cours dont les livres vont être rendus
    :param personnes: (list) Liste des dictionnaires contenant les emprunts enregistrés
    :param personne: (dict) nom et prénom de la personne qui rapporte des livres
    :param livres: (dict) dictionnaire contenant tous les livres de la bibiliothèque
    :return: rien
    """
    montant_total = 0
    for retour in retours_selectionnes:
        for p in personnes:
            if p['nom'] == personne['nom'] and p['prenom'] == personne['prenom']:
                emprunts_dict = p['emprunts']
                emprunt_id = retour['emprunt_id']
                if emprunt_id in emprunts_dict and emprunts_dict[emprunt_id]['titre'] == retour['titre']:
                    # Ajouter la date de retour
                    emprunts_dict[emprunt_id]['date_retour'] = date.today().strftime("%Y-%m-%d")
                    # Calculer les pénalités si retard
                    montant_total = calculer_montant_total(emprunts_dict[emprunt_id], montant_total)
                    # Incrémenter le nombre d'exemplaires du livre rendu
                    livre = livres.get(emprunts_dict[emprunt_id]['titre'], None)
                    if livre:
                        livre['Exemplaires'] += 1
                    # Recalculer nbr_livres_empruntes
                    p['nbr_livres_empruntes'] = sum(1 for e in emprunts_dict.values() if not e['date_retour'])

    if montant_total and (len(retours_selectionnes) > 1):
        print(f"------------------------------------------------------"
              f"\n💶 Montant total à payer : {"{:.2f}".format(montant_total)}€.")


def modifier_personne():
    pass