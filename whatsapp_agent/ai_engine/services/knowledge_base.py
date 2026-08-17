"""
BASE DE CONNAISSANCES - "LE PROF EN CHINE"
Tous les détails, coûts, procédures, universités, etc.
"""

# ==========================================================
# IDENTITÉ ET TON DE L'AGENT
# ==========================================================

AGENT_IDENTITY = {
    "name": "Prof en Chine",
    "tone": ["Professionnel", "Direct", "Encourageant", "Structuré", "Rapide", "Confiant", "Clair"],
    "languages": ["Français", "Anglais"],
    "target_countries": ["Togo", "Bénin", "Cameroun", "Côte d'Ivoire", "Burkina Faso", "Sénégal", "Congo", "Gabon"],
}

# ==========================================================
# COÛTS DÉTAILLÉS
# ==========================================================

COSTS = {
    "translation_per_page": 5000,  # FCFA
    "translation_standard_dossier": 30000,  # FCFA
    "file_study": 60000,  # FCFA (étude dossier)
    "jw202": 350000,  # FCFA
    "visa": {"min": 19000, "max": 50000},  # FCFA
    "language_year_tuition": {"min": 600000, "max": 1200000},  # FCFA
    "dormitory_per_year": 250000,  # FCFA
    "apartment_per_month": 60000,  # FCFA
    "flight": {"min": 400000, "max": 700000},  # FCFA
    "insurance": {"min": 50000, "max": 100000},  # FCFA
}

BACHELOR_COSTS = {
    "tuition_per_year": {"min": 1000000, "max": 4000000},  # FCFA
    "dormitory": {"min": 250000, "max": 600000},  # FCFA
    "insurance": {"min": 50000, "max": 100000},  # FCFA
    "visa": {"min": 19000, "max": 50000},  # FCFA
    "flight": {"min": 400000, "max": 700000},  # FCFA
}

MASTER_COSTS = {
    "tuition_per_year": {"min": 1500000, "max": 5000000},  # FCFA
    "accommodation": {"min": 300000, "max": 800000},  # FCFA
    "insurance": {"min": 50000, "max": 100000},  # FCFA
}

# ==========================================================
# PARCOURS DISPONIBLES
# ==========================================================

PROGRAMS = {
    "language_year": {
        "name": "Année de langue chinoise",
        "duration": "1 an",
        "recommended_for": [
            "Débutants complets",
            "Étudiants sans bon dossier",
            "Étudiants voulant immigrer progressivement",
            "Étudiants avec petit budget",
            "Étudiants préparant Licence/Master après",
        ],
        "conditions": [
            "Bac minimum",
            "Passeport valide",
            "Casier judiciaire vierge",
            "Bonne santé",
        ],
        "documents": [
            "Passeport",
            "Attestation du Bac",
            "Relevé du Bac",
            "Casier judiciaire",
            "CV",
            "Certificat médical chinois",
        ],
        "budget_range": {"min": 1800000, "max": 3000000},  # FCFA
        "advantages": [
            "Apprendre le chinois",
            "Préparer une future Licence ou Master",
            "Faciliter l'intégration",
            "Augmenter les chances d'opportunités sur place",
        ],
    },
    "bachelor": {
        "name": "Licence",
        "duration": "4-5 ans",
        "fields": [
            "Médecine",
            "Informatique",
            "Génie civil",
            "IA",
            "Commerce",
            "Finance",
            "Architecture",
            "Pharmacie",
            "Génie biomédical",
            "Aviation",
            "Arts",
            "Design",
            "Communication",
            "Relations internationales",
            "Langue chinoise",
        ],
        "conditions": [
            "Bac obligatoire",
            "Âge généralement < 25 ans pour bourse",
            "Bon niveau académique",
        ],
        "types": {
            "self_funded": {
                "name": "Self-funded",
                "advantages": [
                    "Admission plus facile",
                    "Procédure rapide",
                    "Beaucoup d'universités disponibles",
                ],
                "budget": BACHELOR_COSTS,
            },
            "scholarship": {
                "name": "Avec bourse",
                "types": [
                    "CSC Scholarship (gouvernementale)",
                    "Provincial Scholarship",
                    "University Scholarship",
                ],
            },
        },
    },
    "master": {
        "name": "Master",
        "duration": "2-3 ans",
        "conditions": [
            "Licence obligatoire",
            "Relevés universitaires",
            "Passeport",
            "CV",
            "Plan d'étude",
        ],
        "documents": [
            "Diplôme Licence",
            "Relevés de notes universitaires",
            "Motivation letter",
            "Lettres de recommandation",
            "CV",
        ],
        "budget_self_funded": MASTER_COSTS,
        "scholarship": {
            "accessibility": "Très accessible comparé à la Licence",
            "csc_coverage": [
                "Scolarité complète",
                "Allocation mensuelle",
                "Hébergement",
            ],
            "ideal_profile": [
                "Bon GPA",
                "Projet clair",
                "Âge raisonnable",
                "Bon anglais",
            ],
        },
    },
    "phd": {
        "name": "Doctorat",
        "duration": "3-5 ans",
        "conditions": [
            "Master obligatoire",
            "Projet recherche",
            "Bon parcours académique",
        ],
        "documents": [
            "Master",
            "Projet de recherche",
            "CV académique",
            "Publications (avantage)",
            "Lettres de recommandation",
        ],
        "advantages": [
            "Très fortes chances de bourse",
            "Allocation élevée",
            "Recherche avancée",
        ],
    },
}

