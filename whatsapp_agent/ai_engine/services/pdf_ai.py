from ai_engine.models import Document

from .config import client, MODEL
from .prompts import SYSTEM_PROMPT_PDF


def ask_pdf_ai(doc_id, question):

    try:

        if client is None:
            return "⚠️ Le service IA n'est pas disponible actuellement."

        doc = Document.objects.filter(
            id=doc_id
        ).first()

        if not doc:

            return "❌ Document introuvable."

        if not doc.content:

            return "❌ Document vide."

        response = client.chat.completions.create(

            model=MODEL,

            temperature=0.3,

            max_tokens=700,

            messages=[

                {

                    "role": "system",

                    "content": SYSTEM_PROMPT_PDF

                },

                {

                    "role": "user",

                    "content": f"{doc.content}\n\nQuestion : {question}"

                }

            ]

        )

        return response.choices[0].message.content.strip()

    except Exception as e:

        print(e)

        return "Erreur lors de l'analyse du document."