from conversations.models import ProspectProfile


def generate_recommendation(phone_number):

    try:

        profile = ProspectProfile.objects.filter(
            phone_number=phone_number
        ).first()

        if not profile:
            return {
                "score": 0,
                "level": "unknown",
                "recommendations": [
                    "Analyse complète du dossier recommandée."
                ]
            }

        recommendations = []
        score = 0

        # =========================
        # ÂGE
        # =========================
        if profile.age is not None:

            if profile.age <= 25:
                score += 20
                recommendations.append("Excellent profil pour programme universitaire + bourse.")

            elif 26 <= profile.age <= 35:
                score += 10
                recommendations.append("Profil adapté aux programmes standards universitaires.")

            else:
                score += 5
                recommendations.append("Profil plutôt orienté self-funded ou programmes adaptés.")

        # =========================
        # BUDGET
        # =========================
        if profile.budget is not None:

            if profile.budget < 2000000:
                score += 5
                recommendations.append("Budget faible : orientation année de langue recommandée.")

            elif 2000000 <= profile.budget <= 5000000:
                score += 15
                recommendations.append("Budget moyen : plusieurs options universitaires possibles.")

            else:
                score += 25
                recommendations.append("Bon budget : accès à un large choix d’universités.")

        # =========================
        # PASSEPORT
        # =========================
        passport_lower = str(profile.passport).lower() if profile.passport else ""
        
        if passport_lower and "non" not in passport_lower:
            score += 15
            recommendations.append("Dossier prêt côté administratif (passeport disponible).")

        else:
            score -= 10
            recommendations.append("Priorité : lancer la procédure de passeport.")

        # =========================
        # PROGRAMME
        # =========================
        if profile.target_program:

            program = profile.target_program.lower()

            if "master" in program:
                score += 15
                recommendations.append("Candidat adapté pour admission en master.")

            elif "doctorat" in program:
                score += 20
                recommendations.append("Profil avancé pour programmes doctoraux.")

            elif "licence" in program:
                score += 10
                recommendations.append("Programme licence adapté.")

        # =========================
        # FILIÈRE
        # =========================
        if profile.current_field:

            field = profile.current_field.lower()

            if "informatique" in field or "it" in field:
                score += 15
                recommendations.append("Forte compatibilité avec universités technologiques.")

            elif "gestion" in field or "commerce" in field:
                score += 10
                recommendations.append("Compatible avec programmes business en Chine.")

        # =========================
        # SCORE FINAL
        # =========================
        if score >= 60:
            level = "excellent"
        elif score >= 40:
            level = "good"
        elif score >= 20:
            level = "medium"
        else:
            level = "low"

        # =========================
        # CAS PAR DÉFAUT
        # =========================
        if not recommendations:
            recommendations.append("Analyse complète du dossier recommandée.")

        return {
            "score": score,
            "level": level,
            "recommendations": recommendations
        }

    except Exception as e:
        print("❌ ERREUR RECOMMANDATION :", str(e))

        return {
            "score": 0,
            "level": "error",
            "recommendations": [
                "Analyse complète du dossier recommandée."
            ]
        }