# ==========================================================
# FINANCEMENT - COÛT TOTAL SELON BOURSE / UNIVERSITÉ
# ==========================================================

FINANCING_OVERVIEW = {
    "note": (
        "Le montant total à prévoir dépend de l'université choisie et du profil de "
        "l'étudiant, ainsi que de l'obtention ou non d'une bourse."
    ),
    "no_scholarship": {
        "programs": ["Licence", "Master"],
        "total_budget": {"min": 400000, "max": 2000000},  # FCFA, pour tout le programme
        "note": (
            "Pour la Licence ou le Master, les étudiants sans bourse financent "
            "eux-mêmes leurs études. Le montant final dépend de l'université et du profil."
        ),
    },
    "monthly_allowance_with_scholarship": {
        "master": {"min": 150000, "max": 350000},  # FCFA/mois
        "phd": {"min": 150000, "max": 450000},  # FCFA/mois
    },
}

# ==========================================================
# TYPES DE VISA ACCOMPAGNÉS
# ==========================================================

VISA_TYPES = ["Étudiant", "Business", "Tourisme"]

# ==========================================================
# DOCUMENTS DE SOUMISSION FINALE (APRÈS QUALIFICATION)
# ==========================================================

FINAL_SUBMISSION_DOCUMENTS = [
    "Passeport",
    "Casier judiciaire",
    "Diplôme",
    "Photo passeport (format numérique)",
]

# ==========================================================
# RÈGLES DE RECOMMANDATION
# ==========================================================

RECOMMENDATION_RULES = {
    "small_budget": {
        "condition": "Budget < 2.5M FCFA",
        "recommend": [
            "Année de langue",
            "Universités moins chères",
            "Dortoir universitaire",
            "Programmes self-funded low cost",
        ],
    },
    "good_academics": {
        "condition": "Licence/Master avec bonnes notes, âge raisonnable, casier vierge",
        "recommend": [
            "Bourses CSC",
            "Bourses provinciales",
            "Bourses universitaires",
        ],
    },
    "high_age": {
        "condition": "Licence > 28 ans, Master > 35 ans",
        "recommend": [
            "Éviter les bourses compétitives",
            "Prioriser self-funded",
        ],
    },
    "no_passport": {
        "condition": "Pas de passeport",
        "recommend": [
            "Priorité: obtenir le passeport avant dépôt",
        ],
    },
    "weak_profile": {
        "condition": "Mauvaises notes, long gap académique",
        "recommend": [
            "Année de langue",
            "Universités accessibles",
            "Self-funded",
        ],
    },
}

