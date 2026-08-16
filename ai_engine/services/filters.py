"""
FILTRES & VALIDATION DES MESSAGES
Valide les messages, détecte spam, contenu inapproprié, hors contexte, etc.
"""

import re


def normalize(text):
    """Normalise le texte"""
    return re.sub(
        r"[^\w\s]",
        " ",
        text.lower()
    ).strip()


# ==========================================================
# MESSAGES INVALIDES (SPAM, INSULTES, etc.)
# ==========================================================

BLACKLIST_KEYWORDS = [
    "hack", "drug", "arme", "weapon", "terror", "fake passport",
    "bitcoin", "crypto", "money", "argent rapide",
    "escort", "adult", "xxx",
]

def is_invalid_message(text):
    """
    Vérifie si le message contient du contenu bloqué.
    """
    if not text:
        return True
    
    msg_lower = text.lower().strip()
    
    # Trop court
    if len(msg_lower) < 2:
        return True
    
    # Mots-clés bloqués
    return any(
        word in msg_lower
        for word in BLACKLIST_KEYWORDS
    )


# ==========================================================
# DÉTECTION : MESSAGE HORS CONTEXTE
# ==========================================================

CHINA_STUDY_KEYWORDS = [
    "chine", "china", "chinois", "étude", "study", "études",
    "université", "universite", "bourse", "visa", "admission",
    "licence", "master", "doctorat", "programme", "program",
    "profil", "dossier", "candidature", "application",
    "école", "ecole", "formation", "cours", "diplôme", "diplome",
    "professeur", "prof", "enseignement", "pédagogique", "academique",
    "budget", "frais", "coût", "cout", "prix", "scolarité", "scolarite",
    "passeport", "document", "traduction", "certification",
    "admissions", "université", "etudes", "etudie", "etudier",
]

def is_off_topic(message: str) -> bool:
    """
    Détecte si le message est hors du contexte "études en Chine".
    Retourne True si hors sujet.
    """
    if not message:
        return False
    
    msg_lower = message.lower().strip()
    
    # Messages courts = probablement des réponses simples
    if len(msg_lower.split()) <= 3:
        return False
    
    # Vérifier s'il y a des keywords du contexte
    has_context_keyword = any(
        keyword in msg_lower for keyword in CHINA_STUDY_KEYWORDS
    )
    
    # Si c'est une question ET aucun keyword = hors sujet
    has_question_mark = "?" in msg_lower
    
    if has_question_mark and not has_context_keyword:
        return True
    
    return False


def get_off_topic_message():
    """Retourne le message standard pour hors contexte."""
    return (
        "📌 **Je suis l'agent IA \"Prof en Chine\", spécialisé uniquement dans les études en Chine.**\n\n"
        "Je peux vous aider avec :\n"
        "✅ Les programmes d'études (Licence, Master, Doctorat, Année de langue)\n"
        "✅ Les bourses et financement\n"
        "✅ Les conditions d'admission\n"
        "✅ Les frais, budgets et coûts\n"
        "✅ Les visas et procédures\n"
        "✅ Les universités chinoises\n\n"
        "**Posez-moi une question sur l'étude en Chine !** 😊"
    )
