"""
ANALYSE DE PROFIL & RECOMMANDATIONS
Analyse automatique du profil pour recommander le meilleur parcours
"""

from .knowledge_base import (
    PROGRAMS,
    RECOMMENDATION_RULES,
    POPULAR_FIELDS,
    FIELD_SPECIFIC_QUESTIONS,
)


def analyze_profile(prospect) -> dict:
    """
    Analyse automatique du profil d'un prospect.
    Retourne: {
        "score": int (0-100),
        "profile_type": str,
        "recommendations": list,
        "next_steps": list,
        "warnings": list,
        "program_match": str,
    }
    """
    
    analysis = {
        "score": 0,
        "profile_type": "unknown",
        "recommendations": [],
        "next_steps": [],
        "warnings": [],
        "program_match": None,
    }
    
    score = 0
    
    # ================================================
    # 1️⃣ VÉRIFICATIONS ESSENTIELLES
    # ================================================
    
    # Passeport
    passport_value = str(prospect.passport).lower() if prospect.passport is not None else ""
    if prospect.passport is True or passport_value in ["oui", "true", "vrai"]:
        score += 15
    elif prospect.passport is None or passport_value in ["non", "false", "faux"]:
        analysis["warnings"].append("⚠️ Passeport manquant ou expirant - Priorité: renouvellement")
        score -= 10
    
    # Casier judiciaire
    if prospect.criminal_record and str(prospect.criminal_record).lower() == "non":
        score += 15
    elif prospect.criminal_record is None:
        analysis["warnings"].append("⚠️ Casier judiciaire non confirmé")
    
    # ================================================
    # 2️⃣ ANALYSE ACADÉMIQUE
    # ================================================
    
    education_level = (prospect.education_level or "").lower()
    
    if "doctorat" in education_level:
        score += 25
        analysis["profile_type"] = "Advanced"
    elif "master" in education_level:
        score += 20
        analysis["profile_type"] = "Intermediate"
    elif "licence" in education_level or "bac+3" in education_level:
        score += 15
        analysis["profile_type"] = "Bachelor"
    elif "bac" in education_level:
        score += 10
        analysis["profile_type"] = "Secondary"
    else:
        analysis["warnings"].append("⚠️ Niveau d'études non clair")
    
    # ================================================
    # 3️⃣ ANALYSE BUDGÉTAIRE
    # ================================================
    
    budget = prospect.budget
    
    if budget is not None:
        try:
            budget = float(budget)
            
            if budget < 2500000:
                score += 10
                analysis["profile_type"] = (
                    "Budget limité - Année de langue recommandée"
                )
                analysis["recommendations"].append(
                    "💰 Budget réduit → Année de langue ou universités low-cost"
                )
            elif budget < 5000000:
                score += 15
                analysis["recommendations"].append(
                    "💰 Budget moyen → Licence/Master self-funded accessible"
                )
            else:
                score += 20
                analysis["recommendations"].append(
                    "💰 Bon budget → Accès aux universités premium"
                )
        except:
            pass
    else:
        analysis["warnings"].append("⚠️ Budget non renseigné")
    
    # ================================================
    # 4️⃣ ANALYSE ÂGE
    # ================================================
    
    age = prospect.age
    
    if age is not None:
        try:
            age = int(age)
            
            if age < 20:
                score += 10
            elif age < 25:
                score += 15
            elif age < 30:
                score += 12
            elif age < 35:
                score += 10
            elif age > 40:
                analysis["warnings"].append(
                    "⚠️ Âge élevé - Self-funded recommandé plutôt que bourses"
                )
                score -= 5
        except:
            pass
    
    # ================================================
    # 5️⃣ OBJECTIVE MATCH
    # ================================================
    
    objective = (prospect.objective or "").lower()
    
    if "immigr" in objective:
        score += 5
        analysis["recommendations"].append(
            "✅ Objectif immigration → Parcours complet de 4-5 ans recommandé"
        )
    elif "étudi" in objective:
        score += 3
    
    # ================================================
    # 6️⃣ FIELD MATCH (Demandes populaires)
    # ================================================
    
    current_field = (prospect.current_field or "").lower()
    
    if any(field.lower() in current_field for field in POPULAR_FIELDS["stem"]):
        score += 10
        analysis["recommendations"].append(
            "📊 Domaine STEM demandé → Bonnes opportunités de bourses"
        )
    elif any(
        field.lower() in current_field for field in POPULAR_FIELDS["health"]
    ):
        score += 8
    elif any(
        field.lower() in current_field
        for field in POPULAR_FIELDS["business"]
    ):
        score += 8
    
    # ================================================
    # 7️⃣ PROGRAMME RECOMMENDATION
    # ================================================
    
    target_program = (prospect.target_program or "").lower()
    
    if "langue" in target_program or "chinois" in target_program:
        analysis["program_match"] = "Année de langue"
    elif "licence" in target_program or "bachelor" in target_program:
        analysis["program_match"] = "Licence"
    elif "master" in target_program:
        analysis["program_match"] = "Master"
    elif "doctorat" in target_program or "phd" in target_program:
        analysis["program_match"] = "Doctorat"
    else:
        # Déterminer automatiquement
        if education_level and "bac" in education_level and budget and float(budget) < 3000000:
            analysis["program_match"] = "Année de langue"
        elif education_level and "licence" in education_level:
            analysis["program_match"] = "Master"
        else:
            analysis["program_match"] = "Licence"
    
    # ================================================
    # 8️⃣ SCORE FINAL
    # ================================================
    
    score = max(0, min(100, score))
    analysis["score"] = score
    
    # ================================================
    # 9️⃣ NEXT STEPS
    # ================================================
    
    if prospect.passport is None or str(prospect.passport).lower() == "non":
        analysis["next_steps"].append("1️⃣ Obtenir/Renouveler le passeport")
    
    analysis["next_steps"].append("2️⃣ Préparer les documents requis (Bac, casier, etc.)")
    analysis["next_steps"].append("3️⃣ Candidature universités")
    analysis["next_steps"].append(f"4️⃣ Visa étudiant vers la Chine")
    
    # ================================================
    # BONUS: Questions spécifiques selon filière
    # ================================================
    
    field_key = current_field.split()[0].lower() if current_field else None
    
    if field_key:
        for field_name, questions in FIELD_SPECIFIC_QUESTIONS.items():
            if field_name in current_field:
                analysis["extra_questions"] = questions
                break
    
    return analysis