# ==========================================================
# DEMANDES TRÈS POPULAIRES - STEM, SANTÉ, BUSINESS
# ==========================================================

POPULAR_FIELDS = {
    "stem": ["IA", "Informatique", "Data Science", "Génie biomédical", "Génie civil"],
    "health": ["Médecine", "Pharmacie", "Santé publique"],
    "business": ["Commerce international", "Finance", "Marketing"],
}

# ==========================================================
# QUESTIONS SUPPLÉMENTAIRES PAR FILIÈRE
# ==========================================================

FIELD_SPECIFIC_QUESTIONS = {
    "medicine": [
        "Avez-vous un bon niveau en sciences ?",
        "Acceptez-vous un programme en anglais ?",
    ],
    "informatique": [
        "Avez-vous déjà des bases en programmation ?",
    ],
    "ia": [
        "Avez-vous déjà des bases en programmation ?",
        "Connaissances en mathématiques/statistiques ?",
    ],
    "master_research": [
        "Avez-vous déjà un sujet de recherche ?",
    ],
}

# ==========================================================
# PROCESSUS COMPLET DE CANDIDATURE
# ==========================================================

APPLICATION_PROCESS = [
    "Traduction des documents",
    "Étude du dossier",
    "Candidature université",
    "Admission",
    "Obtention JW202",
    "Demande de visa",
    "Paiement scolarité",
    "Réservation logement",
    "Achat billet",
    "Départ Chine",
]

# ==========================================================
# RÉPONSES AUX OBJECTIONS COURANTES
# ==========================================================

OBJECTION_RESPONSES = {
    "no_money": {
        "objection": "Je n'ai pas assez d'argent",
        "response": """Pas de souci 😊

Nous avons plusieurs solutions :

💰 Universités avec frais réduits
📚 Bourses partielles disponibles
🌍 Programmes self-funded adaptés

Le plus important est d'abord d'analyser votre profil afin de trouver l'option la plus adaptée à votre budget.

Quel est approximativement votre budget ?""",
    },
    "no_passport": {
        "objection": "Je n'ai pas encore de passeport",
        "response": """Le passeport est indispensable pour commencer les procédures officielles. 

✅ Priorité 1: Lancer la demande rapidement dans votre pays

📌 Pendant ce temps, nous pouvons :
- Préparer vos autres documents
- Analyser votre profil
- Choisir les meilleures universités

En combien de temps pouvez-vous avoir votre passeport ?""",
    },
    "worried_about_level": {
        "objection": "Je ne suis pas sûr(e) de mon niveau",
        "response": """C'est normal ! 😊

Notre approche :

1️⃣ Année de langue pour renforcer votre chinois
2️⃣ Ensuite Licence/Master avec plus de confiance
3️⃣ Support académique tout au long

Quel est actuellement votre niveau d'études ?""",
    },
}

# ==========================================================
# FAQ - QUESTIONS FRÉQUENTES ET RÉPONSES
# ==========================================================

