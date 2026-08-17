from conversations.models import ProspectProfile


def calculate_ai_score(profile: ProspectProfile):

    score = 0

    # =========================================================
    # BUDGET (SAFE - IntegerField maintenant)
    # =========================================================
    budget = profile.budget or 0

    if budget >= 5_000_000:
        score += 35

    elif budget >= 2_000_000:
        score += 25

    elif budget >= 1_000_000:
        score += 15

    elif budget > 0:
        score += 5


    # =========================================================
    # PASSEPORT (string clair : Oui/Non)
    # =========================================================
    passport = profile.passport
    if isinstance(passport, bool):
        passport = "oui" if passport else "non"
    else:
        passport = str(passport or "").lower()

    if passport and passport not in ["", "non", "no", "false", "faux"]:
        score += 25
    elif passport in ["non", "no", "false", "faux"]:
        score += 5


    # =========================================================
    # NIVEAU D'ÉTUDE (SAFE STRING)
    # =========================================================
    level = (profile.education_level or "").lower()

    if level:

        if "master" in level:
            score += 20

        elif "licence" in level:
            score += 15

        elif "bac" in level or "lycee" in level:
            score += 10

        else:
            score += 5


    # =========================================================
    # FILIÈRE ACTUELLE
    # =========================================================
    field = (profile.current_field or "").lower()

    if field:

        if field in ["informatique", "it", "software", "data"]:
            score += 15

        elif field in ["commerce", "business", "gestion"]:
            score += 12

        elif field in ["finance", "marketing"]:
            score += 10

        else:
            score += 5


    # =========================================================
    # PROGRAMME SOUHAITÉ
    # =========================================================
    program = (profile.target_program or "").lower()

    if program:

        if "doctorat" in program:
            score += 25

        elif "ingénieur" in program or "ingenieur" in program:
            score += 20

        elif "informatique" in program or "ia" in program:
            score += 20

        elif "business" in program or "commerce" in program:
            score += 15

        elif "médecine" in program:
            score += 20

        else:
            score += 10


    # =========================================================
    # OBJECTIF
    # =========================================================
    objective = (profile.objective or "").lower()

    if objective:
        score += 10


    # =========================================================
    # CASIER JUDICIAIRE
    # =========================================================
    criminal_record = (profile.criminal_record or "").lower()

    if "non" in criminal_record or "vierge" in criminal_record:
        score += 15
    elif "oui" in criminal_record:
        score += 5  # Pénalité pour casier judiciaire


    # =========================================================
    # DATE DE DÉPART
    # =========================================================
    departure = (profile.departure_date or "").lower()

    if departure:
        score += 10


    # =========================================================
    # GROUPE WHATSAPP
    # =========================================================
    whatsapp = (profile.in_whatsapp_group or "").lower()

    if "oui" in whatsapp:
        score += 5  # Bonus pour engagement


    # =========================================================
    # COMPLETUDE DOSSIER
    # =========================================================
    fields = [
        profile.objective,
        profile.age,
        profile.nationality,
        profile.education_level,
        profile.current_field,
        profile.target_program,
        profile.budget,
        profile.passport,
        profile.criminal_record,
        profile.departure_date,
        profile.in_whatsapp_group,
    ]

    completed = sum(1 for f in fields if f not in [None, ""])

    completion_bonus = (completed / len(fields)) * 20
    score += round(completion_bonus)


    # =========================================================
    # CAP FINAL
    # =========================================================
    return min(score, 100)