from .ai_chat import ask_ai
from .pdf_ai import ask_pdf_ai


def ask_smart_ai(
    phone_number,
    prospect,
    message_type,
    message_content,
    doc_id=None
):

    # ==================================================
    # DOCUMENT FLOW
    # ==================================================
    if message_type == "document" or doc_id:

        return ask_pdf_ai(
            doc_id,
            message_content
        )

    # ==================================================
    # CHAT FLOW
    # ==================================================
    return ask_ai(
        phone_number,
        prospect,   # si ton ask_ai l’utilise
        message_content
    )