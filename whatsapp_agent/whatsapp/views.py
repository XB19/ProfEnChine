import mimetypes
import os
import json
import requests

from django.core.files.base import ContentFile
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from conversations.models import Conversation, ProspectProfile
from ai_engine.models import Document
from ai_engine.services.router import ask_smart_ai
from ai_engine.utils.pdf_utils import extract_pdf_text


# =========================
# ENV
# =========================
# Les variables d'environnement sont déjà chargées de façon centralisée par
# config/settings.py (load_dotenv sur le chemin explicite config/.env).
VERIFY_TOKEN = (os.getenv("WHATSAPP_VERIFY_TOKEN") or "").strip()
WHATSAPP_TOKEN = (os.getenv("WHATSAPP_TOKEN") or "").strip()
PHONE_NUMBER_ID = (os.getenv("WHATSAPP_PHONE_NUMBER_ID") or "").strip()


# ==========================================================
# SEND MESSAGE SAFE
# ==========================================================

def send_whatsapp_message(to, message):

    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("❌ Missing WhatsApp config")
        return

    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": (message or "")[:4000]}
    }

    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception as e:
        print("❌ SEND ERROR:", e)


# ==========================================================
# DOWNLOAD MEDIA (document ou image) SAFE
# ==========================================================

def download_whatsapp_media(file_id):
    """
    Télécharge un média WhatsApp (document OU image) par son id.
    Retourne (contenu_bytes, mime_type) ou (None, None) en cas d'échec.
    """

    try:
        url = f"https://graph.facebook.com/v22.0/{file_id}"

        headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}"}

        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            print("❌ META ERROR:", r.text)
            return None, None

        meta = r.json()
        file_url = meta.get("url")
        if not file_url:
            return None, None

        media = requests.get(
            file_url,
            headers={"Authorization": f"Bearer {WHATSAPP_TOKEN}"},
            timeout=20
        )

        if media.status_code != 200:
            print("❌ DOWNLOAD ERROR:", media.text)
            return None, None

        mime_type = meta.get("mime_type") or media.headers.get("Content-Type") or "application/octet-stream"

        return media.content, mime_type

    except Exception as e:
        print("❌ MEDIA ERROR:", e)
        return None, None


# ==========================================================
# SAFE META PARSER
# ==========================================================

def extract_message(body):
    """
    Extraction robuste Meta WhatsApp
    """
    try:
        entry = body.get("entry", [])
        if not entry:
            return None

        changes = entry[0].get("changes", [])
        if not changes:
            return None

        value = changes[0].get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return None

        return messages[0]

    except Exception:
        return None
    





# ==========================================================
# WEBHOOK
# ==========================================================

