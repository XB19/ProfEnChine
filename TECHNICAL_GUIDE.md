# 📖 GUIDE TECHNIQUE - AGENT IA "LE PROF EN CHINE"

## 🚀 DÉPLOIEMENT RAPIDE

### 1. Installation & Test

```bash
# Aller dans le dossier du projet
cd e:\leprof_ai

# Vérifier la syntaxe
python -m py_compile ai_engine/services/knowledge_base.py
python -m py_compile ai_engine/services/profile_analyzer.py
python -m py_compile ai_engine/services/ai_chat.py

# Lancer les tests
python manage.py shell < test_ai_improvements.py
```

### 2. Déploiement production

```bash
# Vérifier que tout fonctionne
python manage.py test

# Si OK, déployer
python manage.py migrate  # Si changements BD
python manage.py runserver

# Tester avec WhatsApp
# Envoyer message de test au bot
```

---

## 🔧 ARCHITECTURE

### Structure des fichiers

```
ai_engine/services/
├── ai_chat.py                    # MAIN - Orchestration IA
├── knowledge_base.py             # 🆕 Base de connaissances
├── profile_analyzer.py           # 🆕 Analyse de profil
├── crm.py                        # Mise à jour CRM
├── conversation.py               # Questions de qualification
├── extractor.py                  # Extraction profil (Groq)
├── prompts.py                    # Prompts système
├── router.py                     # Routage messages
└── ...
```

---

## 📚 UTILISATION : AJOUTER DES FAQ

### Ajouter une nouvelle FAQ

**Fichier:** `ai_engine/services/knowledge_base.py`

**Trouver la section FAQ :**
```python
FAQ = {
    "how_much_cost": {
        "keywords": ["coûte", "prix", "budget", "frais", "combien"],
        "answer": """💰 **Budget estimatif par programme :**
        ...
        """
    },
    # ← AJOUTER ICI
}
```

**Exemple : Ajouter "Puis-je apporter ma famille ?"**
```python
"family_abroad": {
    "keywords": ["famille", "enfant", "femme", "époux", "dépendant"],
    "answer": """👨‍👩‍👧 **Accompagnants en Chine :**
    
Vous pouvez amener votre famille, mais avec certaines conditions :

✅ **Époux(se)** : Visa accompagnant disponible
✅ **Enfants** : Peuvent vous accompagner
✅ **Conditions** : Vous devez avoir un logement adapté

📌 Les frais supplémentaires :
- Visa époux/enfants : ~19k-50k FCFA
- Logement supplémentaire : +150k-400k FCFA/mois

💡 Recommandation : Discuter avec l'université avant de planifier.
    """
},
```

**Keyword matching automatique :**
```
"Puis-je apporter ma femme ?" → détecte "femme" → retourne réponse FAQ
"Je veux venir avec mes enfants" → détecte "enfants" → retourne réponse FAQ
```

---

## 🔄 AJOUTER DES OBJECTIONS

**Fichier:** `ai_engine/services/knowledge_base.py`

**Section OBJECTION_RESPONSES :**
```python
OBJECTION_RESPONSES = {
    "no_money": { ... },  # Existant
    # ← AJOUTER ICI
}
```

**Exemple : Objection "J'ai des doutes"**
```python
"doubt_about_choice": {
    "objection": "Je ne suis pas sûr(e)",
    "response": """Doutes tout à fait normaux ! 😊

Voici pourquoi choisir la Chine :

✅ **Diplôme reconnu** mondialement
✅ **Coûts réduits** vs Europe/Amériques
✅ **Opportunités** énormes (tech, business, recherche)
✅ **Culture** incroyable à découvrir
✅ **Réseau** international permanent

📌 Comment nous aidons :
- Analyse complète de votre profil
- Matching universités parfaites
- Support à CHAQUE étape
- Garantie entrée en Chine

Êtes-vous prêt(e) à explorer cette opportunité ? 😊""",
},
```

---

## 🎯 AMÉLIORER LE SCORING IA

**Fichier:** `ai_engine/services/profile_analyzer.py`

**Fonction:** `analyze_profile(prospect) → dict`

**Poids actuels :**
```python
score += 15  # Passeport
score += 20  # Master
score += 25  # Doctorat
score += 10  # Budget réduit
score += 20  # Bon budget
score += 10  # Jeune
```

**Ajuster les poids selon retours :**
```python
# Exemple: Si Master est sous-score
score += 25  # Augmenter de 20 → 25

# Exemple: Si jeune âge moins important
score += 8   # Réduire de 10 → 8
```

**Monitoring :**
```
Regarder régulièrement :
- Quel score moyen par profil ?
- Quel score → conversion ?
- Quels avertissements récurrents ?
```

---

## 🔍 DÉBOGUER - QU'EST-CE QUI VA MAL ?

