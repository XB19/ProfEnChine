"""
SIMPLE EXTRACTOR - FALLBACK LÉGER
Extracteur basé sur regex pour quand Groq est indisponible (rate limit, etc.)
Extraction rapide et fiable pour les patterns simples.
"""

import re
import json


# ==========================================================
# PATTERNS REGEX
# ==========================================================

PATTERNS = {
    "objective": [
        r"(immigr|étud|les deux)",
    ],
    "nationality": [
        r"(?:je\s+(?:suis|viens)\s+)?(?:du\s+)?(\w+(?:\s+\w+)?)",  # Je suis/viens du Togo
        r"(?:je\s+suis\s+)?(\w+ois|ienne|ien|ienne)(?:\s|$)",  # togolais, béninois, etc.
    ],
    "age": [
        r"(?:j[\'a]i\s+)?(\d{1,2})\s*(?:ans?)?(?:\s|$|\.)",
        r"(\d{1,2})\s*(?:ans?)?(?:\s|\.)",
    ],
    "education_level": [
        r"(?:bac|lycée|licence|master|doctorat|école)",
    ],
    "budget": [
        r"(\d+(?:\s*(?:millions?|m|000\s*000|€|euros?|dollars?|fcfa|k))?)",
    ],
    "passport": [
        r"(?:j[\'a]i\s+)?(?:un\s+)?passeport",
        r"(?:valide|expir|jusqu)",
        r"(?:pas\s+(?:encore|de))",
    ],
    "criminal_record": [
        r"(?:casier|judiciaire|vierge)",
    ],
    "departure_date": [
        r"(septembre|mars|2026|2027|2028)",
    ],
    "in_whatsapp_group": [
        r"(?:whatsapp|groupe|group)",
    ],
}