@csrf_exempt
def webhook(request):

    # =========================
    # VERIFY META
    # =========================
    if request.method == "GET":
        if request.GET.get("hub.verify_token") == VERIFY_TOKEN:
            return HttpResponse(request.GET.get("hub.challenge"))
        return HttpResponse("Forbidden", status=403)

    # =========================
    # RECEIVE MESSAGE
    # =========================
    if request.method == "POST":

        try:
            body = json.loads(request.body.decode("utf-8"))

            msg = extract_message(body)
            if not msg:
                return JsonResponse({"status": "no_message"})

            phone = msg.get("from")
            msg_type = msg.get("type")

            text = ""
            doc_id = None

            # =========================
            # PROSPECT
            # =========================
            prospect, created = ProspectProfile.objects.get_or_create(
                phone_number=phone
            )

            # ==================================================
            # FIRST TIME USER → WELCOME + CONSENT FLOW
            # ==================================================
            if created:

                prospect.current_step = "consent"
                prospect.save(update_fields=["current_step"])

                welcome = (
                    "👋 Bonjour et bienvenue chez Le Prof en Chine ! 🇨🇳\n\n"
                    "Le Prof en Chine vous aide à préparer votre préinscription pour étudier en Chine : \n"
                    "👉 on analyse votre profil,\n"
                    "👉 on identifie les programmes et filières adaptés,\n"
                    "👉 on vous accompagne vers les meilleures options d'admission.\n\n"
                    "Avant de commencer, puis-je recueillir vos informations pour lancer votre préinscription ?\n\n"
                    "Répondez simplement : Oui ou Non"
                )

                Conversation.objects.create(
                    prospect=prospect,
                    role="assistant",
                    message=welcome
                )

                send_whatsapp_message(phone, welcome)

                return JsonResponse({"status": "welcome_sent"})

            # ==================================================
            # TEXT MESSAGE
            # ==================================================
            if msg_type == "text":
                text = (msg.get("text", {}).get("body") or "").strip()

                Conversation.objects.create(
                    prospect=prospect,
                    role="user",
                    message=text
                )

            # ==================================================
            # DOCUMENT OU IMAGE (passeport, casier, diplôme, photo...)
            # ==================================================
            elif msg_type in ("document", "image"):

                media_info = msg.get(msg_type, {})
                file_id = media_info.get("id")
                mime_type = media_info.get("mime_type") or ""

                content, downloaded_mime = download_whatsapp_media(file_id)
                mime_type = mime_type or downloaded_mime or ""

                if not content:
                    return JsonResponse({"status": "media_download_failed"})

                is_pdf = "pdf" in mime_type.lower()

                extension = mimetypes.guess_extension(mime_type) or (".pdf" if is_pdf else ".bin")
                filename = media_info.get("filename") or f"{file_id}{extension}"

                doc = Document(prospect=prospect, title=filename)
                doc.file.save(filename, ContentFile(content), save=False)
                doc.save()

                Conversation.objects.create(
                    prospect=prospect,
                    role="user",
                    message=f"[DOCUMENT REÇU : {filename}]"
                )

                if is_pdf:
                    # Vrai PDF : on tente l'extraction de texte pour permettre
                    # l'analyse par l'IA (ask_pdf_ai).
                    try:
                        doc.content = extract_pdf_text(doc.file.path)
                        doc.save(update_fields=["content"])
                        doc_id = doc.id
                        text = "Analyse document PDF"
                    except Exception as e:
                        # Fichier envoyé en "document" mais pas un vrai PDF
                        # exploitable (ex: PNG/JPEG partagé comme fichier) :
                        # on ne fait pas planter le webhook, on accuse
                        # simplement réception.
                        print("⚠️ PDF EXTRACT ERROR:", e)
                        is_pdf = False

                if not is_pdf:
                    # Image (photo de passeport, diplôme scanné en JPEG...) :
                    # pas d'extraction de texte, juste un accusé de réception.
                    ack = (
                        "✅ Document bien reçu, merci ! Il a été transmis à "
                        "notre équipe pour la préparation de votre dossier."
                    )

                    Conversation.objects.create(
                        prospect=prospect,
                        role="assistant",
                        message=ack
                    )

                    send_whatsapp_message(phone, ack)

                    return JsonResponse({"status": "document_received"})

            # ==================================================
            # AI CALL
            # ==================================================
            # NOTE : la mise à jour du profil (extraction + score) est
            # déjà effectuée à l'intérieur de ask_ai()/ask_smart_ai() pour
            # les messages texte. Un second appel ici dupliquait
            # l'extraction et empêchait les messages de confirmation
            # ("✅ Merci, ... a bien été enregistré") de s'afficher, car le
            # champ était déjà rempli avant l'appel interne.
            ai_response = ask_smart_ai(
                phone_number=phone,
                message_type=msg_type,
                prospect=prospect,
                message_content=text,
                doc_id=doc_id
            )

            # ==================================================
            # SAVE AI RESPONSE
            # ==================================================
            Conversation.objects.create(
                prospect=prospect,
                role="assistant",
                message=ai_response
            )

            # ==================================================
            # SEND TO WHATSAPP
            # ==================================================
            send_whatsapp_message(phone, ai_response)

            return JsonResponse({"status": "success"})

        except Exception as e:
            print("❌ WEBHOOK ERROR:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "method_not_allowed"}, status=405)