### Problème : Agent dit "Je peux seulement répondre..."

**Cause :** Question n'est pas sur études en Chine

**Solution :** Vérifier dans `ai_chat.py` la fonction `answer_general_question()`

```python
# Voir le prompt système
"Tu réponds UNIQUEMENT aux questions sur les études en Chine."
```

### Problème : FAQ ne répond pas

**Cause :** Keywords ne matchent pas

**Solution :** Ajouter plus de keywords dans `knowledge_base.py`

```python
"keywords": ["coûte", "prix", "budget", "frais", "combien", 
             "ça coûte", "c'est combien", "tarif"]  # ← Ajouter
```

### Problème : Groq donne réponse hors sujet

**Cause :** Prompt système pas assez strict

**Solution :** Renforcer dans `ai_chat.py`:

```python
"content": """Tu es "Prof en Chine". 
Tu réponds UNIQUEMENT sur études en Chine.
Si autre sujet, dis: "Je peux seulement répondre aux questions sur...
"""
```

---

## 📊 MONITORING EN PRODUCTION

### Métriques à surveiller

```
1. QUALITÉ RÉPONSES
   - Questions sans réponse FAQ
   - Temps de réponse Groq
   - Taux d'erreurs Groq
   
2. FLUX UTILISATEURS
   - % questions vs réponses
   - Intent distribution (coûts, bourses, visa, etc.)
   - Taux abandon
   
3. SCORING PROFILES
   - Score moyen
   - % excellent/bon/moyen/faible
   - Corrélation score → conversion
```

### Logs à vérifier

```python
# Dans ai_chat.py:
print(f"✅ Réponse FAQ trouvée")
print(f"✅ Réponse Groq générée")
print(f"⚠️ GROQ RATE LIMIT - Continuons...")
print(f"❌ AI ERROR : {e}")
```

---

## 🚀 AMÉLIORATIONS FUTURES

### Court terme (semaine 1-2)
- [ ] Collecter questions sans réponse → améliorer FAQ
- [ ] Ajuster scoring selon profils reçus
- [ ] Ajouter 5-10 objections courantes

### Moyen terme (mois 1)
- [ ] Intégrer avec CUCAS (vérification universités réelles)
- [ ] Dashboard candidatures (suivi utilisateurs)
- [ ] Multi-langue (français + anglais + autres)

### Long terme (mois 2+)
- [ ] API universités chinoises (données temps réel)
- [ ] Webhook WhatsApp (réponses sans délai)
- [ ] Machine learning (prédire programme optimal)
- [ ] Claude 3.5 Sonnet (qualité supérieure Groq)

---

## 💡 BONNES PRATIQUES

### ✅ À FAIRE

```python
# Ajouter keywords variées
"keywords": ["coûte", "prix", "budget", "combien", "tarif", 
             "ça coûte", "c'est combien"]

# Réponses concises (max 150 mots)
"answer": "Réponse courte et actionnable..."

# Toujours avec appel à action
"Souhaitez-vous en savoir plus ?"

# Tester avant production
python manage.py shell < test_ai_improvements.py
```

### ❌ À ÉVITER

```python
# Réponses vagues
"answer": "C'est compliqué, ça dépend..."

# Trop d'informations
"answer": "[1000 mots de détails...]"

# Sans CTA
"answer": "Voilà l'information." # ← Ajouter question

# Keywords trop spécifiques
"keywords": ["très long et compliqué"]  # ← Généraliser
```

---

## 🧪 TESTER LOCALEMENT

### Test simple en Django shell

```bash
python manage.py shell

>>> from ai_engine.services.knowledge_base import get_faq_answer
>>> get_faq_answer("Combien ça coûte l'année de langue ?")
'💰 **Budget estimatif...'

>>> from ai_engine.services.ai_chat import is_user_asking_question
>>> is_user_asking_question("Oui")
False

>>> is_user_asking_question("Comment ça marche ?")
True
```

### Test complet

```bash
python manage.py shell < test_ai_improvements.py
```

---

## 📞 SUPPORT & HELP

### Erreurs courantes

| Erreur | Cause | Fix |
|--------|-------|-----|
| `ImportError: no module knowledge_base` | Fichier manquant | `python -m py_compile ...` |
| `GROQ_API_KEY missing` | Clé API absente | Ajouter dans `.env` |
| `Rate limit 429` | Trop de requêtes | Fallback auto (OK) |
| `KeyError: 'passport'` | Champ CRM manquant | Migrer DB |

---

## 🎓 CONCLUSION

Votre agent IA est maintenant :
✅ **Vraiment dynamique** (questions + réponses + qualification)
✅ **Intelligent** (FAQ + Groq + profil)
✅ **Scalable** (facile ajouter contenus)
✅ **Prêt production** (testé et validé)

Bon déploiement ! 🚀🇨🇳
