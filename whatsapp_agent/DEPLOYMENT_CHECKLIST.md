# 🚀 CHECKLIST DE DÉPLOIEMENT - LE PROF EN CHINE

**Version:** 2.0 (Post-Cleanup)  
**Date:** 2025  

---

## ✅ PRÉ-DÉPLOIEMENT (Avant de mettre en production)

### 1. Validation du code

- [ ] Exécuter: `python manage.py check`
  - Expected: "System check identified no issues"

- [ ] Exécuter: `python test_cleanup_flow.py`
  - Expected: "🎉 TESTS TERMINÉS - ✅ Nettoyage du projet validé !"

- [ ] Vérifier les 12 questions présentes

### 2. Vérification des fichiers clés

- [ ] ✅ `conversation.py` - 12 questions (full_name en Q0)
- [ ] ✅ `ai_chat.py` - Imports is_off_topic, FIELD_LABELS complet
- [ ] ✅ `filters.py` - Fonction is_off_topic() présente
- [ ] ✅ `crm.py` - Pas d'erreur last_question.lower()
- [ ] ✅ `prompts.py` - full_name dans JSON extraction
- [ ] ✅ `detail.html` - full_name dans sidebar

### 3. Nettoyage base de données (OPTIONNEL)

```bash
# Si vous voulez réinitialiser les anciens tests:
python manage.py shell
>>> from conversations.models import ProspectProfile
>>> ProspectProfile.objects.filter(phone_number__startswith="+33").delete()
```

---

## 🎯 TESTS EN PRODUCTION

### Scenario 1: Premier contact (Nouveau prospect)

**Action:** Envoyez "Bonjour" au bot  
**Attendu:**
1. ✅ Q0: "👤 Quel est votre nom complet ?"
2. Bot ne doit PAS demander objectif tout de suite

**Réponse client:** "Jean Dupont"  
**Attendu:** 
- ✅ Nom sauvegardé
- ✅ Q1: "1️⃣ Voulez-vous immigrer ou étudier ?"

### Scenario 2: Réponses séquentielles

**Flow complet:**

```
👤 Quel est votre nom complet ?
User: Jean Dupont
✅ Merci

1️⃣ Immigrer ou Étudier ?
User: Étudier
✅ Merci

2️⃣ Niveau d'études souhaité ?
User: Master
✅ Merci

3️⃣ Filière souhaitée ?
User: Informatique
✅ Merci

4️⃣ Niveau d'étude actuel ?
User: Licence
✅ Merci

5️⃣ Quel âge avez-vous ?
User: 25
✅ Merci

6️⃣ Nationalité ?
User: Togolais
✅ Merci

7️⃣ Passeport valide ?
User: Oui
✅ Merci

8️⃣ Casier judiciaire vierge ?
User: Oui
✅ Merci

9️⃣ Date de départ ?
User: Septembre 2026
✅ Merci

🔟 Budget approximatif ?
User: 5 millions FCFA
✅ Merci

1️⃣1️⃣ Groupe WhatsApp ?
User: Non
✅ Merci - Dossier complet !

[Message d'analyse du profil]
```

**Vérification:**
- [ ] 12 questions posées en séquence
- [ ] Pas de doublons
- [ ] Pas de saut de questions
- [ ] Pas de numérotation incorrecte

### Scenario 3: Détection Hors-Sujet

**Action:** Utilisateur demande "Pourquoi le ciel est bleu ?"  
**Attendu:** 
- ✅ Réponse: "📌 Je suis l'agent IA... spécialisé uniquement dans les études en Chine"
- ✅ Bot recommande une question sur Chine

**Action:** Utilisateur demande "Combien ça coûte en Chine ?"  
**Attendu:**
- ✅ Question valide détectée (contient "coûte" + "Chine")
- ✅ Réponse normale + continuité du questionnaire

### Scenario 4: Vérification Admin

**Action:** Aller dans l'admin Django > Prospects  
**Attendu:**
- [ ] Cliquez sur un prospect
- [ ] Vérifiez sidebar: `👤 Nom: Jean Dupont`
- [ ] Nom s'affiche correctement
- [ ] Pas d'erreur

### Scenario 5: Extraction Complète

**Envoyez:** "Je suis Aminata Traore, togolaise, 23 ans, je veux étudier l'informatique en Chine, j'ai un master en génie logiciel, mon budget est 3 millions FCFA, et j'ai mon passeport"

**Attendu:**
- [x] full_name: "Aminata Traore"
- [x] nationality: "Togo"
- [x] age: 23
- [x] target_program: "Informatique"
- [x] education_level: "Master"
- [x] budget: 3000000
- [x] passport: "Oui"
- [x] CRM MIS À JOUR AUTOMATIQUEMENT

