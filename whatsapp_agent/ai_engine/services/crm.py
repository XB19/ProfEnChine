from ai_engine.services.extractor import extract_profile
from ai_engine.scoring import calculate_ai_score
from ai_engine.status import determine_status


def parse_passport(value):

    if value is None:
        return None

    if isinstance(value, bool):
        return "Oui" if value else "Non"

    text = str(value).strip().lower()

    if text in ["oui", "yes", "y", "ok", "true", "vrai"]:
        return "Oui"

    if text in ["non", "no", "n", "nop", "false", "faux"]:
        return "Non"

    if "pas de passeport" in text or "pas encore" in text or "n'ai" in text:
        return "Non"

    if "valide jusqu" in text or "valide" in text or "j'ai" in text:
        return "Oui"

    return None


# ==========================================================
# HELPERS
# ==========================================================

def is_empty(value):
    """
    Vérifie si une valeur est vide ou invalide.
    """
    return value in (None, "", [], {}, "null")


def update_if_empty(prospect, field, value):
    """
    Met à jour uniquement si :
    - la nouvelle valeur est valide
    - le champ est encore vide
    """
    if not is_empty(value) and is_empty(getattr(prospect, field, None)):
        setattr(prospect, field, value)
        return True
    return False


# ==========================================================
# MAIN CRM UPDATE
# ==========================================================

def update_prospect_profile(prospect, user_message):
    """
    Met à jour automatiquement le profil prospect
    à partir de l'IA (extractor Groq / Llama).

    Retourne :
        list[str] updated_fields
    """

    updated_fields = []

    try:
        # ==================================================
        # DERNIÈRE QUESTION POSÉE PAR L'IA
        # ==================================================
        last_ai = (
            prospect.conversations
            .filter(role="assistant")
            .order_by("-id")
            .first()
        )

        last_question = last_ai.message if last_ai else None

        # ==================================================
        # EXTRACTION IA
        # ==================================================
        extracted = extract_profile(
            message=user_message,
            last_question=last_question
        )

        if not isinstance(extracted, dict):
            return []

        # ==================================================
        # CORRECTION CONTEXTE QUESTION / CHAMP
        # ==================================================
        if last_question and "domaine" in last_question.lower():
            if extracted.get("current_field") is None and extracted.get("target_program") is not None:
                extracted["current_field"] = extracted.get("target_program")
                extracted["target_program"] = None

        if last_question and "programme" in last_question.lower():
            if extracted.get("target_program") is None and extracted.get("current_field") is not None:
                extracted["target_program"] = extracted.get("current_field")
                extracted["current_field"] = None

        # ==================================================
        # CHAMPS TEXTES - TOUS LES CHAMPS
        # ==================================================
        if update_if_empty(prospect, "full_name", extracted.get("full_name")):
            updated_fields.append("full_name")

        if update_if_empty(prospect, "objective", extracted.get("objective")):
            updated_fields.append("objective")

        if update_if_empty(prospect, "nationality", extracted.get("nationality")):
            updated_fields.append("nationality")

        if update_if_empty(prospect, "education_level", extracted.get("education_level")):
            updated_fields.append("education_level")

        if update_if_empty(prospect, "current_field", extracted.get("current_field")):
            updated_fields.append("current_field")

        if update_if_empty(prospect, "target_program", extracted.get("target_program")):
            updated_fields.append("target_program")

        if update_if_empty(prospect, "departure_date", extracted.get("departure_date")):
            updated_fields.append("departure_date")

        if prospect.criminal_record is None and extracted.get("criminal_record") is not None:
            prospect.criminal_record = str(extracted.get("criminal_record")).strip()
            updated_fields.append("criminal_record")

        if update_if_empty(prospect, "in_whatsapp_group", extracted.get("in_whatsapp_group")):
            updated_fields.append("in_whatsapp_group")

        # ==================================================
        # AGE (validation stricte)
        # ==================================================
        if prospect.age is None:
            try:
                age = extracted.get("age")
                if age is not None:
                    age = int(age)
                    if 10 <= age <= 100:
                        prospect.age = age
                        updated_fields.append("age")
            except (ValueError, TypeError):
                pass

        # ==================================================
        # BUDGET
        # ==================================================
        if prospect.budget is None:
            try:
                budget = extracted.get("budget")
                if budget is not None:
                    prospect.budget = float(budget)
                    updated_fields.append("budget")
            except (ValueError, TypeError):
                pass

        # ==================================================
        # PASSEPORT (bool strict)
        # ==================================================
        if prospect.passport is None:

            raw_passport = extracted.get("passport")
            parsed_passport = parse_passport(raw_passport)

            if parsed_passport is not None:
                prospect.passport = parsed_passport
                updated_fields.append("passport")

        # ==================================================
        # SCORE IA + STATUS
        # ==================================================
        try:
            prospect.ai_score = calculate_ai_score(prospect)
            prospect.status = determine_status(prospect.ai_score)
        except Exception as e:
            print("❌ SCORING ERROR:", e)

        # ==================================================
        # DOSSIER COMPLET
        # ==================================================
        required_fields = [
            prospect.full_name,
            prospect.age,
            prospect.nationality,
            prospect.education_level,
            prospect.current_field,
            prospect.target_program,
        ]

        prospect.dossier_complet = (
            all(required_fields)
            and prospect.budget is not None
            and prospect.passport is not None
        )

        def clean(value):
            if isinstance(value, str):
                value = value.strip()
            return value
        
        if extracted.get("target_program") is not None:
            prospect.target_program = clean(extracted.get("target_program"))

        # ==================================================
        # SAVE
        # ==================================================
        prospect.save()

        return updated_fields

    except Exception as e:
        print("❌ CRM UPDATE ERROR:", e)
        return []
    