def simple_extract_profile(message: str, last_question: str = None) -> dict:
    """
    Extraction simple basée sur regex.
    Rapide, pas d'IA, moins puissant mais fonctionne quand Groq rate-limit.
    """
    
    DEFAULT_PROFILE = {
        "full_name": None,
        "objective": None,
        "age": None,
        "nationality": None,
        "education_level": None,
        "current_field": None,
        "target_program": None,
        "budget": None,
        "passport": None,
        "criminal_record": None,
        "departure_date": None,
        "in_whatsapp_group": None,
    }

    msg_lower = message.lower().strip()
    msg_original = message.strip()
    
    # ================================================
    # FULL NAME (si dernière question était sur le nom)
    # ================================================
    if last_question and "nom complet" in last_question.lower():
        # Prendre la réponse comme nom complet si elle n'est pas un pattern spécial
        # (normalisation des accents : "etudier" sans accent doit être exclu comme "étudier")
        msg_no_accent = msg_lower.replace("é", "e").replace("è", "e").replace("ê", "e")
        is_special_pattern = any(
            keyword in msg_no_accent
            for keyword in ["immigr", "etudi", "oui", "non", "yes", "no"]
        )
        # Un nom complet fait rarement plus de 4 mots
        is_plausible_name_length = len(msg_original.split()) <= 4
        if not is_special_pattern and is_plausible_name_length:
            # Si c'est juste des lettres/espaces, c'est probablement un nom
            if re.match(r"^[a-zàâäçèéêëîïôùûüœæ\s'-]+$", msg_lower, re.IGNORECASE):
                DEFAULT_PROFILE["full_name"] = msg_original
    
    # ================================================
    # OBJECTIVE (Immigrer / Étudier / Les deux)
    # ================================================
    # Normaliser les accents pour la détection
    msg_normalized = msg_lower.replace("é", "e").replace("è", "e").replace("ê", "e")
    
    if "les deux" in msg_lower or ("immigr" in msg_lower and ("etudi" in msg_normalized or "étudi" in msg_lower)):
        DEFAULT_PROFILE["objective"] = "Les deux"
    elif "immigr" in msg_lower:
        DEFAULT_PROFILE["objective"] = "Immigrer"
    elif "etudi" in msg_normalized or "étudi" in msg_lower or "etud" in msg_normalized or "étud" in msg_lower:
        DEFAULT_PROFILE["objective"] = "Étudier"
    
    # ================================================
    # AGE
    # ================================================
    age_match = re.search(r"(\d{1,2})\s*(?:ans?)?", msg_lower)
    if age_match:
        try:
            age = int(age_match.group(1))
            if 10 <= age <= 100:
                DEFAULT_PROFILE["age"] = age
        except ValueError:
            pass
    
    # ================================================
    # NATIONALITY
    # ================================================
    nationality_map = {
        "togo": "Togo",
        "togolai": "Togo",
        "benin": "Bénin",
        "beninoi": "Bénin",
        "cameroun": "Cameroun",
        "camerounai": "Cameroun",
        "côte": "Côte d'Ivoire",
        "ivoire": "Côte d'Ivoire",
        "ivoirien": "Côte d'Ivoire",
        "burkina": "Burkina Faso",
        "burkinabè": "Burkina Faso",
        "senegal": "Sénégal",
        "senegalai": "Sénégal",
        "congo": "Congo",
        "congolai": "Congo",
        "gabon": "Gabon",
        "gabonai": "Gabon",
        "ghana": "Ghana",
        "ghaneen": "Ghana",
        "mali": "Mali",
        "malien": "Mali",
        "niger": "Niger",
        "nigerien": "Niger",
        "guinee": "Guinée",
        "guineen": "Guinée",
    }
    
    for pattern, country in nationality_map.items():
        if pattern in msg_lower:
            DEFAULT_PROFILE["nationality"] = country
            break
    
    # ================================================
    # EDUCATION LEVEL (Bac, Licence, Master)
    # ================================================
    education_map = {
        "bac": "Bac",
        "lycée": "Lycée",
        "licence": "Licence",
        "master": "Master",
        "doctorat": "Doctorat",
        "bachelor": "Licence",
        "deug": "Licence",
    }
    
    for pattern, level in education_map.items():
        if pattern in msg_lower:
            DEFAULT_PROFILE["education_level"] = level
            break
    
    # ================================================
    # CURRENT FIELD / FILIÈRE (si last_question parle de filière)
    # ================================================
    if last_question and ("filière" in last_question.lower() or "domaine" in last_question.lower()):
        # Extraire le domaine principal de la message
        domain_keywords = {
            "informatique": "Informatique",
            "médecine": "Médecine",
            "commerce": "Commerce",
            "architecture": "Architecture",
            "droit": "Droit",
            "gestion": "Gestion",
            "marketing": "Marketing",
            "finance": "Finance",
            "ingénierie": "Ingénierie",
            "design": "Design",
            "mécanique": "Mécanique",
            "électricité": "Électricité",
            "biologie": "Biologie",
            "chimie": "Chimie",
            "physique": "Physique",
            "mathématiques": "Mathématiques",
            "géologie": "Géologie",
            "agriculture": "Agriculture",
            "agronomie": "Agronomie",
            "pharmacie": "Pharmacie",
            "infirmier": "Infirmerie",
            "communication": "Communication",
            "journalisme": "Journalisme",
            "arts": "Arts",
            "musique": "Musique",
            "langue chinoise": "Langue chinoise",
            "langues": "Langues",
            "chinois": "Langue chinoise",
            "tourisme": "Tourisme",
            "hôtellerie": "Hôtellerie",
            "sport": "Sport",
            "éducation": "Éducation",
            "pédagogie": "Pédagogie",
            "psychologie": "Psychologie",
            "sociologie": "Sociologie",
            "anthropologie": "Anthropologie",
            "histoire": "Histoire",
            "géographie": "Géographie",
            "économie": "Économie",
            "comptabilité": "Comptabilité",
            "audit": "Audit",
            "ressources humaines": "Ressources Humaines",
            "rh": "Ressources Humaines",
            "gestion de projet": "Gestion de Projet",
            "genie civil": "Génie Civil",
            "génie logiciel": "Génie Logiciel",
            "cybersécurité": "Cybersécurité",
            "ia": "Intelligence Artificielle",
            "intelligence artificielle": "Intelligence Artificielle",
            "data science": "Data Science",
            "électronique": "Électronique",
            "télécommunications": "Télécommunications",
            "aviation": "Aviation",
            "transport": "Transport",
            "logistique": "Logistique",
            "environnement": "Environnement",
            "écologie": "Écologie",
        }
        
        for keyword, domain in domain_keywords.items():
            if keyword in msg_lower:
                DEFAULT_PROFILE["current_field"] = domain
                break
        
        # Si aucun keyword trouvé et message court, garder la réponse brute
        if not DEFAULT_PROFILE["current_field"] and len(message.split()) <= 5:
            # Prendre le dernier mot ou groupe de mots
            words = message.strip().split()
            DEFAULT_PROFILE["current_field"] = " ".join(words[-2:] if len(words) > 1 else words).capitalize()
    
    # ================================================
    # TARGET PROGRAM (si last_question parle de niveau)
    # ================================================
    if last_question and ("niveau d'étud" in last_question.lower() and "actuel" not in last_question.lower()):
        program_map = {
            "licence": "Licence",
            "master": "Master",
            "doctorat": "Doctorat",
            "langue": "Année de langue",
            "language": "Année de langue",
            "chinois": "Année de langue",
        }
        for pattern, prog in program_map.items():
            if pattern in msg_lower:
                DEFAULT_PROFILE["target_program"] = prog
                break
        
        # Si rien trouvé mais réponse courte, garder la réponse brute
        if not DEFAULT_PROFILE["target_program"] and len(message.split()) <= 5:
            DEFAULT_PROFILE["target_program"] = message.strip().capitalize()
    
    # ================================================
    # BUDGET
    # ================================================
    budget_patterns = [
        (r"(\d+)\s*millions?", 1000000),
        (r"(\d+)\s*m(?:illions)?(?:\s|$)", 1000000),
        (r"(\d+)\s*k(?:illos)?", 1000),
        (r"(\d+)\s*euros?", 1),  # Direct conversion EUR (very rough)
        (r"(\d+)\s*dollars?", 600),  # Very rough USD to FCFA
        (r"(\d+)(?:000\s*000|\s*millions?)?", 1),
    ]
    
    for pattern, multiplier in budget_patterns:
        match = re.search(pattern, msg_lower, re.IGNORECASE)
        if match:
            try:
                number = int(match.group(1))
                budget = number * multiplier
                if 100000 <= budget <= 100000000:  # Sanity check
                    DEFAULT_PROFILE["budget"] = budget
                    break
            except ValueError:
                continue
    
    # ================================================
    # PASSPORT (Oui / Non / Date)
    # ================================================
    if "passeport" in msg_lower or "passport" in msg_lower or (last_question and "passeport" in last_question.lower()):
        if "non" in msg_lower or "pas" in msg_lower or "n'" in msg_lower or "nop" in msg_lower:
            DEFAULT_PROFILE["passport"] = "Non"
        elif "oui" in msg_lower or "j'" in msg_lower or "j ai" in msg_lower or "valide" in msg_lower or "jusqu" in msg_lower:
            # Extraire la date si présente
            date_match_passport = re.search(r"(202[0-9]|20[2-9][0-9])", msg_lower)
            if date_match_passport:
                year = date_match_passport.group(1)
                DEFAULT_PROFILE["passport"] = f"Oui, valide jusqu'en {year}"
            else:
                DEFAULT_PROFILE["passport"] = "Oui"
    
    # ================================================
    # CRIMINAL RECORD (Oui / Non)
    # ================================================
    if "casier" in msg_lower or "judiciaire" in msg_lower or (last_question and "casier" in last_question.lower()):
        if "vierge" in msg_lower or "non" in msg_lower or "n'" in msg_lower or "nop" in msg_lower:
            DEFAULT_PROFILE["criminal_record"] = "Non"
        elif "oui" in msg_lower or "j'" in msg_lower or "j ai" in msg_lower or "j ai un" in msg_lower:
            DEFAULT_PROFILE["criminal_record"] = "Oui"
    
    # ================================================
    # DEPARTURE DATE
    # ================================================
    date_match = re.search(r"(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre|jan|fév|mar|avr|mai|juin|juil|aoû|sep|oct|nov|déc)\s+(202[0-9]|20[2-9][0-9])", msg_lower)
    if date_match:
        month_str = date_match.group(1).lower()
        year_str = date_match.group(2)
        
        month_map = {
            "janvier": "Janvier", "jan": "Janvier",
            "février": "Février", "fév": "Février",
            "mars": "Mars", "mar": "Mars",
            "avril": "Avril", "avr": "Avril",
            "mai": "Mai",
            "juin": "Juin",
            "juillet": "Juillet", "juil": "Juillet",
            "août": "Août", "aoû": "Août",
            "septembre": "Septembre", "sep": "Septembre",
            "octobre": "Octobre", "oct": "Octobre",
            "novembre": "Novembre", "nov": "Novembre",
            "décembre": "Décembre", "déc": "Décembre",
        }
        month = month_map.get(month_str, month_str.capitalize())
        DEFAULT_PROFILE["departure_date"] = f"{month} {year_str}"
    else:
        # Fallback: chercher juste le mois
        if "septembre" in msg_lower or "sep" in msg_lower:
            if "2027" in msg_lower:
                DEFAULT_PROFILE["departure_date"] = "Septembre 2027"
            else:
                DEFAULT_PROFILE["departure_date"] = "Septembre 2026"
        elif "mars" in msg_lower:
            if "2026" in msg_lower:
                DEFAULT_PROFILE["departure_date"] = "Mars 2026"
            else:
                DEFAULT_PROFILE["departure_date"] = "Mars 2027"
    
    # ================================================
    # WHATSAPP GROUP
    # ================================================
    if "whatsapp" in msg_lower or "groupe" in msg_lower or "group" in msg_lower:
        if "non" in msg_lower or "pas" in msg_lower or "n'" in msg_lower or "pas encore" in msg_lower:
            DEFAULT_PROFILE["in_whatsapp_group"] = "Non"
        elif "oui" in msg_lower or "suis" in msg_lower or "dans" in msg_lower or "j'" in msg_lower:
            DEFAULT_PROFILE["in_whatsapp_group"] = "Oui"
    # Aussi accepter les réponses courtes oui/non sans contexte whatsapp
    elif last_question and "whatsapp" in last_question.lower():
        if "non" in msg_lower or "nop" in msg_lower or "pas" in msg_lower:
            DEFAULT_PROFILE["in_whatsapp_group"] = "Non"
        elif "oui" in msg_lower or "ouais" in msg_lower or "yes" in msg_lower:
            DEFAULT_PROFILE["in_whatsapp_group"] = "Oui"
    
    return DEFAULT_PROFILE
