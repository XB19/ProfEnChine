#!/usr/bin/env python
"""
SCRIPT DE VALIDATION FINAL - LE PROF EN CHINE
Vérifie que tout est correct avant déploiement
"""

import os
import sys
import subprocess
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from conversations.models import ProspectProfile, Conversation
from ai_engine.services.conversation import get_next_question
from ai_engine.services.filters import is_invalid_message, is_off_topic, get_off_topic_message
from ai_engine.services.ai_chat import FIELD_LABELS, ask_ai
import uuid

print("=" * 80)
print("🔍 VALIDATION FINALE - LE PROF EN CHINE")
print("=" * 80)

checks_passed = 0
checks_failed = 0

def check(description, result):
    global checks_passed, checks_failed
    if result:
        print(f"✅ {description}")
        checks_passed += 1
    else:
        print(f"❌ {description}")
        checks_failed += 1
    return result

# ================================================================
# 1. DJANGO CHECK
# ================================================================
print("\n📋 1️⃣ Django System Check")
print("-" * 80)
result = subprocess.run(
    ["python", "manage.py", "check"],
    capture_output=True,
    text=True
)
check("Django santé générale", result.returncode == 0)

# ================================================================
# 2. LES 12 QUESTIONS
# ================================================================
print("\n📋 2️⃣ Questions de Qualification")
print("-" * 80)

test_prospect = ProspectProfile(phone_number=f"+33{uuid.uuid4().hex[:10]}")
test_prospect.save()

questions = []
for i in range(20):
    q = get_next_question(test_prospect)
    if q is None:
        break
    questions.append(q)
    if hasattr(test_prospect, 'current_step') and test_prospect.current_step:
        setattr(test_prospect, test_prospect.current_step, f"test_{i}")

check("12 questions présentes", len(questions) == 12)
check("Première question demande le nom (👤)", "👤" in questions[0])
check("Deuxième question est l'objectif (1️⃣)", "1️⃣" in questions[1])
check("Dernière question est le WhatsApp (1️⃣1️⃣)", "1️⃣1️⃣" in questions[11])

# ================================================================
# 3. FIELD_LABELS
# ================================================================
print("\n📋 3️⃣ Étiquettes des Champs")
print("-" * 80)

required_fields = [
    "full_name", "objective", "age", "nationality", 
    "education_level", "current_field", "target_program",
    "budget", "passport", "criminal_record", "departure_date",
    "in_whatsapp_group"
]

for field in required_fields:
    check(f"FIELD_LABELS contient '{field}'", field in FIELD_LABELS)

# ================================================================
# 4. FILTRES OFF-TOPIC
# ================================================================
print("\n📋 4️⃣ Détection Hors-Contexte")
print("-" * 80)

check(
    "Question hors sujet détectée",
    is_off_topic("Pourquoi le ciel est bleu ?") == True
)
check(
    "Question valide pas rejetée",
    is_off_topic("Combien ça coûte en Chine ?") == False
)
check(
    "Message off-topic a réponse",
    "Je suis l'agent IA" in get_off_topic_message()
)
check(
    "Message bloqué rejeté",
    is_invalid_message("hack bitcoin") == True
)

# ================================================================
# 5. EXTRACTION CRM
# ================================================================
print("\n📋 5️⃣ Extraction Profil (CRM)")
print("-" * 80)

test_prospect2 = ProspectProfile(phone_number=f"+33{uuid.uuid4().hex[:10]}")
test_prospect2.save()

from ai_engine.services.crm import update_prospect_profile

updated = update_prospect_profile(
    test_prospect2,
    "Je m'appelle Alice Martin, togolaise, 25 ans, j'étudie l'informatique"
)

check("full_name extrait (Alice Martin)", "full_name" in updated or test_prospect2.full_name == "Alice Martin")
check("nationality extrait (Togo)", "nationality" in updated or test_prospect2.nationality == "Togo")
check("age extrait (25)", "age" in updated or test_prospect2.age == 25)

# ================================================================
# 6. SIDEBAR ADMIN
# ================================================================
print("\n📋 6️⃣ Affichage Admin (Sidebar)")
print("-" * 80)

with open("dashboard/templates/dashboard/prospects/detail.html", "r", encoding="utf-8") as f:
    template_content = f.read()

check("Template contient {{ prospect.full_name }}", "prospect.full_name" in template_content)
check("Template affiche l'emoji 👤", "👤" in template_content)
check("Template a section identité", "Identité" in template_content or "IDENTITÉ" in template_content)

# ================================================================
# 7. FICHIERS MODIFIÉS
# ================================================================
print("\n📋 7️⃣ Fichiers Clés Présents")
print("-" * 80)

files_to_check = [
    "ai_engine/services/conversation.py",
    "ai_engine/services/ai_chat.py",
    "ai_engine/services/filters.py",
    "ai_engine/services/crm.py",
    "ai_engine/services/prompts.py",
    "dashboard/templates/dashboard/prospects/detail.html",
    "test_cleanup_flow.py",
    "CLEANUP_REPORT.md",
    "DEPLOYMENT_CHECKLIST.md",
]

for filepath in files_to_check:
    check(f"Fichier existe: {filepath}", os.path.exists(filepath))

# ================================================================
# 8. SYNTAXE PYTHON
# ================================================================
print("\n📋 8️⃣ Syntaxe Python")
print("-" * 80)

python_files = [
    "ai_engine/services/conversation.py",
    "ai_engine/services/ai_chat.py",
    "ai_engine/services/filters.py",
    "ai_engine/services/crm.py",
    "ai_engine/services/prompts.py",
]

for py_file in python_files:
    result = subprocess.run(
        ["python", "-m", "py_compile", py_file],
        capture_output=True,
        text=True
    )
    check(f"Syntaxe correcte: {py_file}", result.returncode == 0)

# ================================================================
# RÉSUMÉ FINAL
# ================================================================
print("\n" + "=" * 80)
print("📊 RÉSUMÉ FINAL")
print("=" * 80)

total_checks = checks_passed + checks_failed
percentage = (checks_passed / total_checks * 100) if total_checks > 0 else 0

print(f"\n✅ Vérifications réussies: {checks_passed}/{total_checks}")
print(f"❌ Vérifications échouées: {checks_failed}/{total_checks}")
print(f"📈 Taux de réussite: {percentage:.1f}%")

if checks_failed == 0:
    print("\n" + "🎉" * 20)
    print("✅ TOUS LES TESTS PASSENT - PRÊT POUR PRODUCTION !")
    print("🎉" * 20)
    sys.exit(0)
else:
    print("\n⚠️  CERTAINS TESTS ONT ÉCHOUÉ - VÉRIFIEZ LES ERREURS CI-DESSUS")
    sys.exit(1)