def build_recommendation_message(prospect, analysis: dict) -> str:
    """
    Construit un message de recommandation personnalisé.
    """
    
    program = analysis.get("program_match", "Parcours personnalisé")
    score = analysis.get("score", 0)
    
    # Emoji status basé sur score
    if score >= 80:
        status_emoji = "🔥"
        status_text = "Excellent profil"
    elif score >= 60:
        status_emoji = "🔆"
        status_text = "Bon profil"
    elif score >= 40:
        status_emoji = "⚠️"
        status_text = "Profil à renforcer"
    else:
        status_emoji = "📋"
        status_text = "Profil en cours de qualification"
    
    message = f"{status_emoji} **{status_text}** (Score: {score}%)\n\n"
    
    message += f"📌 **Programme recommandé** : {program}\n\n"
    
    # Recommandations
    if analysis.get("recommendations"):
        message += "💡 **Recommandations** :\n"
        for rec in analysis["recommendations"][:3]:  # Top 3
            message += f"{rec}\n"
        message += "\n"
    
    # Avertissements
    if analysis.get("warnings"):
        message += "⚠️ **À vérifier** :\n"
        for warning in analysis["warnings"]:
            message += f"{warning}\n"
        message += "\n"
    
    # Prochaines étapes
    if analysis.get("next_steps"):
        message += "✅ **Prochaines étapes** :\n"
        for step in analysis["next_steps"][:3]:
            message += f"→ {step}\n"
    
    return message


def should_ask_scholarship_questions(prospect, analysis: dict) -> bool:
    """
    Détermine si on devrait poser des questions sur les bourses.
    """
    
    score = analysis.get("score", 0)
    age = prospect.age or 0
    education_level = (prospect.education_level or "").lower()
    
    # Conditions pour bourses:
    # 1. Bon profil académique (score >= 60)
    # 2. Âge raisonnable (< 28 pour licence, < 35 pour master)
    # 3. Niveau d'études approprié
    
    if score >= 60:
        if education_level and "licence" in education_level and age < 28:
            return True
        elif education_level and "master" in education_level and age < 35:
            return True
    
    return False
