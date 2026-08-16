from conversations.models import ProspectProfile
from .scoring import calculate_ai_score
from .status import determine_status


def extract_user_data(phone_number, message):
    """
    Mise à jour CRM sans appel IA.

    Les informations utilisateur sont déjà extraites
    par update_prospect_profile() dans services.py.

    Cette fonction ne fait que :
    - récupérer le prospect
    - recalculer le score
    - recalculer le statut
    """

    try:

        profile, _ = ProspectProfile.objects.get_or_create(
            phone_number=phone_number
        )

        # Score IA
        score = calculate_ai_score(profile)
        profile.ai_score = score

        # Statut prospect
        profile.status = determine_status(score)

        # Dossier complet
        profile.dossier_complet = all([
            profile.age,
            profile.nationality,
            profile.education_level,
            profile.current_field,
            profile.target_program,
            profile.budget is not None
        ])

        profile.save()

        return {
            "success": True,
            "score": score,
            "status": profile.status,
            "dossier_complet": profile.dossier_complet
        }

    except Exception as e:

        print("❌ ERREUR EXTRACTION :", str(e))

        return {
            "success": False,
            "error": str(e)
        }