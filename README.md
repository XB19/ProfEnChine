# Le Prof en Chine

Ce dépôt contient deux projets indépendants :

## [`whatsapp_agent/`](whatsapp_agent/)

L'application Django : agent IA WhatsApp de qualification des prospects + dashboard administrateur.
Déployée sur Render. Voir les fichiers `*.md` à l'intérieur du dossier pour l'historique technique.

- Démarrer en local : `cd whatsapp_agent && ../venv/Scripts/python.exe manage.py runserver`
- Variables d'environnement : `whatsapp_agent/config/.env` (non versionné)
- Sur Render : le champ **Root Directory** du service doit être réglé sur `whatsapp_agent`

## [`site_vitrine/`](site_vitrine/)

Le site vitrine public (présentation de "Le Prof en Chine", programmes, bourses, contact WhatsApp).
Site statique (HTML/CSS/JS), aucun backend requis.

- Ouvrir en local : ouvrir `site_vitrine/index.html` dans un navigateur