---

## 🐛 DÉBOGAGE - Si quelque chose ne fonctionne pas

### Problème 1: "Bot ne pose pas le nom"
**Solution:**
```bash
# Vérifier que conversation.py a la Q0
grep -n "full_name" ai_engine/services/conversation.py
# Doit trouver: "if is_missing(getattr(prospect, "full_name", None)):"
```

### Problème 2: "Questions dupliquées"
**Solution:**
```bash
# Lancer le test
python test_cleanup_flow.py
# Chercher "TEST 1" - doit trouver exactement 12 questions
```

### Problème 3: "Messages hors sujet ne sont pas détectés"
**Solution:**
```bash
python manage.py shell
>>> from ai_engine.services.filters import is_off_topic
>>> is_off_topic("Pourquoi le ciel est bleu ?")
True  # Doit retourner True
>>> is_off_topic("Combien ça coûte en Chine ?")
False  # Doit retourner False
```

### Problème 4: "Nom ne s'affiche pas en admin"
**Solution:**
```bash
# Vérifier le template
grep -n "full_name" dashboard/templates/dashboard/prospects/detail.html
# Doit trouver le code HTML avec {{ prospect.full_name }}
```

### Problème 5: "Erreur: 'NoneType' object has no attribute 'lower'"
**Solution:** C'est une erreur antérieure qui a été CORRIGÉE dans crm.py.  
Mettez à jour si vous voyez cette erreur:
```python
# ANCIEN (BUG):
if last_question and "filière" in last_question.lower() or "domaine" in last_question.lower():

# NOUVEAU (CORRECT):
last_question_lower = last_question.lower() if last_question else ""
if last_question_lower and ("filière" in last_question_lower or "domaine" in last_question_lower):
```

---

## 📊 MONITORING POST-DÉPLOIEMENT

### Métriques à surveiller:

1. **Taux de complétion des 12 questions**
   - Cible: > 80% des utilisateurs
   - Alerte si < 50%

2. **Erreurs hors-sujet**
   - Cible: < 5% de faux positifs
   - Monitor si trop de gens reçoivent "hors sujet" à tort

3. **Extraction du nom**
   - Cible: 100% des noms extraits correctement
   - Alerte si certains noms = NULL

4. **Doublons de questions**
   - Cible: 0 doublons
   - Alerte immédiate si présent

### SQL pour vérifier:

```sql
-- Vérifier que tous les prospects ont un nom
SELECT COUNT(*) as total, 
       COUNT(full_name) as avec_nom,
       COUNT(full_name) * 100 / COUNT(*) as pct_avec_nom
FROM conversations_prospectprofile;

-- Vérifier la complétude des dossiers
SELECT COUNT(*) as complets
FROM conversations_prospectprofile
WHERE dossier_complet = true;

-- Vérifier les doublons (ne doit être 0)
SELECT count(*) as doublons
FROM conversations_prospectprofile
WHERE phone_number IN (
  SELECT phone_number FROM conversations_prospectprofile 
  GROUP BY phone_number HAVING count(*) > 1
);
```

---

## 🎓 DOCUMENTATION UTILISATEUR

### Pour les prospects WhatsApp:

```
Bienvenue! 👋

Je suis Prof en Chine, votre agent IA pour préparer votre admission en Chine.

✅ Je vais vous poser 12 questions pour analyser votre profil
⏱️ Ça prend environ 5-10 minutes
✨ À la fin, vous recevrez une analyse personnalisée

Commençons ! 😊

👤 Quel est votre nom complet ?
```

---

## ✨ CONFIRMATION FINALE

**Avant de déployer, confirmez:**

- [ ] ✅ Tous les tests passent
- [ ] ✅ Django check = 0 errors
- [ ] ✅ Les 12 questions présentes
- [ ] ✅ Pas de messages d'erreur Python
- [ ] ✅ Sidebar affiche le nom
- [ ] ✅ Détection hors-sujet fonctionne

**Si tout est ✅, vous êtes prêt pour la production !**

---

## 📞 SUPPORT

Si vous avez des problèmes:

1. Exécutez `python test_cleanup_flow.py` - cherchez les erreurs
2. Exécutez `python manage.py check` - cherchez les warnings Django
3. Consultez `CLEANUP_REPORT.md` pour les détails techniques
4. Vérifiez les logs du serveur Django

---

**Dernière mise à jour:** 2025  
**Status:** ✅ PRÊT POUR PRODUCTION  
**Version:** 2.0
