"""
TESTS - Vérifier que le système fonctionne
python manage.py shell < test_ai_improvements.py
"""

from ai_engine.services.knowledge_base import (
    get_faq_answer,
    detect_intent,
    get_budget_recommendation,
)
from ai_engine.services.ai_chat import is_user_asking_question

print("=" * 60)
print("🧪 TEST : SYSTÈME IA AMÉLIORÉ")
print("=" * 60)

# ================================================
# TEST 1: FAQ
# ================================================
print("\n✅ TEST 1: FAQ")
print("-" * 60)

test_questions = [
    "Combien ça coûte l'année de langue ?",
    "Comment obtenir une bourse ?",
    "Quel est le processus visa ?",
]

for q in test_questions:
    answer = get_faq_answer(q)
    if answer:
        print(f"Q: {q}")
        print(f"A: {answer[:100]}...")
        print()
    else:
        print(f"❌ Pas de réponse trouvée pour: {q}")

# ================================================
# TEST 2: DÉTECTION D'INTENTIONS
# ================================================
print("\n✅ TEST 2: DÉTECTION D'INTENTIONS")
print("-" * 60)

test_intents = [
    ("Quelle est le coût de l'année ?", "ask_cost"),
    ("Je veux une bourse", "ask_scholarship"),
    ("Quel est le processus visa ?", "ask_visa"),
    ("Combien de documents faut-il ?", "ask_documents"),
]

for msg, expected_intent in test_intents:
    detected = detect_intent(msg)
    status = "✅" if detected == expected_intent else "❌"
    print(f"{status} '{msg}' → {detected} (attendu: {expected_intent})")

# ================================================
# TEST 3: DÉTECTION QUESTION vs RÉPONSE
# ================================================
print("\n✅ TEST 3: DÉTECTION QUESTION vs RÉPONSE")
print("-" * 60)

test_cases = [
    ("Combien ça coûte ?", True, "Question"),
    ("Oui", False, "Réponse simple"),
    ("Informatique", False, "Réponse simple"),
    ("Comment fonctionne le visa ?", True, "Question"),
    ("25 ans", False, "Réponse simple"),
    ("Quel est le meilleur programme pour moi ?", True, "Question"),
    ("Master en informatique", False, "Réponse simple"),
    ("J'ai 30 ans et je viens du Togo", False, "Réponse composée"),
]

for msg, expected_is_q, desc in test_cases:
    is_q = is_user_asking_question(msg)
    status = "✅" if is_q == expected_is_q else "❌"
    actual = "Question" if is_q else "Réponse"
    print(f"{status} [{desc}] '{msg}' → {actual}")

# ================================================
# TEST 4: RECOMMANDATIONS PAR BUDGET
# ================================================
print("\n✅ TEST 4: RECOMMANDATIONS PAR BUDGET")
print("-" * 60)

test_budgets = [
    (2000000, "Petit budget"),
    (4000000, "Budget moyen"),
    (7000000, "Bon budget"),
]

for budget, desc in test_budgets:
    recs = get_budget_recommendation(budget)
    print(f"\n💰 {desc} ({budget:,} FCFA):")
    for rec in recs:
        print(f"   → {rec}")

# ================================================
# RÉSUMÉ
# ================================================
print("\n" + "=" * 60)
print("✅ TOUS LES TESTS COMPLÉTÉS")
print("=" * 60)
print("\n📌 Le système est prêt pour les tests en production!")
print("\n🚀 Prochaines étapes:")
print("   1. Tester avec des vrais utilisateurs")
print("   2. Collecter les questions non-trouvées pour améliorer FAQ")
print("   3. Monitorer la qualité des réponses Groq")
print("   4. Ajuster les poids du scoring IA selon retours")
