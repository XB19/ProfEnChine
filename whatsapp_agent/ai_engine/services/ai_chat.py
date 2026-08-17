from conversations.models import Conversation

from .filters import is_invalid_message
from .crm import update_prospect_profile
from .conversation import get_next_question
from .prompts import SYSTEM_PROMPT, KNOWLEDGE_PROMPT
from .knowledge_base import (
    get_faq_answer,
    detect_intent,
    get_program_info,
    get_budget_recommendation,
    OBJECTION_RESPONSES,
    FINAL_SUBMISSION_DOCUMENTS,
)
from .config import client as groq_client, MODEL


# ==========================================================
# RÉPONDRE AUX QUESTIONS GÉNÉRALES - INTELLIGENT
# ==========================================================

def _is_positive_consent(message: str) -> bool:
    normalized = message.lower()
    positives = [
        "oui", "d'accord", "daccord", "ok", "bien sûr", "je suis prêt", "je suis prete", "je veux", "je souhaite", "c'est bon", "cest bon"
    ]
    return any(keyword in normalized for keyword in positives) and "non" not in normalized


def _is_negative_consent(message: str) -> bool:
    normalized = message.lower()
    negatives = [
        "non", "pas maintenant", "pas encore", "je ne souhaite pas", "je ne veux pas", "plus tard", "pas tout de suite"
    ]
    return any(keyword in normalized for keyword in negatives)


def answer_general_question(question: str) -> str:
    """
    Répond intelligemment aux questions générales sur les études en Chine.
    
    Stratégie :
    1. D'abord vérifier FAQ (réponses pré-préparées)
    2. Si pas dans FAQ, utiliser Groq/Claude
    3. En cas de rate limit, continue sans interruption
    4. Toujours garder les réponses concises et pertinentes
    """
    
    if not question:
        return ""

    question_lower = question.lower().strip()

    # ================================================
    # ESSAI 1: FAQ (RÉPONSES PRÉ-PRÉPARÉES)
    # ================================================
    faq_answer = get_faq_answer(question)
    if faq_answer:
        print(f"✅ Réponse FAQ trouvée")
        return faq_answer

    # ================================================
    # ESSAI 2: OBJECTIONS COURANTES
    # ================================================
    for objection_key, objection_data in OBJECTION_RESPONSES.items():
        if objection_data["objection"].lower() in question_lower:
            print(f"✅ Objection {objection_key} détectée")
            return objection_data["response"]

    # ================================================
    # ESSAI 3: GROQ/CLAUDE (IA INTELLIGENTE)
    # ================================================
    if not groq_client:
        return ""

    try:
        # KNOWLEDGE_PROMPT contient toute la base de connaissance officielle,
        # y compris la règle critique interdisant de citer des universités
        # chinoises précises. Ne jamais répondre avec un prompt "maison" à
        # côté qui n'aurait pas cette contrainte.
        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": KNOWLEDGE_PROMPT,
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7,
            max_tokens=300,
        )
        
        answer = response.choices[0].message.content.strip()
        print(f"✅ Réponse Groq générée")
        return answer
    
    except Exception as e:
        error_str = str(e)
        
        # Rate limit - continue sans répondre
        if "429" in error_str or "rate_limit" in error_str.lower():
            print(f"⚠️ GROQ RATE LIMIT (Q&A) - Continuons la qualification...")
            return ""
        
        # Autres erreurs - log et continue
        print(f"⚠️ Error answering question: {e}")
        return ""


# ==========================================================
# DETECT QUESTION TYPE - AMÉLIORÉ
# ===========================================================

