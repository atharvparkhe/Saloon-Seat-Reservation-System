from django.conf import settings
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
from io import BytesIO
import uuid


def save_invoice(params:dict):
    try:
        template = get_template("invoice.html")
        html = template.render(params)
        response = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
        file_name = str(uuid.uuid4())

        with open(str(settings.BASE_DIR) + f"/data/invoice/{file_name}.pdf", "wb+") as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)

        if pdf.err:
            return "", False

        return file_name, True

    except Exception as e:
        print(e)