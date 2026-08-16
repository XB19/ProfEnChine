from django.db import models


# =========================
# PROSPECT PROFILE (CRM CORE)
# =========================
class ProspectProfile(models.Model):

    phone_number = models.CharField(max_length=20, unique=True)

    # =========================
    # IDENTITÉ
    # =========================
    full_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)

    # =========================
    # FINANCE
    # =========================
    # plus stable pour IA (évite "5 millions", "5M", etc.)
    budget = models.IntegerField(blank=True, null=True)

    # =========================
    # PARCOURS ACADÉMIQUE
    # =========================
    education_level = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Niveau d'études ACTUEL (Bac, Licence, Master) [Q4]"
    )

    current_field = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Filière SOUHAITÉE en Chine (Informatique, Commerce, Médecine) [Q3]"
    )

    target_program = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Niveau d'études SOUHAITÉ en Chine (Licence, Master, Doctorat, Année de langue) [Q2]"
    )

    # =========================
    # DOCUMENTS & OBJECTIF
    # =========================
    objective = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Immigrer en Chine ou uniquement étudier"
    )

    passport = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Oui, Non, ou date d'expiration"
    )

    criminal_record = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Oui (casier judiciaire) ou Non (vierge)"
    )

    departure_date = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Septembre 2026, Mars 2027, etc."
    )

    in_whatsapp_group = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Oui ou Non"
    )

    # =========================
    # CRM INTELLIGENCE
    # =========================
    STATUS_CHOICES = [
        ('cold', 'Froid'),
        ('warm', 'Moyen'),
        ('hot', 'Chaud'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='cold'
    )

    ai_score = models.IntegerField(default=0)
    human_takeover = models.BooleanField(default=False)
    dossier_complet = models.BooleanField(default=False)

    notes = models.TextField(blank=True, null=True)
    last_followup = models.DateTimeField(blank=True, null=True)

    # =========================
    # 🧠 STATE MACHINE (IMPORTANT POUR TON BOT)
    # =========================

    current_step = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    last_question = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    last_answer = models.TextField(
        blank=True,
        null=True
    )

    confidence_score = models.FloatField(default=0.0)

    # =========================
    # SYSTEM FIELDS
    # =========================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number


# =========================
# CONVERSATION (CRM LINKED)
# =========================
class Conversation(models.Model):

    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
    )

    prospect = models.ForeignKey(
        ProspectProfile,
        on_delete=models.CASCADE,
        related_name="conversations"
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prospect.phone_number} - {self.role}"