from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Max

from conversations.models import Conversation, ProspectProfile
from whatsapp.views import send_whatsapp_message


# =========================
# DASHBOARD HOME
# =========================
@login_required
def dashboard_home(request):

    prospects = ProspectProfile.objects.all()

    prospects_count = prospects.count()
    conversations_count = Conversation.objects.count()

    hot_count = prospects.filter(status="hot").count()
    warm_count = prospects.filter(status="warm").count()
    cold_count = prospects.filter(status="cold").count()
    completed_count = prospects.filter(dossier_complet=True).count()

    latest_prospects = (
        prospects
        .order_by("-updated_at")[:10]
    )

    return render(request, "dashboard/dashboard.html", {
        "prospects": prospects_count,
        "conversations": conversations_count,
        "hot_count": hot_count,
        "warm_count": warm_count,
        "cold_count": cold_count,
        "completed_count": completed_count,
        "latest_prospects": latest_prospects
    })

# =========================
# LISTE PROSPECTS
# =========================
@login_required
def prospects_list(request):

    search = request.GET.get("search", "")

    prospects = ProspectProfile.objects.all()

    if search:
        prospects = prospects.filter(phone_number__icontains=search)

    for p in prospects:

        p.total_messages = p.conversations.count()

        last_msg = p.conversations.order_by("-created_at").first()
        p.last_message = last_msg.created_at if last_msg else None

    hot = prospects.filter(status="hot").order_by("-ai_score")
    warm = prospects.filter(status="warm").order_by("-ai_score")
    cold = prospects.filter(status="cold").order_by("-created_at")
    completed = prospects.filter(dossier_complet=True)

    return render(request, "dashboard/prospects/list.html", {
        "hot": hot,
        "warm": warm,
        "cold": cold,
        "completed": completed,
        "search": search
    })


# =========================
# DETAIL PROSPECT
# =========================
from django.utils import timezone
from ai_engine.scoring import calculate_ai_score
from ai_engine.status import determine_status


@login_required
def prospect_detail(request, phone_number):

    prospect = get_object_or_404(
        ProspectProfile,
        phone_number=phone_number
    )

    # 🔥 FORCE SYNC SCORE À CHAQUE OUVERTURE
    score = calculate_ai_score(prospect)
    prospect.ai_score = score
    prospect.status = determine_status(score)
    prospect.save(update_fields=["ai_score", "status"])

    if request.method == "POST":

        admin_message = request.POST.get("admin_message")

        if admin_message:

            Conversation.objects.create(
                prospect=prospect,
                role="assistant",
                message=admin_message
            )

            send_whatsapp_message(phone_number, admin_message)

            prospect.last_followup = timezone.now()
            prospect.save(update_fields=["last_followup"])

            return redirect("prospect_detail", phone_number=phone_number)

    conversations = prospect.conversations.order_by("created_at")
    documents = prospect.documents.order_by("-created_at")

    return render(request, "dashboard/prospects/detail.html", {
        "prospect": prospect,
        "conversations": conversations,
        "documents": documents,
    })

# =========================
# TOGGLE HUMAN TAKEOVER
# =========================
@login_required
def toggle_human_takeover(request, phone_number):

    prospect = get_object_or_404(ProspectProfile, phone_number=phone_number)

    prospect.human_takeover = not prospect.human_takeover

    if prospect.human_takeover:
        prospect.status = "warm"  # ou hot selon ton choix

    prospect.save()

    return redirect("prospect_detail", phone_number=phone_number)


# =========================
# INBOX CONVERSATIONS
# =========================
@login_required
def conversations_inbox(request):

    prospects = ProspectProfile.objects.all()

    inbox = []

    for p in prospects:

        last_msg = p.conversations.order_by("-created_at").first()

        if last_msg:
            inbox.append({
                "prospect": p,
                "last_message": last_msg.message,
                "last_time": last_msg.created_at,
                "total_messages": p.conversations.count(),
                "status": p.status
            })

    inbox = sorted(inbox, key=lambda x: x["last_time"], reverse=True)

    return render(request, "dashboard/conversations/inbox.html", {
        "inbox": inbox
    })

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.http import HttpResponse
from io import BytesIO

from conversations.models import ProspectProfile


@login_required
def download_prospect_pdf(request, phone_number):

    prospect = ProspectProfile.objects.get(phone_number=phone_number)
    prospect.refresh_from_db()

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    width, height = A4

    # =========================
    # HEADER
    # =========================
    p.setFillColorRGB(0.1, 0.1, 0.1)
    p.setFont("Helvetica-Bold", 18)
    p.drawString(180, height - 80, "DOSSIER CANDIDAT")

    p.setFont("Helvetica", 10)
    p.drawString(200, height - 100, "Le Prof en Chine - CRM IA")

    y = height - 150

    # =========================
    # SECTION FUNCTION
    # =========================
    def add_line(label, value):
        nonlocal y
        p.setFont("Helvetica-Bold", 11)
        p.drawString(60, y, f"{label}:")
        
        p.setFont("Helvetica", 11)
        p.drawString(200, y, f"{value if value else 'N/A'}")
        y -= 25

    # =========================
    # DATA CLEAN DISPLAY
    # =========================
    add_line("Objectif", prospect.objective)
    add_line("Âge", prospect.age)
    add_line("Nationalité", prospect.nationality)
    add_line("Niveau d'étude", prospect.education_level)
    add_line("Filière souhaitée", prospect.current_field)
    add_line("Programme souhaité", prospect.target_program)

    # 💰 FORMAT CFA
    budget = format_budget(prospect.budget)
    add_line("Budget", budget)

    add_line("Passeport", prospect.passport)
    add_line("Casier judiciaire", prospect.criminal_record)
    add_line("Date de départ", prospect.departure_date)
    add_line("Groupe WhatsApp", prospect.in_whatsapp_group)
    add_line("Score IA", prospect.ai_score)
    add_line("Statut", prospect.status.upper())

    # =========================
    # FOOTER
    # =========================
    p.setFont("Helvetica-Oblique", 9)


    p.showPage()
    p.save()

    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="dossier_{phone_number}.pdf"'

    return response


def format_budget(value):
    if not value:
        return "N/A"
    return f"{int(value):,} FCFA".replace(",", " ")