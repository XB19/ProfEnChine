from django.http import JsonResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from conversations.models import Conversation, ProspectProfile
from ai_engine.models import Document

from ai_engine.services.ai_chat import ask_ai
from ai_engine.utils.pdf_utils import extract_pdf_text


# =========================
# CHAT IA ENDPOINT
# =========================
@api_view(['POST'])
def chat_with_ai(request):

    message = request.data.get("message")
    phone_number = request.data.get("phone_number", "test_user")

    if not message:
        return Response({"error": "message manquant"}, status=400)

    # =========================
    # GET OR CREATE PROSPECT
    # =========================
    prospect, _ = ProspectProfile.objects.get_or_create(
        phone_number=phone_number
    )

    # =========================
    # SAVE USER MESSAGE (CRM PROPRE)
    # =========================
    Conversation.objects.create(
        prospect=prospect,
        role='user',
        message=message
    )

    # =========================
    # HUMAN TAKEOVER CHECK
    # =========================
    if prospect.human_takeover:
        return Response({
            "response": "Conversation prise en charge par un conseiller humain."
        })

    # =========================
    # AI RESPONSE
    # =========================
    ai_response = ask_ai(phone_number, prospect, message)

    # =========================
    # SAVE AI RESPONSE
    # =========================

    return Response({
        "response": ai_response
    })


# =========================
# PDF UPLOAD + ANALYSE
# =========================
def upload_pdf(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    file = request.FILES.get("file")
    title = request.POST.get("title", "document")

    if not file:
        return JsonResponse({"error": "file manquant"}, status=400)

    doc = Document.objects.create(
        title=title,
        file=file
    )

    # =========================
    # EXTRACTION TEXTE PDF
    # =========================
    file_path = doc.file.path
    text = extract_pdf_text(file_path)

    doc.content = text
    doc.save()

    return JsonResponse({
        "message": "PDF uploadé et analysé",
        "doc_id": doc.id
    })