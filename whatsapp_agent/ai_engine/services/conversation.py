def get_next_question(prospect):
    """
    Retourne la prochaine question de qualification.
    Ordre cohérent : Nom → Objectif → Niveau → Filière → Éducation → Âge → Nationalité → Passeport → Casier → Départ → Budget → WhatsApp
    """

    def is_missing(value):
        """Vérifie si une valeur est vide/invalide"""
        return value in [None, "", " ", "null", "None", "Non spécifié"]

    # ================================================
    # 0️⃣ NOM COMPLET (FIRST - MUST HAVE)
    # ================================================
    if is_missing(getattr(prospect, "full_name", None)):
        prospect.current_step = "full_name"
        prospect.save(update_fields=["current_step"])
        return (
            "👤 **Quel est votre nom complet ?**\n\n"
            "Merci de nous indiquer votre prénom et nom."
        )

    # ================================================
    # 1️⃣ OBJECTIF (Immigrer ou Étudier)
    # ================================================
    if is_missing(getattr(prospect, "objective", None)):
        prospect.current_step = "objective"
        prospect.save(update_fields=["current_step"])
        return (
            "1️⃣ **Voulez-vous immigrer en Chine ou uniquement étudier ?**\n\n"
            "Répondez : Immigrer ou Étudier"
        )

    # ================================================
    # 2️⃣ NIVEAU D'ÉTUDES ACTUEL
    # ================================================
    if is_missing(getattr(prospect, "education_level", None)):
        prospect.current_step = "education_level"
        prospect.save(update_fields=["current_step"])
        return (
            "2️⃣ **Quel est votre niveau d'études actuel ?** (avant la Chine)\n\n"
            "Ex : Bac, Licence, Master..."
        )

    # ================================================
    # 3️⃣ FILIÈRE SOUHAITÉE EN CHINE
    # ================================================
    if is_missing(getattr(prospect, "current_field", None)):
        prospect.current_step = "current_field"
        prospect.save(update_fields=["current_step"])
        return (
            "3️⃣ **Dans quelle filière souhaitez-vous étudier en Chine ?**\n\n"
            "Ex : Informatique, Médecine, Commerce, Génie civil, Architecture, "
            "Design, Droit, Finance, Ingénierie, Langue chinoise, Marketing..."
        )

    # ================================================
    # 4️⃣ NIVEAU D'ÉÉTUDES SOUHAITÉ EN CHINE
    # ================================================
    if is_missing(getattr(prospect, "target_program", None)):
        prospect.current_step = "target_program"
        prospect.save(update_fields=["current_step"])
        return (
            "4️⃣ **Pour quel niveau d'études souhaitez-vous étudier en Chine ?**\n\n"
            "- Année de langue chinoise\n"
            "- Licence\n"
            "- Master\n"
            "- Doctorat"
        )

    # ================================================
    # 5️⃣ ÂGE
    # ================================================
    if is_missing(getattr(prospect, "age", None)):
        prospect.current_step = "age"
        prospect.save(update_fields=["current_step"])
        return (
            "5️⃣ **Quel âge avez-vous ?**"
        )

    # ================================================
    # 6️⃣ NATIONALITÉ
    # ================================================
    if is_missing(getattr(prospect, "nationality", None)):
        prospect.current_step = "nationality"
        prospect.save(update_fields=["current_step"])
        return (
            "6️⃣ **Quelle est votre nationalité ?**"
        )

    # ================================================
    # 7️⃣ PASSEPORT
    # ================================================
    if is_missing(getattr(prospect, "passport", None)):
        prospect.current_step = "passport"
        prospect.save(update_fields=["current_step"])
        return (
            "7️⃣ **Avez-vous un passeport valide ?**\n\n"
            "Répondez :\n"
            "- Oui (si vous en avez un valide)\n"
            "- Non (si vous n'en avez pas ou s'il expire bientôt)\n"
            "- Ou précisez la date d'expiration (ex: Valide jusqu'en 2028)"
        )

    # ================================================
    # 8️⃣ CASIER JUDICIAIRE
    # ================================================
    if is_missing(getattr(prospect, "criminal_record", None)):
        prospect.current_step = "criminal_record"
        prospect.save(update_fields=["current_step"])
        return (
            "8️⃣ **Avez-vous un casier judiciaire ?** "
            "(avez-vous déjà été condamné(e) par la justice ?)\n\n"
            "Répondez :\n"
            "- Oui (j'ai un casier judiciaire)\n"
            "- Non (mon casier est vierge)"
        )

    # ================================================
    # 9️⃣ DATE DE DÉPART
    # ================================================
    if is_missing(getattr(prospect, "departure_date", None)):
        prospect.current_step = "departure_date"
        prospect.save(update_fields=["current_step"])
        return (
            "9️⃣ **Quand souhaitez-vous partir en Chine ?**\n\n"
            "- Septembre 2026\n"
            "- Mars 2027\n"
            "(Ou proposez une autre date)"
        )

    # ================================================
    # 🔟 BUDGET
    # ================================================
    if is_missing(getattr(prospect, "budget", None)):
        prospect.current_step = "budget"
        prospect.save(update_fields=["current_step"])
        return (
            "🔟 **Quel est votre budget approximatif en FCFA ?**\n\n"
            "Pour vos études et frais liés (traduction, visa, billet, etc.)"
        )

    # ================================================
    # 1️⃣1️⃣ GROUPE WHATSAPP
    # ================================================
    if is_missing(getattr(prospect, "in_whatsapp_group", None)):
        prospect.current_step = "in_whatsapp_group"
        prospect.save(update_fields=["current_step"])
        return (
            "1️⃣1️⃣ **Êtes-vous déjà dans le groupe WhatsApp \"Le Prof en Chine\" ?**\n\n"
            "Répondez : Oui ou Non"
        )

    # ================================================
    # TOUTES LES QUESTIONS RÉPONDUES ✅
    # ================================================
    return None