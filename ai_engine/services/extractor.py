import json
import re

from .config import client, MODEL
from .prompts import EXTRACTION_PROMPT
from .simple_extractor import simple_extract_profile

# ==========================================================
# STRUCTURE PAR DÉFAUT
# ==========================================================

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

# ==========================================================
# JSON PARSER
# ==========================================================

def safe_json_parse(text: str) -> dict:

    if not text:
        return DEFAULT_PROFILE.copy()

    try:
        data = json.loads(text)

    except Exception:

        match = re.search(r"\{[\s\S]*\}", text)

        if not match:
            return DEFAULT_PROFILE.copy()

        try:
            data = json.loads(match.group())

        except Exception:
            return DEFAULT_PROFILE.copy()

    result = DEFAULT_PROFILE.copy()

    if isinstance(data, dict):
        result.update(data)

    return result


# ==========================================================
# NORMALISATION
# ==========================================================

def normalize_result(profile):

    result = DEFAULT_PROFILE.copy()

    for key, value in profile.items():

        if value in ["", "null", "None", "Aucun", "aucun"]:
            value = None

        if isinstance(value, str):
            value = value.strip()

        result[key] = value

    # âge
    try:
        if result["age"] is not None:
            result["age"] = int(result["age"])
    except:
        result["age"] = None

    # budget
    if result["budget"] is not None:

        try:

            budget = str(result["budget"])

            budget = (
                budget.lower()
                .replace("fcfa", "")
                .replace("f cfa", "")
                .replace("$", "")
                .replace("€", "")
                .replace(",", "")
                .replace(" ", "")
            )

            result["budget"] = float(budget)

        except:
            result["budget"] = None

    # Majuscule de cohérence sur les champs catégoriels (l'IA peut renvoyer
    # "informatique" ou "Informatique" selon comment l'étudiant l'a tapé ;
    # le reste du système - récap, dashboard, FAQ - affiche ces champs en
    # partant du principe qu'ils commencent par une majuscule).
    for field in ["objective", "education_level", "current_field", "target_program", "nationality", "departure_date"]:
        value = result.get(field)
        if isinstance(value, str) and value and value[0].islower():
            result[field] = value[0].upper() + value[1:]

    return result


# ==========================================================
# EXTRACTION IA (avec fallback intelligent)
# ==========================================================

def extract_profile(message: str, last_question: str | None = None):
    """
    Extraction de profil à partir du message de l'étudiant.

    1. Essaie d'abord Groq (IA) avec EXTRACTION_PROMPT, pour comprendre le
       message quelle que soit sa formulation (langage naturel libre).
    2. Si Groq est indisponible (pas de clé API, rate limit, erreur réseau),
       bascule automatiquement sur l'extracteur léger basé sur des règles
       (simple_extract_profile), qui reste fiable pour les cas courants.
    """

    if not message:
        return DEFAULT_PROFILE.copy()

    if client is not None:
        try:
            response = client.chat.completions.create(
                model=MODEL,
                temperature=0,
                max_tokens=500,
                messages=[
                    {"role": "system", "content": EXTRACTION_PROMPT},
                    {
                        "role": "user",
                        "content": (
                            f"Dernière question posée par l'agent : {last_question or 'Aucune'}\n"
                            f"Message de l'étudiant : {message}"
                        ),
                    },
                ],
            )

            raw = response.choices[0].message.content
            result = normalize_result(safe_json_parse(raw))

            if any(value is not None for value in result.values()):
                return result

            # Appel Groq réussi (pas d'exception) mais réponse vide ou JSON
            # illisible : on retente quand même avec l'extracteur léger
            # plutôt que de perdre silencieusement l'information.
            print("⚠️ Groq a renvoyé un résultat vide/invalide - repli sur l'extracteur léger...")

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate_limit" in error_str.lower() or "tokens per day" in error_str.lower():
                print("⚠️ GROQ RATE LIMIT (extraction) - Basculage sur extracteur léger...")
            else:
                print(f"⚠️ Extractor error: {e}")

    # ================================================
    # FALLBACK (pas de clé API, erreur, ou rate limit)
    # ================================================
    return simple_extract_profile(message, last_question)