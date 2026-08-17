import os

os.environ.setdefault("GROQ_API_KEY", "test-key")

from django.test import TestCase

from ai_engine.services.ai_chat import build_orientation_message
from ai_engine.services.conversation import get_next_question
from ai_engine.services.crm import update_prospect_profile
from conversations.models import ProspectProfile


class ConversationFlowTests(TestCase):
    def test_next_question_prioritizes_profile_fields(self):
        prospect = ProspectProfile.objects.create(
            phone_number="123456",
            full_name="Alice Kouassi",
        )

        question = get_next_question(prospect)

        self.assertIn("immigrer", question.lower())
        self.assertNotIn("nom", question.lower())

    def test_orientation_message_is_generic_and_profile_based(self):
        prospect = ProspectProfile.objects.create(
            phone_number="654321",
            full_name="Bob Dossou",
            current_field="Informatique",
            target_program="Intelligence artificielle",
            budget=3000000,
            education_level="Licence",
        )

        message = build_orientation_message(prospect)

        self.assertIn("profil", message.lower())
        self.assertIn("orientation", message.lower())
        self.assertNotIn("harvard", message.lower())
        self.assertNotIn("oxford", message.lower())

    def test_domain_question_fills_current_field(self):
        from ai_engine.services.extractor import extract_profile

        profile = extract_profile(
            "Je veux faire informatique",
            "Dans quel domaine souhaitez-vous étudier en Chine ?"
        )

        self.assertEqual(profile["current_field"], "Informatique")

    def test_crm_updates_current_field_when_last_question_is_domain(self):
        prospect = ProspectProfile.objects.create(
            phone_number="999999"
        )

        from conversations.models import Conversation
        Conversation.objects.create(
            prospect=prospect,
            role="assistant",
            message="Dans quel domaine souhaitez-vous étudier en Chine ?"
        )

        updated = update_prospect_profile(prospect, "communication")

        self.assertIn("current_field", updated)
        self.assertEqual(prospect.current_field, "Communication")
        self.assertIsNone(prospect.target_program)

    def test_crm_updates_passport_and_criminal_record_as_clear_values(self):
        prospect = ProspectProfile.objects.create(phone_number="111111")

        from conversations.models import Conversation
        Conversation.objects.create(
            prospect=prospect,
            role="assistant",
            message="Avez-vous un passeport valide ?"
        )

        updated = update_prospect_profile(prospect, "Non, je n'ai pas de passeport et mon casier est vierge")

        self.assertIn("passport", updated)
        self.assertEqual(prospect.passport, "Non")
        self.assertEqual(prospect.criminal_record, "Non")

    def test_crm_updates_all_qualification_fields(self):
        prospect = ProspectProfile.objects.create(phone_number="test_all_fields")

        from conversations.models import Conversation
        
        # Test objectif
        Conversation.objects.create(
            prospect=prospect,
            role="assistant",
            message="Voulez-vous immigrer en Chine ou uniquement étudier ?"
        )
        updated = update_prospect_profile(prospect, "immigrer")
        self.assertIn("objective", updated)
        self.assertEqual(prospect.objective, "Immigrer")
        
        # Test departure_date
        Conversation.objects.create(
            prospect=prospect,
            role="assistant",
            message="Quand souhaitez-vous partir en Chine ?"
        )
        updated = update_prospect_profile(prospect, "septembre 2026")
        self.assertIn("departure_date", updated)
        self.assertEqual(prospect.departure_date, "Septembre 2026")
        
        # Test whatsapp_group
        Conversation.objects.create(
            prospect=prospect,
            role="assistant",
            message="Êtes-vous dans le groupe WhatsApp ?"
        )
        updated = update_prospect_profile(prospect, "oui")
        self.assertIn("in_whatsapp_group", updated)
        self.assertEqual(prospect.in_whatsapp_group, "Oui")

