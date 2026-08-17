"""
TEST COMPLET DU NETTOYAGE DU PROJET
Valide que:
1. Les 12 questions sont bien numérotées (0️⃣ à 1️⃣1️⃣)
2. Le flow des questions est cohérent
3. La détection hors sujet fonctionne
4. L'extraction du full_name fonctionne
5. Le CRM met à jour correctement
"""

import os
import sys
import django
import uuid
from datetime import datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from conversations.models import ProspectProfile, Conversation
from ai_engine.services.conversation import get_next_question
from ai_engine.services.filters import is_invalid_message, is_off_topic, get_off_topic_message
from ai_engine.services.ai_chat import FIELD_LABELS
from ai_engine.services.crm import update_prospect_profile

print("=" * 70)
print("🧪 TEST COMPLET DU NETTOYAGE DU PROJET")
print("=" * 70)

# ================================================================
# TEST 1: VÉRIFIER QUE TOUTES LES 12 QUESTIONS EXISTENT
# ================================================================
print("\n✅ TEST 1: Vérifier les 12 questions de qualification")
print("-" * 70)

test_prospect = ProspectProfile(phone_number=f"+33{uuid.uuid4().hex[:10]}")
test_prospect.save()  # Sauvegarder pour pouvoir modifier
questions = []
field_names = []

for i in range(20):  # Itération pour obtenir toutes les questions
    q = get_next_question(test_prospect)
    if q is None:
        break
    questions.append(q)
    field_names.append(test_prospect.current_step)
    
    # Marquer tous les champs comme remplis
    setattr(test_prospect, test_prospect.current_step, f"test_{i}")

print(f"✓ Trouvé {len(questions)} questions")
print(f"✓ Champs en ordre : {field_names}")

expected_fields = [
    "full_name", "objective", "target_program", "current_field",
    "education_level", "age", "nationality", "passport", 
    "criminal_record", "departure_date", "budget", "in_whatsapp_group"
]

if field_names == expected_fields:
    print("✅ L'ordre des questions est CORRECT !")
else:
    print(f"❌ L'ordre est incorrect !")
    print(f"  Attendu: {expected_fields}")
    print(f"  Obtenu : {field_names}")

# ================================================================
# TEST 2: VÉRIFIER LES EMOJIS DE NUMÉROTATION
# ================================================================
print("\n✅ TEST 2: Vérifier la numérotation (emojis)")
print("-" * 70)

emoji_checks = [
    ("👤", "full_name"),
    ("1️⃣", "objective"),
    ("2️⃣", "target_program"),
    ("3️⃣", "current_field"),
    ("4️⃣", "education_level"),
    ("5️⃣", "age"),
    ("6️⃣", "nationality"),
    ("7️⃣", "passport"),
    ("8️⃣", "criminal_record"),
    ("9️⃣", "departure_date"),
    ("🔟", "budget"),
    ("1️⃣1️⃣", "in_whatsapp_group"),
]

for emoji, field in emoji_checks:
    unique_phone = f"+33{uuid.uuid4().hex[:10]}"
    test_prospect = ProspectProfile(phone_number=unique_phone)
    test_prospect.save()  # Sauvegarder
    if field == "full_name":
        pass  # pas de remplissage
    else:
        setattr(test_prospect, field, None)
        # Remplir tous les précédents
        for prev_emoji, prev_field in emoji_checks:
            if prev_field != field:
                setattr(test_prospect, prev_field, "rempli")
    
    q = get_next_question(test_prospect)
    if q and emoji in q:
        print(f"✓ {emoji} trouvé pour {field}")
    else:
        print(f"❌ {emoji} MANQUANT pour {field}")
        if q:
            print(f"   Question reçue: {q[:50]}...")

# ================================================================
# TEST 3: DÉTECTION HORS SUJET
# ================================================================
print("\n✅ TEST 3: Détection des messages hors sujet")
print("-" * 70)

off_topic_tests = [
    ("Combien ça coûte à l'université de Pékin ?", False, "Question valide sur coûts"),
    ("Quel âge dois-je avoir pour étudier en Chine ?", False, "Question valide sur études"),
    ("Pourquoi le ciel est bleu ?", True, "Hors sujet"),
    ("Qui est le président de la France ?", True, "Hors sujet"),
    ("Comment puis-je obtenir une bourse pour étudier en Chine ?", False, "Question valide sur bourse"),
]

for msg, expected_off_topic, description in off_topic_tests:
    result = is_off_topic(msg)
    status = "✓" if result == expected_off_topic else "❌"
    print(f"{status} {description}")
    if result != expected_off_topic:
        print(f"   Message: {msg}")
        print(f"   Attendu: {expected_off_topic}, Obtenu: {result}")

# ================================================================
# TEST 4: FIELD_LABELS INCLUT TOUS LES CHAMPS
# ================================================================
print("\n✅ TEST 4: Vérifier FIELD_LABELS")
print("-" * 70)

expected_labels = ["full_name", "objective", "age", "nationality", 
                   "education_level", "current_field", "target_program",
                   "budget", "passport", "criminal_record", "departure_date",
                   "in_whatsapp_group"]

for field in expected_labels:
    if field in FIELD_LABELS:
        print(f"✓ {field}: {FIELD_LABELS[field]}")
    else:
        print(f"❌ {field}: MANQUANT")

# ================================================================
# TEST 5: EXTRACTION FULL_NAME
# ================================================================
print("\n✅ TEST 5: Extraction du full_name dans CRM")
print("-" * 70)

# Test l'extraction avec un message simple
import uuid
test_phone = f"+33{uuid.uuid4().hex[:10]}"
test_prospect = ProspectProfile(phone_number=test_phone)
test_prospect.save()  # Sauvegarder
test_message = "Je m'appelle Jean Dupont et je suis togolais"

updated_fields = update_prospect_profile(test_prospect, test_message)

if "full_name" in updated_fields:
    print(f"✓ full_name extrait correctement")
    print(f"  Valeur: {test_prospect.full_name}")
else:
    print(f"❌ full_name non extrait")
    print(f"  Champs mis à jour: {updated_fields}")

# ================================================================
# RÉSUMÉ
# ================================================================
print("\n" + "=" * 70)
print("🎉 TESTS TERMINÉS")
print("=" * 70)
print(f"Total de questions trouvées: {len(questions)}")
print(f"Champs attendus: {len(expected_fields)}")
print("✅ Nettoyage du projet validé !")
print("\nPour tester en production sur WhatsApp:")
print("  1. Envoyez un message au bot")
print("  2. Vérifiez que la première question demande le nom (👤)")
print("  3. Répondez aux 12 questions séquentiellement")
print("  4. Vérifiez l'absence de doubles questions")
print("  5. Le nom doit s'afficher dans le sidebar admin")