def is_user_asking_question(message: str) -> bool:
    """
    Détecte si l'utilisateur pose une question générale 
    (vs répond à une question de qualification).
    
    Amélioré pour distinguer:
    - Questions générales (répondre en dehors de la qualification)
    - Réponses à des questions de qualification
    """
    msg_lower = message.lower().strip()
    
    # ================================================
    # 1️⃣ DÉTECTION PAR PONCTUATION
    # ================================================
    has_question_mark = "?" in msg_lower
    
    # ================================================
    # 2️⃣ MOTS-CLÉS DE QUESTIONS
    # ================================================
    question_markers = [
        # Comment/Pourquoi/Quel
        "comment", "pourquoi", "quoi", "quel", "quelle", "quels", "quelles",
        
        # Où/Quand/Combien
        "où", "quand", "combien", 
        
        # Coûts/Budget
        "ça coûte", "prix", "budget", "frais", "tarif",
        
        # Universités
        "université", "universités", "école", "écoles", "programme",
        "meilleure", "recommande", "conseil", "avis",
        
        # Bourses/Financement
        "bourse", "gratuit", "financement", "aide financière",
        
        # Procédure
        "visa", "documents", "procédure", "processus", "sélection", "admission",
        "conditions", "durée", "combien de temps",
        
        # Vie/Logement
        "vie", "logement", "dortoir", "expatrié", "expatriés", "coût de la vie",
        "logement", "travail", "job", "part-time",
        
        # Général
        "c'est quoi", "c'est comment", "peut", "puis-je", "comment ça marche"
    ]
    
    has_question_word = any(word in msg_lower for word in question_markers)
    
    # ================================================
    # 3️⃣ DÉTECTION D'INTENTIONS
    # ================================================
    intent = detect_intent(message)
    
    # ================================================
    # 4️⃣ EXCLUSIONS (cas de réponses courtes)
    # ================================================
    # Court réponse qui ne semble pas être une question
    is_short_simple_answer = len(msg_lower.split()) <= 3 and not has_question_mark
    
    # Réponses courtes typiques à des questions de qualification
    typical_answers = [
        "oui", "non", "peut-être", "j'ai", "je suis", "je viens", "de", "du",
        "c'est", "informatique", "médecine", "commerce", "licence", "master",
        "doctorat", "togo", "bénin", "cameroun", "2026", "2027",
        "septembre", "mars", "immigrer", "étudier", "les deux", "aucun", "rien", "pas",
        "année de langue", "année", "langue", "vierge", "valide"
    ]
    
    is_typical_answer = any(msg_lower.startswith(ans) for ans in typical_answers)
    
    # ================================================
    # DÉCISION FINALE
    # ================================================
    # C'est une question si:
    # 1. Contient un "?" OU
    # 2. A des mots-clés de question ET c'est pas une réponse typique courte
    # 3. OU intent détecté (comme bourse, coûts, etc.)
    
    is_question = (
        has_question_mark or 
        (has_question_word and not (is_short_simple_answer and is_typical_answer)) or
        (intent is not None and intent not in ["ask_general"])  # Intent actionnable
    )
    
    return is_question


# ==========================================================
# LIBELLÉS UTILISÉS POUR LES MESSAGES
# ==========================================================

FIELD_LABELS = {
    "full_name": "votre nom complet",
    "objective": "votre objectif",
    "age": "votre âge",
    "nationality": "votre nationalité",
    "education_level": "votre niveau d'étude",
    "current_field": "votre filière souhaitée",
    "target_program": "votre niveau d'études souhaité",
    "budget": "votre budget",
    "passport": "votre statut passeport",
    "criminal_record": "votre statut casier judiciaire",
    "departure_date": "votre date de départ souhaitée",
    "in_whatsapp_group": "votre statut groupe WhatsApp",
}


def build_orientation_message(prospect):
    profile_parts = []

    if prospect.education_level:
        profile_parts.append(f"niveau {prospect.education_level}")

    if prospect.current_field:
        profile_parts.append(f"domaine {prospect.current_field}")

    if prospect.target_program:
        profile_parts.append(f"projet {prospect.target_program}")

    if prospect.budget is not None:
        profile_parts.append(f"budget {int(float(prospect.budget)):,} FCFA")

    profile_summary = ", ".join(profile_parts) if profile_parts else "un profil encore en cours de qualification"

    if prospect.target_program:
        focus = prospect.target_program
    elif prospect.current_field:
        focus = prospect.current_field
    else:
        focus = "votre domaine d'études"

    return (
        "🧭 Orientation intelligente : d’après votre profil, "
        f"nous allons orienter votre parcours vers des options cohérentes pour {focus}. "
        f"Le détail de votre profil ({profile_summary}) permettra de choisir les programmes et les établissements les plus adaptés. "
        "Les universités seront retenues en fonction de votre profil, de votre niveau académique et de votre budget."
    )


# ==========================================================
# MAIN AI
# ==========================================================

