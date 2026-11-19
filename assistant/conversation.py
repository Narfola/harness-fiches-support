"""Cœur de l’assistant : la conversation et la boucle des appels d’outil."""

from assistant import client, outils

CONSIGNES = """Tu es l’assistant de l’équipe support de Batifact, éditeur d’un logiciel de facturation pour artisans.
Réponds en français, brièvement, à partir des fiches de procédure, et cite la fiche utilisée.
Utilise lire_fiche pour consulter une fiche et ecrire_fiche pour enregistrer un brouillon de fiche.
Fiches disponibles : {fiches}"""


class LimiteAtteinte(Exception):
    """La question en cours s’arrête sur une limite fixée par l’équipe."""


def nouvelle_conversation(limites):
    """Renvoie la liste des messages d’une nouvelle conversation."""
    fiches = ", ".join(outils.lister_fiches(limites))
    # format remplace {fiches} dans CONSIGNES par la valeur donnée.
    return [{"role": "system", "content": CONSIGNES.format(fiches=fiches)}]


def joindre_fiche(nom, question, limites):
    """Renvoie la question suivie du contenu de la fiche jointe, ou lève AccesRefuse."""
    # À faire (étape 3).
    # raise NotImplementedError("Étape 3 : joindre_fiche")
    contenu = outils.lire_fiche(nom, limites)
    return f"Contenu de la fiche {nom} : \n{contenu}\n Question : {question}"


def poser(question, messages, service, modele, limites, confirmer, signaler):
    """Ajoute la question aux messages, exécute les appels d’outil et renvoie la réponse du modèle.

    confirmer(nom) renvoie True si l’utilisateur accepte d’écraser la fiche ;
    signaler(texte) affiche une opération ou un refus à l’utilisateur.
    """
    # À faire (étape 2) : envoyer la conversation avec client.envoyer et garder l’historique.
    # À faire (étape 3) : exécuter les appels d’outil du modèle jusqu’à sa réponse finale.
    nb_appels = 0
    limite_appels = limites["appels_outil_max"]
    messages.append({"role": "user", "content": question})
    while True:
        reponse = client.envoyer(service, modele, messages)
        reponse_message = reponse.choices[0].message
        messages.append({"role": "assistant", "content": reponse_message.content})

        if not reponse_message.tool_calls:
            return reponse_message.content

        nb_appels += len(reponse_message.tool_calls)

        if nb_appels > limite_appels:
            return "La limite d'appels d'outils pour cette conversation a été atteinte."

        for tool_call in reponse_message.tool_calls:

            try:
                resultat = outils.executer(tool_call, limites, confirmer)
            except outils.AccesRefuse as erreur:
                resultat = f"Erreur : {erreur}"
            except Exception as erreur:
                resultat = f"Erreur inattendue : {erreur}"

            messages.append(
                {"role": "tool", "tool_call_id": tool_call.id, "content": resultat}
            )

    # À faire (étape 4) : arrêter la question au-delà des limites.
    # raise NotImplementedError("Étape 2 : poser")
    return contenu_reponse