FAQ = {
    "how_much_cost": {
        "keywords": ["coûte", "prix", "budget", "frais", "combien"],
        "answer": """💰 **Budget estimatif par programme :**

🟦 **Année de langue** : 1.8M - 3M FCFA
🟦 **Licence (sans bourse)** : 400 000 - 2 000 000 FCFA pour tout le programme
🟦 **Master (sans bourse)** : 400 000 - 2 000 000 FCFA pour tout le programme
🟦 **Doctorat** : Souvent gratuit avec bourse

📌 Le montant final dépend de l'université choisie, de votre profil, et de l'obtention ou non d'une bourse.

🎓 **Avec bourse** :
- Master : allocation mensuelle de 150 000 à 350 000 FCFA
- Doctorat : allocation mensuelle de 150 000 à 450 000 FCFA

📋 **Coûts détaillés** :
- Traduction: 5,000 FCFA/page
- Étude dossier: 60,000 FCFA
- Visa: 19,000 - 50,000 FCFA
- JW202: 350,000 FCFA
- Billet avion: 400,000 - 700,000 FCFA
- Logement: 60,000 FCFA/mois (appartement)

➡️ Quel programme vous intéresse ?""",
    },
    "how_get_scholarship": {
        "keywords": ["bourse", "gratuit", "aid", "scholarship", "financement"],
        "answer": """🏆 **Bourses disponibles en Chine :**

**1️⃣ CSC Scholarship (gouvernementale)**
- ✅ Couvre tout (scolarité + logement + allocation)
- 💰 Allocation mensuelle : Master 150 000 - 350 000 FCFA, Doctorat 150 000 - 450 000 FCFA
- 📊 Très compétitive
- 📝 Conditions : bonnes notes, projet clair

**2️⃣ Bourses provinciales**
- 📊 Moins compétitive que CSC
- 💰 Couvre 50%, 70%, ou 100%

**3️⃣ Bourses universitaires**
- 💰 Bourses internes des universités

**4️⃣ Bourses partielles**
- 📚 Pour réduire les frais

➡️ Quel est votre niveau académique actuel ?""",
    },
    "what_universities": {
        "keywords": ["université", "universités", "quelle", "meilleure", "recommande"],
        "answer": """🏫 **Les universités dépendent de votre profil.**

**Après votre qualification, nous vous proposerons :**

✅ Universités adaptées à votre budget
✅ Universités dans votre domaine
✅ Universités reconnues internationalement

🟦 **Catégories** :
- Low-cost (petit budget)
- Qualité moyenne
- Premium (Top classement)

📌 Nous travaillons avec des universités vérifiées via CUCAS et China Admissions.

➡️ Quel est votre budget et votre domaine ?""",
    },
    "visa_process": {
        "keywords": ["visa", "procédure", "demande", "application"],
        "answer": """📖 **Processus visa étudiant Chine :**

**1️⃣ Admission à l'université**
**2️⃣ Obtention du JW202** (document d'invitation)
**3️⃣ Demande visa auprès du service** (Chinese Visa Application Service Center)
**4️⃣ Entretien (si nécessaire)**
**5️⃣ Obtention du visa**

⏱️ Durée : environ 2-4 semaines

💰 Coûts :
- Visa : 19,000 - 50,000 FCFA
- JW202 : 350,000 FCFA

📌 Vous pouvez faire la demande une fois votre admission confirmée.

📌 Nous accompagnons aussi les demandes de visa Business et Tourisme, en plus du visa étudiant.

➡️ Êtes-vous prêt à commencer les procédures ?""",
    },
    "documents_needed": {
        "keywords": ["documents", "papiers", "requis", "nécessaires", "dossier"],
        "answer": """📋 **Documents généralement requis :**

**De base** :
✅ Passeport (copie + original)
✅ Bac (attestation + relevé)
✅ Casier judiciaire (extrait)
✅ CV
✅ Certificat médical chinois

**Pour Master** :
✅ Diplôme Licence
✅ Relevés universitaires
✅ Motivation letter
✅ Lettres de recommandation

**Pour Doctorat** :
✅ Tous les documents Master
✅ Projet de recherche
✅ CV académique

📌 Nous vous aiderons à traduire et formatter tous vos documents.

Quel programme vous envisagez ?""",
    },
    "timeline": {
        "keywords": ["quand", "date", "combien de temps", "délai", "processus", "durée"],
        "answer": """⏱️ **Calendrier complet :**

**Phase 1 : Préparation** (1-2 mois)
- Traduction documents
- Étude dossier
- Candidature

**Phase 2 : Admission** (1-3 mois)
- Attente réponse université
- Obtention admission

**Phase 3 : Visa** (1 mois)
- JW202
- Demande visa

**Phase 4 : Départ** (2-4 semaines avant)
- Paiement scolarité
- Réservation logement
- Achat billet

⏱️ Total : 4-7 mois (selon université)

📌 Nous accélèrons le processus au maximum.

Souhaitez-vous partir en septembre 2026 ou mars 2027 ?""",
    },
    "working_while_studying": {
        "keywords": ["travail", "job", "argent", "part-time", "emploi"],
        "answer": """💼 **Travail en tant qu'étudiant en Chine :**

**Règles** :
- ✅ Autorisé 20h/semaine durant les études
- ✅ Autorisé temps plein pendant les vacances
- ⚠️ Nécessite autorisation de l'université

**Opportunités** :
- 🏫 Tutoring (enseignement de langues)
- 💻 Freelance online
- 📚 Campus jobs
- 🏢 Entreprises internationales

💰 **Revenus** : 3,000 - 10,000 FCFA/jour en tutoring

📌 Cela aide à couvrir les frais de vie mais ne remplace pas le budget initial.

Souhaitez-vous avoir des informations sur le coût de la vie ?""",
    },
    "life_in_china": {
        "keywords": ["vie", "logement", "dortoir", "dépenses", "coût de la vie", "expatrié"],
        "answer": """🏠 **Coût de la vie en Chine :**

**Logement** :
- Dortoir université : 60,000 - 250,000 FCFA/mois
- Appartement : 60,000 - 300,000 FCFA/mois

**Nourriture** :
- Restaurant universitaire : 10,000 - 30,000 FCFA/repas
- Faire à manger : beaucoup moins cher

**Transport** :
- Métro/bus : très bon marché (1,000-2,000 FCFA)
- Vélo : 200,000 - 400,000 FCFA (une fois)

**Loisirs** :
- Cinéma, restaurants : 20,000 - 50,000 FCFA
- Très accessible

💡 **Budget de vie mensuel** : 300,000 - 600,000 FCFA

📌 Les universités aident à trouver logement abordable.

Des questions spécifiques sur la vie là-bas ?""",
    },
}