def ask_ai(phone_number, prospect, user_message):

    try:

        if is_invalid_message(user_message):
            return "Désolé, je ne peux pas traiter ce type de demande."

        # NOTE : il n'y a plus de blocage "hors sujet" par mots-clés ici.
        # L'ancien filtre bloquait toute question de plus de 3 mots ne
        # contenant aucun mot-clé précis (ex: "Je peux vous poser une
        # question ?"), avant même que l'IA ne la voie. C'est maintenant
        # KNOWLEDGE_PROMPT qui indique à l'IA de recadrer poliment une
        # question réellement hors sujet, avec un vrai jugement contextuel
        # plutôt qu'une liste de mots-clés.

        prospect.last_answer = user_message
        prospect.save(update_fields=["last_answer"])

        # ==================================================
        # CONSENT STEP FOR FIRST-TIME USERS
        # ==================================================
        if prospect.current_step == "consent":
            if _is_positive_consent(user_message):
                prospect.current_step = None
                prospect.save(update_fields=["current_step"])

                reply = (
                    "Merci pour votre accord.\n\n"
                    "Je vais maintenant vous poser quelques questions pour démarrer votre préinscription.\n\n"
                    "Commençons par :\n\n"
                    f"{get_next_question(prospect)}"
                )

                Conversation.objects.create(
                    prospect=prospect,
                    role="assistant",
                    message=reply,
                )

                prospect.last_question = reply
                prospect.save(update_fields=["last_question"])

                return reply

            if _is_negative_consent(user_message):
                prospect.current_step = "consent_denied"
                prospect.save(update_fields=["current_step"])

                reply = (
                    "D'accord, je respecte votre choix.\n\n"
                    "Si vous souhaitez reprendre la préinscription plus tard, écrivez simplement : Je suis prêt(e)."
                )

                Conversation.objects.create(
                    prospect=prospect,
                    role="assistant",
                    message=reply,
                )

                prospect.last_question = reply
                prospect.save(update_fields=["last_question"])

                return reply

            reply = (
                "Pour commencer la préinscription, j'ai besoin de votre accord.\n\n"
                "Merci de répondre par Oui ou Non."
            )

            Conversation.objects.create(
                prospect=prospect,
                role="assistant",
                message=reply,
            )

            prospect.last_question = reply
            prospect.save(update_fields=["last_question"])

            return reply

        # ==================================================
        # EXTRACT & UPDATE PROFILE SILENTLY
        # ==================================================
        updated_fields = update_prospect_profile(
            prospect,
            user_message
        )

        # ==================================================
        # DETERMINE NEXT STEP
        # ==================================================
        next_question = get_next_question(prospect)
        is_question = is_user_asking_question(user_message)

        # ==================================================
        # CASE 1: ALL QUESTIONS ANSWERED
        # ==================================================
        if next_question is None:

            if prospect.current_step != "completed":
                # Première fois que le dossier est complet : récapitulatif +
                # demande des documents.
                reply = build_final_message()

                prospect.current_step = "completed"
                prospect.dossier_complet = True
                prospect.last_question = None

                prospect.save(
                    update_fields=[
                        "current_step",
                        "dossier_complet",
                        "last_question",
                    ]
                )

            elif is_user_asking_question(user_message):
                # Le dossier est déjà complet : on continue de répondre aux
                # questions normalement, au lieu de renvoyer sans cesse le
                # même récapitulatif.
                answer = answer_general_question(user_message)
                reply = answer or (
                    "Votre dossier est déjà complet et transmis à notre équipe 🙂\n\n"
                    "N'hésitez pas si vous avez d'autres questions."
                )

            else:
                reply = (
                    "Votre dossier est déjà complet ✅ Notre équipe le traite.\n\n"
                    "Vous pouvez encore nous envoyer des documents ou poser des "
                    "questions ici à tout moment."
                )

            Conversation.objects.create(
                prospect=prospect,
                role="assistant",
                message=reply,
            )

            return reply

        # ==================================================
        # CASE 2: USER ASKING A GENERAL QUESTION
        # ==================================================
        messages = []

        if is_question:
            # Get answer from Claude/Groq
            answer = answer_general_question(user_message)
            
            if answer:
                messages.append(answer)
                messages.append("")
            
            # Add qualification question
            messages.append("Continuons pour analyser votre profil :")
            messages.append("")
            messages.append(next_question)

            reply = "\n".join(messages).strip()

        # ==================================================
        # CASE 3: NORMAL QUALIFICATION ANSWER
        # ==================================================
        else:
            if updated_fields:
                for field in updated_fields:
                    label = FIELD_LABELS.get(field)
                    if label:
                        messages.append(f"✅ Merci, {label} a bien été enregistré.")

            if not messages:
                messages.append("Merci pour votre réponse.")

            messages.append("")
            messages.append(next_question)

            reply = "\n".join(messages).strip()

        Conversation.objects.create(
            prospect=prospect,
            role="assistant",
            message=reply,
        )

        prospect.last_question = next_question
        prospect.save(update_fields=["last_question"])

        return reply

    except Exception as e:
        print("❌ AI ERROR :", e)
        return "Une erreur est survenue. Veuillez réessayer."


# ==========================================================
# MESSAGE FINAL
# ==========================================================

def build_final_message():
    """
    Message final quand le profil est complet.
    Pas de récapitulatif ni d'analyse détaillée : juste une confirmation
    et la demande des documents nécessaires pour finaliser le dossier.
    """

    documents_list = "\n".join(
        f"{i}️⃣ {doc}" for i, doc in enumerate(FINAL_SUBMISSION_DOCUMENTS, start=1)
    )

    return (
        "✅ Merci, votre profil est complet et bien enregistré.\n\n"
        "Notre équipe va maintenant l'analyser pour vous proposer les meilleures "
        "options (université, programme, financement).\n\n"
        "📎 Pour finaliser votre dossier, merci de nous envoyer ici, en photo ou "
        "scannés, les documents suivants :\n\n"
        f"{documents_list}\n\n"
        "Vous pouvez les envoyer directement dans cette conversation, ils seront "
        "transmis à notre équipe pour la préparation de votre dossier."
    )