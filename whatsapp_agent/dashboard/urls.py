from django.urls import path
from .views import (
    dashboard_home,
    prospects_list,
    prospect_detail,
    toggle_human_takeover,
    conversations_inbox,
    download_prospect_pdf,
)

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),

    path('prospects/', prospects_list, name='prospects_list'),

    # ✅ DETAIL PAR NUMERO (IMPORTANT)
    path('prospects/<str:phone_number>/', prospect_detail, name='prospect_detail'),

    path(
        'prospects/<str:phone_number>/takeover/',
        toggle_human_takeover,
        name='toggle_human_takeover'
    ),

    path("conversations/", conversations_inbox, name="conversations_inbox"),
    path("prospect/<str:phone_number>/pdf/", download_prospect_pdf, name="prospect_pdf")
    
]