# ==========================================================
# DÉTECTION D'INTENTIONS
# ==========================================================

INTENT_KEYWORDS = {
    "ask_language_year": ["année de langue", "chinois", "apprendre le chinois"],
    "ask_bachelor": ["licence", "bac+3", "3 ans"],
    "ask_master": ["master", "bac+5", "2 ans", "master's"],
    "ask_phd": ["doctorat", "phd", "recherche"],
    "ask_scholarship": ["bourse", "gratuit", "aid", "funding"],
    "ask_cost": ["coûte", "prix", "budget", "frais", "combien"],
    "ask_visa": ["visa", "procédure", "demande"],
    "ask_documents": ["documents", "papiers", "dossier"],
    "ask_deadline": ["quand", "date", "combien de temps", "délai"],
    "ask_university": ["université", "quelle", "meilleure", "recommande"],
    "ask_working": ["travail", "job", "part-time"],
    "ask_life": ["vie", "logement", "dortoir", "coût de vie"],
}

# ==========================================================
# FONCTIONS UTILITAIRES
# ==========================================================

def get_faq_answer(question: str) -> str | None:
    """
    Récherche une réponse FAQ basée sur les mots-clés.
    """
    question_lower = question.lower()
    
    for faq_key, faq_data in FAQ.items():
        keywords = faq_data.get("keywords", [])
        if any(keyword in question_lower for keyword in keywords):
            return faq_data.get("answer", None)
    
    return None


def detect_intent(message: str) -> str | None:
    """
    Détecte l'intention de l'utilisateur.
    """
    message_lower = message.lower()
    
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in message_lower for keyword in keywords):
            return intent
    
    return None


def get_program_info(program: str) -> dict | None:
    """
    Récupère les infos d'un programme spécifique.
    """
    program_lower = program.lower()
    
    for program_key, program_data in PROGRAMS.items():
        if program_lower in program_key or program_lower in program_data.get("name", "").lower():
            return program_data
    
    return None


def get_budget_recommendation(budget: float) -> list:
    """
    Recommande un programme basé sur le budget.
    """
    recommendations = []
    
    if budget < 2500000:
        recommendations = [
            "Année de langue (très accessible)",
            "Universités low-cost",
            "Programmes auto-financés économiques",
        ]
    elif budget < 5000000:
        recommendations = [
            "Licence self-funded",
            "Master self-funded",
        ]
    else:
        recommendations = [
            "Licence premium",
            "Master premium",
            "Doctorat avec bourse",
        ]
    
    return recommendations
